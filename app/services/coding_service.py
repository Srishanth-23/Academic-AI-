from sqlalchemy.orm import Session
from app.models.coding_profile import CodingProfile
from app.models.coding_activity import CodingActivity
from app.models.contest_history import ContestHistory


def create_coding_profile(db: Session, data):

    profile = CodingProfile(
        student_id=data.student_id,
        leetcode_username=data.leetcode_username,
        codechef_username=data.codechef_username,
        codeforces_username=data.codeforces_username
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


def add_daily_activity(db: Session, data):

    activity = CodingActivity(
        student_id=data.student_id,
        platform=data.platform,
        date=data.date,
        problems_solved=data.problems_solved
    )

    db.add(activity)
    db.commit()
    db.refresh(activity)

    return activity


def add_contest_result(db: Session, data):

    contest = ContestHistory(
        student_id=data.student_id,
        platform=data.platform,
        contest_name=data.contest_name,
        rank=data.rank,
        problems_solved=data.problems_solved,
        contest_date=data.contest_date
    )

    db.add(contest)
    db.commit()
    db.refresh(contest)

    return contest