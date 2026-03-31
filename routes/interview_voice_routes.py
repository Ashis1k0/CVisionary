from flask import Blueprint, jsonify, request, session, render_template, redirect, url_for

from services.voice_interview_ai import generate_questions, evaluate_answer


interview_voice_bp = Blueprint("interview_voice", __name__)


def get_interview_candidate_map(sqlalchemy_session, candidate_ids):
    """
    Helper used from the main app to resolve candidate usernames/emails
    for the admin interviews view.
    """
    from app import User  # local import to avoid circulars

    if not candidate_ids:
        return {}

    users = (
        sqlalchemy_session.query(User)
        .filter(User.id.in_(candidate_ids))
        .all()
    )
    return {
        u.id: {"username": u.username, "email": u.email}
        for u in users
    }


def _ensure_user_logged_in():
    if "user_logged_in" not in session:
        return False
    return True


@interview_voice_bp.route("/interview/voice", methods=["GET"])
def voice_interview_page():
    if not _ensure_user_logged_in():
        return redirect(url_for("user_login"))
    return render_template("voice_interview.html")


@interview_voice_bp.route("/interview/voice/start", methods=["POST"])
def start_voice_interview():
    if not _ensure_user_logged_in():
        return jsonify({"error": "Login required"}), 401

    from app import sqlalchemy_session, User, InterviewSession  # local imports

    data = request.get_json() or {}
    job_role = data.get("job_role", "").strip() or "Software Engineer"
    difficulty = data.get("difficulty", "").strip() or "Medium"
    skills = data.get("skills", "").strip()
    experience = data.get("experience", "").strip()

    # Resolve candidate (logged-in user)
    username = session.get("username")
    user = sqlalchemy_session.query(User).filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User account not found"}), 400

    # Generate questions via Gemini
    questions = generate_questions(skills=skills, job_role=job_role, experience=experience)
    if not questions:
        return jsonify({"error": "Unable to generate interview questions. Please try again."}), 500

    # Create DB interview session
    interview = InterviewSession(
        candidate_id=user.id,
        job_role=job_role,
        difficulty=difficulty,
        current_question=0,
        total_score=0,
        feedback="",
    )
    sqlalchemy_session.add(interview)
    sqlalchemy_session.commit()

    # Store questions and running state in Flask session
    voice_state = session.get("voice_interview_sessions", {})
    voice_state[str(interview.id)] = {
        # canonical keys
        "questions": questions,
        "index": 0,
        "score": 0,
        "answers": [],
        # backward-compatible keys (if older code still expects them)
        "current_index": 0,
        "total_score": 0,
    }
    session["voice_interview_sessions"] = voice_state

    first_question = questions[0]["question"]
    return jsonify(
        {
            "session_id": interview.id,
            "total_questions": len(questions),
            "question_index": 0,
            "question": first_question,
        }
    )


@interview_voice_bp.route("/interview/voice/get_question", methods=["POST"])
def get_next_question():
    if not _ensure_user_logged_in():
        return jsonify({"error": "Login required"}), 401

    data = request.get_json() or {}
    session_id = str(data.get("session_id"))

    voice_state = session.get("voice_interview_sessions", {})
    state = voice_state.get(str(session_id))
    if not state:
        return jsonify({"error": "Interview session not found"}), 404

    # support both new and legacy key names
    idx = state.get("index", state.get("current_index", 0))
    questions = state.get("questions", [])
    if idx >= len(questions):
        return jsonify({"finished": True}), 200

    return jsonify(
        {
            "session_id": int(session_id),
            "total_questions": len(questions),
            "question_index": idx,
            "question": questions[idx]["question"],
        }
    )


