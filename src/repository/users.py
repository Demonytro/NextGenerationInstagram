from sqlalchemy.orm import Session, Query
from libgravatar import Gravatar
from src.database.models import User, UserRole
from src.schemas import UserModel



async def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()

async def create_user(body: UserModel, db: Session) -> User:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)

    user_count = db.query(User).count()
    # Якщо ще немає жодного користувача, встановлюємо його роль як "admin"
    if user_count == 0:
        body.role = UserRole.ADMIN

    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()