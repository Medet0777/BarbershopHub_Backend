import io
from datetime import datetime, timedelta, timezone

from celery import Celery
from celery.schedules import crontab
from asgiref.sync import async_to_sync
from PIL import Image
from sqlmodel import select, and_

from src.mail import mail, create_message
from src.config import settings

c_app = Celery()
c_app.config_from_object("src.celery_config")

# Celery Beat schedule - run auto_cancel every hour
c_app.conf.beat_schedule = {
    "auto-cancel-stale-bookings": {
        "task": "src.celery_tasks.auto_cancel_stale_bookings",
        "schedule": crontab(minute=0),  # every hour at :00
    },
}


@c_app.task()
def send_email(recipients: list, subject: str, body: str):
    """Send email in background via Celery worker."""
    message = create_message(recipients, subject, body)
    async_to_sync(mail.send_message)(message)
    print(f"Email sent to {recipients}")


@c_app.task()
def compress_and_store_image(user_uid: str, image_bytes: bytes):
    """Compress image and store in PostgreSQL."""
    from src.db.session import SessionLocal
    from src.db.models import User
    from sqlmodel import select

    # 1. Log original size
    original_size = len(image_bytes)
    print(f"Original image size: {original_size / 1024:.1f} KB")

    # 2. Compress image
    img = Image.open(io.BytesIO(image_bytes))
    img = img.convert("RGB")
    img.thumbnail((800, 800))  # max 800x800

    output = io.BytesIO()
    img.save(output, format="JPEG", quality=60, optimize=True)
    compressed_bytes = output.getvalue()

    # 3. Log compressed size
    compressed_size = len(compressed_bytes)
    print(f"Compressed image size: {compressed_size / 1024:.1f} KB")
    print(f"Compression ratio: {original_size / compressed_size:.1f}x")

    # 4. Store in PostgreSQL
    async def _store():
        async with SessionLocal() as session:
            result = await session.execute(
                select(User).where(User.uid == user_uid)
            )
            user = result.scalar_one_or_none()
            if user:
                user.profile_image = compressed_bytes
                await session.commit()
                print(f"Image stored for user {user_uid}")

    async_to_sync(_store)()


@c_app.task()
def auto_cancel_stale_bookings():
    """Cancel bookings that have been Pending for more than 24 hours."""
    from src.db.session import SessionLocal
    from src.db.models import Booking

    async def _cancel():
        async with SessionLocal() as session:
            cutoff = datetime.now(timezone.utc) - timedelta(hours=24)

            result = await session.execute(
                select(Booking).where(
                    and_(
                        Booking.status == "Pending",
                        Booking.created_at < cutoff,
                    )
                )
            )
            stale_bookings = result.scalars().all()

            count = 0
            for booking in stale_bookings:
                booking.status = "Cancelled"
                count += 1

            if count > 0:
                await session.commit()

            print(f"Auto-cancelled {count} stale bookings")

    async_to_sync(_cancel)()
