from flask import Blueprint, render_template, request, redirect, url_for, session, flash


recruiter_bp = Blueprint("recruiter", __name__)


def _require_recruiter():
    return "recruiter_id" in session


@recruiter_bp.route("/recruiter/register", methods=["GET", "POST"])
def recruiter_register():
    from app import sqlalchemy_session, Recruiter

    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = (request.form.get("password") or "").strip()
        company = (request.form.get("company") or "").strip()

        if not name or not email or not password:
            flash("Name, email and password are required", "error")
            return render_template("recruiter_register.html")

        existing = sqlalchemy_session.query(Recruiter).filter_by(email=email).first()
        if existing:
            flash("Recruiter email already exists", "error")
            return render_template("recruiter_register.html")

        rec = Recruiter(name=name, email=email, password=password, company=company)
        sqlalchemy_session.add(rec)
        sqlalchemy_session.commit()

        flash("Recruiter account created. Please login.", "success")
        return redirect(url_for("recruiter.recruiter_login"))

    return render_template("recruiter_register.html")


@recruiter_bp.route("/recruiter/login", methods=["GET", "POST"])
def recruiter_login():
    from app import sqlalchemy_session, Recruiter

    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = (request.form.get("password") or "").strip()

        rec = sqlalchemy_session.query(Recruiter).filter_by(email=email, password=password).first()
        if not rec:
            flash("Invalid recruiter credentials", "error")
            return render_template("recruiter_login.html")

        session["recruiter_id"] = rec.id
        session["recruiter_name"] = rec.name
        session["recruiter_company"] = rec.company or ""
        return redirect(url_for("recruiter.recruiter_dashboard"))

    return render_template("recruiter_login.html")


@recruiter_bp.route("/recruiter/logout")
def recruiter_logout():
    session.pop("recruiter_id", None)
    session.pop("recruiter_name", None)
    session.pop("recruiter_company", None)
    return redirect(url_for("index"))


@recruiter_bp.route("/recruiter/dashboard")
def recruiter_dashboard():
    from app import sqlalchemy_session, Recruiter, JobPost

    if not _require_recruiter():
        return redirect(url_for("recruiter.recruiter_login"))

    recruiter_id = session["recruiter_id"]
    recruiter = sqlalchemy_session.query(Recruiter).filter_by(id=recruiter_id).first()
    jobs = sqlalchemy_session.query(JobPost).filter_by(recruiter_id=recruiter_id).order_by(JobPost.created_at.desc()).all()

    return render_template("recruiter_dashboard.html", recruiter=recruiter, jobs=jobs)


@recruiter_bp.route("/recruiter/job/create", methods=["GET", "POST"])
def recruiter_job_create():
    from app import sqlalchemy_session, Recruiter, JobPost

    if not _require_recruiter():
        return redirect(url_for("recruiter.recruiter_login"))

    recruiter_id = session["recruiter_id"]
    recruiter = sqlalchemy_session.query(Recruiter).filter_by(id=recruiter_id).first()

    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        location = (request.form.get("location") or "").strip()
        description = (request.form.get("description") or "").strip()
        skills = (request.form.get("skills") or "").strip()
        experience = (request.form.get("experience") or "").strip()
        salary = (request.form.get("salary") or "").strip()

        if not title:
            flash("Title is required", "error")
            return render_template("recruiter_job_create.html", recruiter=recruiter)

        job = JobPost(
            title=title,
            company=recruiter.company or recruiter.name,
            location=location,
            description=description,
            skills=skills,
            experience=experience,
            salary=salary,
            recruiter_id=recruiter_id,
        )
        sqlalchemy_session.add(job)
        sqlalchemy_session.commit()

        flash("Job posted successfully", "success")
        return redirect(url_for("recruiter.recruiter_jobs"))

    return render_template("recruiter_job_create.html", recruiter=recruiter)


