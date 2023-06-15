from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from src.database.models import User, Comment, UserRole
from src.schemas import CommentBase


async def create_comment(image_id: int, body: CommentBase, db: Session, user: User) -> Comment:
    """
    The create_comment function creates a new comment in the database.
        Args:
            image_id (int): The id of the image to which this comment belongs.
            body (CommentBase): A CommentBase object containing information about the new comment.
                This includes its text and user_id, but not its id or date created/updated fields,
                as these are generated by SQLAlchemy when it is added to the database.

    :param image_id: int: Identify the image that the comment is being added to
    :param body: CommentBase: Specify the type of data that is expected to be passed in
    :param db: Session: Access the database
    :param user: User: Get the user_id from the logged in user
    :return: A comment object
    """
    new_comment = Comment(text=body.text, image_id=image_id, user_id=user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


async def show_single_comment(comment_id: int, db: Session, user: User) -> Comment | None:

    """
    The show_single_comment function returns a single comment from the database.
        Args:
            comment_id (int): The id of the comment to be returned.
            db (Session): A connection to the database.  This is provided by FastAPI when it calls this function, so you don't need to worry about it!
            user (User): The currently logged in user, as determined by FastAPI's authentication system.  Again, this is provided for you automatically and does not need to be passed in explicitly!

    :param comment_id: int: Specify the id of the comment that we want to retrieve
    :param db: Session: Access the database
    :param user: User: Check if the user is authorized to see the comment
    :return: The comment with the given id, if it exists
    """
    return db.query(Comment).filter(and_(Comment.id == comment_id, Comment.user_id == user.id)).first()


async def show_user_comments(user_id: int, db: Session) -> List[Comment] | None:

    """
    The show_user_comments function returns a list of comments made by the user with the given id.
        If no such user exists, it returns None.

    :param user_id: int: Specify the user_id of the user whose comments we want to retrieve
    :param db: Session: Pass the database session to the function
    :return: A list of comments
    """
    return db.query(Comment).filter(Comment.user_id == user_id).all()


async def show_user_image_comments(user_id: int, image_id: int, db: Session) -> List[Comment] | None:

    """
    The show_user_image_comments function returns a list of comments for a given user and image.
        Args:
            user_id (int): The id of the user whose comments are being retrieved.
            image_id (int): The id of the image whose comments are being retrieved.

    :param user_id: int: Filter the comments by user_id
    :param image_id: int: Filter the comments by image_id
    :param db: Session: Pass the database session to the function
    :return: A list of comments, or none if the user doesn't exist
    """
    return db.query(Comment).filter(and_(Comment.image_id == image_id, Comment.user_id == user_id)).all()


async def edit_comment(comment_id: int, body: CommentBase, db: Session, user: User) -> Comment | None:

    """
    The edit_comment function allows a user to edit their own comment.
        Args:
            comment_id (int): The id of the comment that is being edited.
            body (CommentBase): The new text for the comment.

    :param comment_id: int: Find the comment in the database
    :param body: CommentBase: Pass the data from the request body to this function
    :param db: Session: Connect to the database
    :param user: User: Check if the user is an admin, moderator or the author of the comment
    :return: A comment object
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        if user.role in [UserRole.admin, UserRole.moder] or comment.user_id == user.id:
            comment.text = body.text
            comment.updated_at = func.now()
            comment.update_status = True
            db.commit()
    return comment


async def delete_comment(comment_id: int, db: Session, user: User) -> None:

    """
    The delete_comment function deletes a comment from the database.
        Args:
            comment_id (int): The id of the comment to be deleted.
            db (Session): A connection to the database.
            user (User): The user who is deleting this post.

    :param comment_id: int: Identify the comment to be deleted
    :param db: Session: Connect to the database
    :param user: User: Check if the user is authorized to delete a comment
    :return: The comment that was deleted
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
    return comment
