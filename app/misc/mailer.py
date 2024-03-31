from flask_mail import Message
from app import mail


class Mailer:
    '''Class for sending emails'''

    @staticmethod
    def send_email(subject: str, email: str, sender: str, msg: str):
        message = Message(
            subject,
            recipients=[email],
            sender=sender,
            body=msg
        )
        mail.send(message=message)