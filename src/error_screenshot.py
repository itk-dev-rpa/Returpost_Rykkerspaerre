"""This module has functionality to send error screenshots via smtp."""

import smtplib
from email.message import EmailMessage
import os
import base64
import traceback

from PIL import ImageGrab


def send_error_screenshot(to_address: str | list[str], exception: Exception, process_name: str):
    """Creates and send an email containing the stacktrace of the given exception and a screenshot of the
    current screen.

    Args:
        to_address: The address or addresses to send the email to.
        exception: The exception to base the email on.
        process_name: The name of the process responsible for the exception.
    """
    # Create message
    msg = EmailMessage()
    msg['to'] = to_address
    msg['from'] = 'robot@friend.dk'
    msg['subject'] = f"Error screenshot: {process_name}"

    # Take screenshot
    screenshot = ImageGrab.grab()
    screenshot.save('screenshot.png')

    # Encode the screenshot as base64
    with open("screenshot.png", "rb") as img_file:
        screenshot_data = img_file.read()
        screenshot_base64 = base64.b64encode(screenshot_data).decode('utf-8')

    # Delete screenshot
    os.remove('screenshot.png')

    # Create an HTML message with the embedded image
    html_message = f"""
    <html>
    <body>
    <p>Error type: {type(exception).__name__}</p>
    <p>Error message: {exception}</p>
    <p>{traceback.format_exc()}</p>
    <img src="data:image/png;base64,{screenshot_base64}" alt="Screenshot">
    </body>
    </html>
    """

    msg.set_content("Please enable HTML to view this message.")
    msg.add_alternative(html_message, subtype='html')

    # Send message
    with smtplib.SMTP("smtp.aarhuskommune.local", 25) as smtp:
        smtp.starttls()
        smtp.send_message(msg)
