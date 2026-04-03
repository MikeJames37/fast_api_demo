from typing import Optional

from sqlalchemy.orm import Session

from app.models import User

def get_user(db: Session, login: str) -> Optional[User]:
    return db.query(User).filter(User.login == login).scalar()

def create_user(db: Session, login: str) -> User:
    user = User(login=login)
    db.add(user)
    db.flush()
    return user
