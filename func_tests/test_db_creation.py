import sqlalchemy
import sqlalchemy.orm as orm
from src.db.models import MediaType
from func_tests.general_fixtures import create_db  # noqa: F401


def test_db_running(db):
    with orm.Session(db) as session:
        media = MediaType(title="Telegram", resource_link="telegram.org")
        session.add(media)
        session.commit()
    with orm.Session(db) as session:
        media = session.scalar(
            sqlalchemy.select(MediaType).where(MediaType.title == "Telegram")
        )
        assert media is not None
        assert media.resource_link == "telegram.org"
