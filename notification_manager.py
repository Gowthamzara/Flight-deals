import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


class NotificationManager:
    """Sends email alerts when a cheaper flight is found."""

    def __init__(self):
        self._sender = os.environ["EMAIL_ADDRESS"]
        self._password = os.environ["EMAIL_PASSWORD"]  # Gmail: use an App Password
        self._recipient = os.getenv("ALERT_TO_EMAIL", self._sender)
        self._smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self._smtp_port = int(os.getenv("SMTP_PORT", "587"))

    def send_email(self, subject, body):
        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = self._sender
        message["To"] = self._recipient
        message.set_content(body)

        try:
            with smtplib.SMTP(self._smtp_host, self._smtp_port, timeout=30) as connection:
                connection.starttls()
                connection.login(self._sender, self._password)
                connection.send_message(message)
            print(f"Email alert sent to {self._recipient}")
            return True
        except (smtplib.SMTPException, OSError) as error:
            # Don't crash the whole run just because one email failed
            print(f"Could not send email: {error}")
            return False

    def send_deal_alert(self, city, flight, previous_price):
        subject = f"Flight deal: {flight.origin_airport} to {city} for GBP {flight.price}"
        previous = f"GBP {previous_price}" if previous_price != float("inf") else "no previous price"
        body = (
            f"Low price alert! Only GBP {flight.price} to fly "
            f"from {flight.origin_airport} to {flight.destination_airport} ({city}).\n\n"
            f"Departure: {flight.out_date}\n"
            f"Return:    {flight.return_date}\n"
            f"Stops:     {flight.stops}\n"
            f"Previous lowest price: {previous}\n\n"
            f"Search it on Google Flights: https://www.google.com/travel/flights\n"
        )
        return self.send_email(subject, body)
