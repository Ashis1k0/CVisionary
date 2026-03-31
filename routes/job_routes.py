from flask import Blueprint, redirect, url_for, session, flash, jsonify, render_template, request


jobs_bp = Blueprint("jobs", __name__)


def _require_user():
    return "user_logged_in" in session and session.get("username")


@jobs_bp.route("/jobs")
def jobs_board():
    from app import sqlalchemy_session, JobPost, JobApplication, User

    query = (request.args.get("q") or "").strip().lower()
    jobs = sqlalchemy_session.query(JobPost).order_by(JobPost.created_at.desc()).all()

    if query:
        jobs = [
            j for j in jobs
            if query in (j.title or "").lower()
            or query in (j.skills or "").lower()
            or query in (j.company or "").lower()
        ]

    applied_job_ids = set()
    if _require_user():
        username = session.get("username")
        user = sqlalchemy_session.query(User).filter_by(username=username).first()
        if user:
            apps = sqlalchemy_session.query(JobApplication).filter_by(candidate_id=user.id).all()
            applied_job_ids = {a.job_id for a in apps}

    return render_template(
        "jobs_board.html",
        jobs=jobs,
        applied_job_ids=applied_job_ids,
        search_query=query,
        user_logged_in=_require_user(),
    )


@jobs_bp.route("/jobs/applied")
def my_applied_jobs():
    if not _require_user():
        flash("Please login to view your applied jobs", "error")
        return redirect(url_for("user_login"))

    from app import sqlalchemy_session, User, JobApplication, JobPost

    username = session.get("username")
    user = sqlalchemy_session.query(User).filter_by(username=username).first()
    if not user:
        flash("User not found", "error")
        return redirect(url_for("index"))

    applications = (
        sqlalchemy_session.query(JobApplication)
        .filter_by(candidate_id=user.id)
        .order_by(JobApplication.created_at.desc())
        .all()
    )

    rows = []
    for app_row in applications:
        job = sqlalchemy_session.query(JobPost).filter_by(id=app_row.job_id).first()
        if not job:
            continue
        rows.append(
            {
                "application_id": app_row.id,
                "job_id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location or "N/A",
                "salary": job.salary or "N/A",
                "experience": job.experience or "N/A",
                "status": app_row.status,
                "applied_at": app_row.created_at,
            }
        )

    return render_template("candidate_applied_jobs.html", applications=rows)


@jobs_bp.route("/job/apply/<int:job_id>")
def apply_job(job_id):
    if not _require_user():
        flash("Please login to apply for jobs", "error")
        return redirect(url_for("user_login"))

    from app import sqlalchemy_session, User, JobApplication

    username = session.get("username")
    user = sqlalchemy_session.query(User).filter_by(username=username).first()
    if not user:
        flash("User not found", "error")
        return redirect(url_for("index"))

    # prevent duplicate applications
    existing = sqlalchemy_session.query(JobApplication).filter_by(job_id=job_id, candidate_id=user.id).first()
    if existing:
        flash("You have already applied for this job.", "success")
        return redirect(url_for("index"))

    app_row = JobApplication(job_id=job_id, candidate_id=user.id, status="Applied")
    sqlalchemy_session.add(app_row)
    sqlalchemy_session.commit()

    flash("Application submitted successfully!", "success")
    return redirect(url_for("index"))


@jobs_bp.route("/job/apply-ajax/<int:job_id>", methods=["POST"])
def apply_job_ajax(job_id):
    if not _require_user():
        return jsonify({"success": False, "message": "Please login first"}), 401

    from app import sqlalchemy_session, User, JobApplication

    username = session.get("username")
    user = sqlalchemy_session.query(User).filter_by(username=username).first()
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 400

    existing = sqlalchemy_session.query(JobApplication).filter_by(job_id=job_id, candidate_id=user.id).first()
    if existing:
        return jsonify({"success": True, "applied": True, "message": "Already applied"})

    app_row = JobApplication(job_id=job_id, candidate_id=user.id, status="Applied")
    sqlalchemy_session.add(app_row)
    sqlalchemy_session.commit()
    return jsonify({"success": True, "applied": True, "message": "Application submitted"})