@recruiter_bp.route("/recruiter/jobs")
def recruiter_jobs():
    from app import sqlalchemy_session, JobPost

    if not _require_recruiter():
        return redirect(url_for("recruiter.recruiter_login"))

    recruiter_id = session["recruiter_id"]
    jobs = sqlalchemy_session.query(JobPost).filter_by(recruiter_id=recruiter_id).order_by(JobPost.created_at.desc()).all()
    return render_template("recruiter_jobs.html", jobs=jobs)


@recruiter_bp.route("/recruiter/job/edit/<int:job_id>", methods=["GET", "POST"])
def recruiter_job_edit(job_id):
    from app import sqlalchemy_session, JobPost

    if not _require_recruiter():
        return redirect(url_for("recruiter.recruiter_login"))

    recruiter_id = session["recruiter_id"]
    job = sqlalchemy_session.query(JobPost).filter_by(id=job_id, recruiter_id=recruiter_id).first()
    if not job:
        flash("Job not found", "error")
        return redirect(url_for("recruiter.recruiter_jobs"))

    if request.method == "POST":
        job.title = (request.form.get("title") or "").strip() or job.title
        job.location = (request.form.get("location") or "").strip()
        job.description = (request.form.get("description") or "").strip()
        job.skills = (request.form.get("skills") or "").strip()
        job.experience = (request.form.get("experience") or "").strip()
        job.salary = (request.form.get("salary") or "").strip()
        sqlalchemy_session.commit()
        flash("Job updated successfully", "success")
        return redirect(url_for("recruiter.recruiter_jobs"))

    return render_template("recruiter_job_edit.html", job=job)


@recruiter_bp.route("/recruiter/job/delete/<int:job_id>", methods=["POST"])
def recruiter_job_delete(job_id):
    from app import sqlalchemy_session, JobPost, JobApplication

    if not _require_recruiter():
        return redirect(url_for("recruiter.recruiter_login"))

    recruiter_id = session["recruiter_id"]
    job = sqlalchemy_session.query(JobPost).filter_by(id=job_id, recruiter_id=recruiter_id).first()
    if not job:
        flash("Job not found", "error")
        return redirect(url_for("recruiter.recruiter_jobs"))

    # Clean dependent applications first
    sqlalchemy_session.query(JobApplication).filter_by(job_id=job.id).delete()
    sqlalchemy_session.delete(job)
    sqlalchemy_session.commit()
    flash("Job deleted successfully", "success")
    return redirect(url_for("recruiter.recruiter_jobs"))


@recruiter_bp.route("/recruiter/applications")
def recruiter_applications():
    from app import sqlalchemy_session, JobApplication, JobPost, User, CandidateProfile

    if not _require_recruiter():
        return redirect(url_for("recruiter.recruiter_login"))

    recruiter_id = session["recruiter_id"]

    # get recruiter's jobs
    jobs = sqlalchemy_session.query(JobPost).filter_by(recruiter_id=recruiter_id).all()
    job_ids = [j.id for j in jobs]
    if not job_ids:
        return render_template("recruiter_applications.html", applications=[])

    applications = sqlalchemy_session.query(JobApplication).filter(JobApplication.job_id.in_(job_ids)).order_by(JobApplication.created_at.desc()).all()

    rows = []
    for app_row in applications:
        candidate = sqlalchemy_session.query(User).filter_by(id=app_row.candidate_id).first()
        job = sqlalchemy_session.query(JobPost).filter_by(id=app_row.job_id).first()
        profile = None
        if candidate:
            profile = sqlalchemy_session.query(CandidateProfile).filter_by(email=candidate.email).first()
        rows.append(
            {
                "candidate_username": candidate.username if candidate else "Unknown",
                "candidate_email": candidate.email if candidate else "Unknown",
                "job_title": job.title if job else "Unknown",
                "job_company": job.company if job else "Unknown",
                "ats_score": profile.ats_score if profile else None,
                "created_at": app_row.created_at,
                "status": app_row.status,
            }
        )

    return render_template("recruiter_applications.html", applications=rows)

