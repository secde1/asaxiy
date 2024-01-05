import smtplib
from sqlalchemy.orm import Session
from models import UserModel
from email.message import EmailMessage


class UserRepository:
    def __init__(self, sess: Session):
        self.sess: Session= sess

    def create_user(self, signup: UserModel) -> bool:
        try:
            self.sess.add(signup)
            self.sess.commit()
        except:
            return False
        return True

    def get_user(self):
        return self.sess.query(UserModel).all()

    def get_user_by_username(self, username: str):
        return self.sess.query(UserModel).filter(UserModel.username==username).first()


class SendEmailVerify:
    def sendVerify(token):
        email_address = "turgunovjamshid32@gmail.com"
        email_password = "vfyhwjjgewslyxsk"  # https://myaccount.google.com/apppasswords

        # create email
        msg = EmailMessage()
        msg['subject'] = "Email subject"
        msg['From'] = email_address
        msg['To'] = "nemon2188@gmail.com"
        msg.set_content(
            f"""\
            verify account
            http://localhost:8000/user/verify/{token}
                """,
        )
        # send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)
