from datetime import datetime

from database.db import SessionLocal
from sqlalchemy import text


def create_table():
    with SessionLocal() as db:
        db.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS subscribers (
                    webhook_id TEXT PRIMARY KEY,
                    url TEXT NOT NULL,
                    secret_ref TEXT NOT NULL,
                    active BOOLEAN DEFAULT TRUE,
                    created_at TEXT
                )
                """
            )
        )
        db.commit()


def add_subscriber(webhook_id, url, secret_ref, active=True):
    with SessionLocal() as db:
        db.execute(
            text(
                """
                INSERT INTO subscribers
                (webhook_id, url, secret_ref, active, created_at)
                VALUES (:webhook_id, :url, :secret_ref, :active, :created_at)
                """
            ),
            {
                "webhook_id": webhook_id,
                "url": url,
                "secret_ref": secret_ref,
                "active": active,
                "created_at": datetime.now().isoformat(),
            },
        )
        db.commit()


def remove_subscriber(webhook_id):
    with SessionLocal() as db:
        db.execute(
            text(
                "DELETE FROM subscribers WHERE webhook_id = :webhook_id"
            ),
            {"webhook_id": webhook_id},
        )
        db.commit()


def list_subscribers():
    with SessionLocal() as db:
        result = db.execute(
            text("SELECT * FROM subscribers WHERE active = TRUE")
        )

        return result.fetchall()