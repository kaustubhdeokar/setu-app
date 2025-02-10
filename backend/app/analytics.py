from app.database import get_db
from sqlalchemy.orm import Session
from app.models import Analytics

def update_analytics_table(case: str, username: str, db: Session):
    analytics_entry = db.query(Analytics).filter(Analytics.username == username).first()

    if not analytics_entry:
        if case == "kyc_fail":
            new_analytics_entry = Analytics(
                username=username,
                fail_kyc=1,
                total_fail=1
            )
        elif case == "bank_fail":
            new_analytics_entry = Analytics(
                username=username,
                fail_bank=1,
                total_fail=1
            )
        else:
            new_analytics_entry = Analytics(
                username=username,
                pass_kyc=1,
                pass_bank=1,
                total_pass=1
            )
        db.add(new_analytics_entry)
        db.commit()
    else:
        if case == "kyc_fail":
            analytics_entry.fail_kyc += 1
            analytics_entry.total_fail += 1
        elif case == "bank_fail":
            analytics_entry.fail_bank += 1
            analytics_entry.total_fail += 1
        else:
            analytics_entry.pass_kyc+=1
            analytics_entry.pass_bank+=1
            analytics_entry.total_pass += 1
    db.commit()