@interview_voice_bp.route("/interview/voice/answer", methods=["POST"])
def submit_answer():
    if not _ensure_user_logged_in():
        return jsonify({"error": "Login required"}), 401

    from app import sqlalchemy_session, InterviewSession  # local imports

    data = request.get_json() or {}
    session_id = str(data.get("session_id"))
    force_end = bool(data.get("force_end"))
    answer_text = (data.get("answer") or "").strip()

    voice_state = session.get("voice_interview_sessions", {})
    state = voice_state.get(str(session_id))
    if not state:
        return jsonify({"error": "Interview session not found"}), 404

    questions = state.get("questions", [])
    total_questions = len(questions)

    # Support both new and legacy keys
    idx = state.get("index", state.get("current_index", 0))
    score_sum = state.get("score", state.get("total_score", 0))

    # Handle manual early termination
    if force_end:
        interview = sqlalchemy_session.query(InterviewSession).filter_by(id=int(session_id)).first()
        if interview:
            answered_count = len(state.get("answers", []))
            avg_score = round(score_sum / max(answered_count, 1)) if answered_count else 0
            interview.current_question = answered_count
            interview.total_score = avg_score
            combined_feedback = []
            for a in state.get("answers", []):
                combined_feedback.append(
                    f"Q: {a['question']}\nScore: {a['score']}/10\nFeedback: {a['feedback']}\nTips: {a['tips']}\n"
                )
            interview.feedback = "\n\n".join(combined_feedback)
            sqlalchemy_session.commit()

        return jsonify(
            {
                "finished": True,
                "redirect_url": url_for("interview_voice.voice_interview_result", session_id=session_id),
            }
        )

    if idx >= total_questions:
        return jsonify({"error": "No more questions"}), 400

    question_text = questions[idx]["question"]

    # Evaluate with Gemini
    eval_result = evaluate_answer(question=question_text, answer=answer_text)
    score = eval_result.get("score", 0)
    feedback = eval_result.get("feedback", "")
    tips = eval_result.get("tips", "")

    # Update in-memory state
    score_sum = score_sum + score
    state["score"] = score_sum
    state["total_score"] = score_sum  # legacy key

    state.setdefault("answers", []).append(
        {
            "question": question_text,
            "answer": answer_text,
            "score": score,
            "feedback": feedback,
            "tips": tips,
        }
    )

    # Move to next question index
    idx += 1
    state["index"] = idx
    state["current_index"] = idx  # legacy key

    voice_state[str(session_id)] = state
    session["voice_interview_sessions"] = voice_state

    # Determine completion and update DB if finished
    is_finished = idx >= total_questions
    if is_finished:
        interview = sqlalchemy_session.query(InterviewSession).filter_by(id=int(session_id)).first()
        if interview:
            answered_count = len(state.get("answers", []))
            avg_score = round(score_sum / max(answered_count, 1)) if answered_count else 0
            interview.current_question = total_questions
            interview.total_score = avg_score
            combined_feedback = []
            for a in state.get("answers", []):
                combined_feedback.append(
                    f"Q: {a['question']}\nScore: {a['score']}/10\nFeedback: {a['feedback']}\nTips: {a['tips']}\n"
                )
            interview.feedback = "\n\n".join(combined_feedback)
            sqlalchemy_session.commit()

    return jsonify(
        {
            "session_id": int(session_id),
            "question_index": idx - 1,
            "score": score,
            "feedback": feedback,
            "tips": tips,
            "finished": is_finished,
            "next_question": None if is_finished or idx >= total_questions else questions[idx]["question"],
            "redirect_url": url_for("interview_voice.voice_interview_result", session_id=session_id)
            if is_finished
            else None,
        }
    )


@interview_voice_bp.route("/interview/voice/result/<int:session_id>", methods=["GET"])
def voice_interview_result(session_id):
    if not _ensure_user_logged_in():
        return redirect(url_for("user_login"))

    from app import sqlalchemy_session, InterviewSession, User  # local imports

    interview = sqlalchemy_session.query(InterviewSession).filter_by(id=session_id).first()
    if not interview:
        return "Interview session not found", 404

    user = sqlalchemy_session.query(User).filter_by(id=interview.candidate_id).first()

    # Rebuild detailed answers from Flask session if available
    detailed = None
    voice_state = session.get("voice_interview_sessions", {})
    state = voice_state.get(str(session_id))
    if state:
        detailed = state.get("answers", [])

    return render_template(
        "voice_interview_result.html",
        interview=interview,
        user=user,
        detailed_answers=detailed,
    )

