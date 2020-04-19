import sqlite3
import logging

logger = logging.getLogger(__name__)


class Status:

    SCHEMA = """CREATE TABLE IF NOT EXISTS status (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id CHAR(16),
        real_name TEXT,
        status_text TEXT,
        status_emoji TEXT,
        status_expiration INTEGER
    )"""

    def __init__(self, bot):
        self.bot = bot

        db = sqlite3.connect("tmp/status.sqlite")
        self.db = db

        # Initialize the database
        cursor = db.cursor()
        cursor.execute(self.SCHEMA)
        db.commit()

    def on_user_change(self, context):
        user = context.Author
        data = {
            "user_id": user.id,
            "real_name": user.real_name,
            "status_text": user.status.status_text,
            "status_emoji": user.status.status_emoji,
            "status_expiration": user.status.status_expiration,
        }

        cursor = self.db.cursor()

        cursor.execute(
            """SELECT user_id
            FROM status
            WHERE user_id = :user_id""",
            data,
        )

        if cursor.fetchone() is None:
            cursor.execute(
                """INSERT INTO status (
                user_id,
                real_name,
                status_text,
                status_emoji,
                status_expiration
            ) VALUES (
                :user_id,
                :real_name,
                :status_text,
                :status_emoji,
                :status_expiration
            )""",
                data,
            )
        else:
            cursor.execute(
                """UPDATE status SET
                real_name = :real_name,
                status_text = :status_text,
                status_emoji = :status_emoji,
                status_expiration = :status_expiration
            WHERE user_id = :user_id""",
                data,
            )

        logger.info("Updating status: %s", data)

        self.db.commit()


def setup(bot):
    return Status(bot)
