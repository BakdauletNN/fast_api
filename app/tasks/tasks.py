import smtplib
from app.tasks.broker import celery_app
from pathlib import Path
from PIL import Image
from pydantic import EmailStr
from app.tasks.email_templates import create_booking_confirm_template
from app.config import stgs


@celery_app.task()
def procces_picture(path: str):
    im_Path = Path(path)
    im = Image.open(im_Path)
    im_rszd_1000_500 = im.resize((1000, 500))
    im_rszd_200_100 = im.resize((200, 100))
    im_rszd_1000_500.save("app/static/images/resized_1000_500_{path_name}".format(path_name=im_Path.name))
    im_rszd_200_100.save("app/static/images/resized_200_100_{path_name}".format(path_name=im_Path.name))


@celery_app.task()
def send_booking_confrim_email(
        booking: dict,
        email_to: EmailStr
):
    email_to_mock = stgs.SMTP_USER
    message_content = create_booking_confirm_template(booking=booking, email_to=email_to)
    with smtplib.SMTP_SSL(stgs.SMTP_HOST, stgs.SMTP_PORT) as server:
        server.login(stgs.SMTP_USER, stgs.SMTP_PASS)
        server.send_message(message_content)

