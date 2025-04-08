from celery import shared_task


@shared_task
def send_user_confirmation_email(send_to: str, send_to_username: str, verification_token: str):
    subject = "Verify your email"
    print("User Verification Email Sended.", subject)