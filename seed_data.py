from datetime import datetime


def seed_if_needed(sqlalchemy_session):
    """
    Seed recruiter + jobs once, if DB is empty of JobPost rows.
    Safe to call on app startup.
    """
    from app import Recruiter, JobPost

    has_jobs = sqlalchemy_session.query(JobPost).first()
    if has_jobs:
        return

    # recruiter
    recruiter = sqlalchemy_session.query(Recruiter).filter_by(email="recruiter@test.com").first()
    if not recruiter:
        recruiter = Recruiter(
            name="Test Recruiter",
            email="recruiter@test.com",
            password="123456",
            company="TechCorp",
            created_at=datetime.now(),
        )
        sqlalchemy_session.add(recruiter)
        sqlalchemy_session.commit()

    jobs = [
        {
            "title": "Python Developer",
            "skills": "python, flask, mysql",
            "location": "Remote",
            "experience": "2+ years",
            "salary": "10 LPA",
            "description": "Build Flask APIs and maintain MySQL-backed services.",
        },
        {
            "title": "Java Developer",
            "skills": "java, spring, mysql",
            "location": "Remote",
            "experience": "2+ years",
            "salary": "12 LPA",
            "description": "Develop Spring services and integrate with MySQL.",
        },
        {
            "title": "Frontend Developer",
            "skills": "html, css, js, react",
            "location": "Remote",
            "experience": "1+ years",
            "salary": "9 LPA",
            "description": "Build responsive UIs using React and modern web tooling.",
        },
        {
            "title": "Data Analyst",
            "skills": "python, pandas, sql",
            "location": "Remote",
            "experience": "1+ years",
            "salary": "8 LPA",
            "description": "Analyze datasets and build reports/dashboards.",
        },
    ]

    for j in jobs:
        sqlalchemy_session.add(
            JobPost(
                title=j["title"],
                company=recruiter.company or "TechCorp",
                location=j["location"],
                description=j["description"],
                skills=j["skills"],
                experience=j["experience"],
                salary=j["salary"],
                recruiter_id=recruiter.id,
                created_at=datetime.now(),
            )
        )

    sqlalchemy_session.commit()

