from email.message import EmailMessage
from pydantic import EmailStr
from app.config import stgs


def create_booking_confirm_template(
        booking: dict,
        email_to: EmailStr,
):
    email = EmailMessage()
    email["Subject"] = "Confurm Booking"
    email["From"] = stgs.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
             <h1> Please, confirm booking <h1> 
             You booked hotel from {booking["date_from"]} to {booking["date_to"]}      
        """,
        subtype="html"
    )
    return email