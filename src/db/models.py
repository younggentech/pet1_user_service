from typing import List, Optional

import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy_utils as su


class Base(orm.DeclarativeBase):
    pass


class User(Base):
    """
    Each system user has one possible role.

    The hierarchy: user -> moderator -> admin.
    a user has several attributes, including a list of assosiated social media,
    and feedbacks for the user.
    """

    __tablename__ = "users"
    GENDERS = (("Male", "Male"), ("Female", "Female"), ("Other", "Other"))
    ROLES = (
        ("admin", "Admin"),
        ("user", "User"),
        ("moderator", "Moderator"),
        ("deleted", "Deleted"),
    )
    user_id: orm.Mapped[sqlalchemy.UUID] = orm.mapped_column(
        sqlalchemy.UUID(as_uuid=True), primary_key=True
    )
    email: orm.Mapped[su.EmailType] = orm.mapped_column(su.EmailType)
    is_verified: orm.Mapped[bool] = orm.mapped_column(
        sqlalchemy.Boolean, default=False
    )
    first_name: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(30))
    last_name: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(30))
    bio: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(100))
    gender: orm.Mapped[str] = orm.mapped_column(su.ChoiceType(GENDERS))
    role: orm.Mapped[str] = orm.mapped_column(su.ChoiceType(ROLES))
    social_media: orm.Mapped[Optional[List["SocialMediaAccount"]]] = (
        orm.relationship()
    )
    password_hash: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(100))
    credibility_score: orm.Mapped[int] = orm.mapped_column(sqlalchemy.Integer)
    feedbacks: orm.Mapped[Optional[List["Feedback"]]] = orm.relationship()
    verification_code: orm.Mapped[Optional["UserVerification"]] = (
        orm.relationship()
    )


class SocialMediaAccount(Base):
    """Map user to media type, contains account information"""

    __tablename__ = "social_media_accounts"
    social_media_account_id: orm.Mapped[sqlalchemy.UUID] = orm.mapped_column(
        sqlalchemy.UUID(as_uuid=True), primary_key=True
    )
    user_id: orm.Mapped[sqlalchemy.UUID] = orm.mapped_column(
        sqlalchemy.ForeignKey("users.user_id")
    )
    media_type_name: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.ForeignKey("media_types.title")
    )
    media_type: orm.Mapped[Optional["MediaType"]] = orm.relationship()
    profile_link: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(50))
    profile_id: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(50))
    phone: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(20))
    user_name: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(20))


class MediaType(Base):
    """Social media resources"""

    __tablename__ = "media_types"
    title: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.String(30), primary_key=True
    )
    resource_link: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(50))


class Feedback(Base):
    """
    Each user has assosiated feedback records.

    Feedback is given to a user within one project by many students.
    Projects are stored in another microservice, thus, the feedback contains
    an external field received from another microservice.
    Feedback contains comments and scorings from different team members.
    """

    __tablename__ = "feedbacks"
    feedback_id: orm.Mapped[sqlalchemy.UUID] = orm.mapped_column(
        sqlalchemy.UUID(as_uuid=True), primary_key=True
    )
    project_name: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(30))
    to_user: orm.Mapped[sqlalchemy.UUID] = orm.mapped_column(
        sqlalchemy.ForeignKey("users.user_id")
    )
    comments: orm.Mapped[Optional[List["Comment"]]] = orm.relationship()
    scores: orm.Mapped[Optional[List["Score"]]] = orm.relationship()


class Comment(Base):
    """Each comment is given by a user within a feedback"""

    __tablename__ = "comments"
    comment_id: orm.Mapped[sqlalchemy.UUID] = orm.mapped_column(
        sqlalchemy.UUID(as_uuid=True), primary_key=True
    )
    from_user: orm.Mapped[sqlalchemy.UUID] = orm.mapped_column(
        sqlalchemy.ForeignKey("users.user_id")
    )
    feedback_id: orm.Mapped[sqlalchemy.UUID] = orm.mapped_column(
        sqlalchemy.ForeignKey("feedbacks.feedback_id")
    )
    text: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(300))
    timestamp: orm.Mapped[int] = orm.mapped_column(sqlalchemy.Integer)


class Score(Base):
    """Each Score is given by a user within a feedback"""

    __tablename__ = "scores"
    score_id: orm.Mapped[sqlalchemy.UUID] = orm.mapped_column(
        sqlalchemy.UUID(as_uuid=True), primary_key=True
    )
    feedback_id: orm.Mapped[sqlalchemy.UUID] = orm.mapped_column(
        sqlalchemy.ForeignKey("feedbacks.feedback_id")
    )
    from_user: orm.Mapped[sqlalchemy.UUID] = orm.mapped_column(
        sqlalchemy.ForeignKey("users.user_id")
    )
    metrica_name: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(20))
    score: orm.Mapped[int] = orm.mapped_column(sqlalchemy.Integer)
    timestamp: orm.Mapped[int] = orm.mapped_column(sqlalchemy.Integer)


class UserVerification(Base):
    """Store code for account verification"""

    __tablename__ = "user_verifications"
    verification_id: orm.Mapped[sqlalchemy.UUID] = orm.mapped_column(
        sqlalchemy.UUID(as_uuid=True), primary_key=True
    )
    user_id: orm.Mapped[sqlalchemy.UUID] = orm.mapped_column(
        sqlalchemy.ForeignKey("users.user_id")
    )
    verification_code: orm.Mapped[int] = orm.mapped_column(sqlalchemy.Integer)
    timestamp: orm.Mapped[int] = orm.mapped_column(sqlalchemy.Integer)
