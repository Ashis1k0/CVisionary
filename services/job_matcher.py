def _normalize_skill(s: str) -> str:
    return (s or "").strip().lower()


def _parse_job_skills(skills_text: str):
    if not skills_text:
        return []
    return [_normalize_skill(x) for x in skills_text.split(",") if _normalize_skill(x)]


def match_jobs(sqlalchemy_session, candidate_skills, limit: int = 6):
    """
    Simple matching:
    - score = number of overlapping skills
    - returns list sorted desc
    Output shape is frontend-friendly and JSON-safe.
    """
    from app import JobPost

    cand = [_normalize_skill(s) for s in (candidate_skills or []) if _normalize_skill(s)]
    if not cand:
        return []

    jobs = sqlalchemy_session.query(JobPost).order_by(JobPost.created_at.desc()).all()
    scored = []
    for job in jobs:
        job_skills = _parse_job_skills(job.skills or "")
        if not job_skills:
            continue
        overlap = set(cand).intersection(set(job_skills))
        score = len(overlap)
        if score <= 0:
            continue
        scored.append(
            {
                "job_id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location or "N/A",
                "match_score": score,
                "matching_skills": sorted(list(overlap)),
            }
        )

    scored.sort(key=lambda x: x["match_score"], reverse=True)
    return scored[:limit]

