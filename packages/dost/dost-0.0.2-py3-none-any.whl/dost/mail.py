""" 
Mail module for dost. This module contains functions for sending emails.

Examples:  
    >>> from dost import mail
    >>> mail.send_gmail_using_app_password('abcd','abcd','abcd@abc.com','abcd','abcd','abc.pdf')


This module contains the following functions:

- `send_gmail_using_app_password(sender_email, sender_password, receiver_email, subject, body, attachment_path)`: Send an email using a gmail account and an app password.

"""


from pathlib import WindowsPath
from typing import List, Union
import os
from dost.helpers import dostify


@dostify(errors=[(ValueError, '')])
def send_gmail_using_app_password(gmail_username: str, gmail_app_password: str, to_email_id: Union[str, List[str]], subject: str, message: str, attachment_path: Union[str, List[str], WindowsPath, List[WindowsPath]] = "") -> None:
    """Send email using gmail app password
    Args:
        gmail_username (str): Gmail username
        gmail_app_password (str): Gmail app password
        to_email_id (Union[str, List[str]]): To email id
        subject (str): Subject of the email
        message (str): Message of the email
        attachment_path (Union[str, List(str)(optional), WindowsPath, List[WindowsPath]]): Attachment path
    Examples:
        >>> send_gmail_using_app_password('abcd','abcd','abcd@abc.com','abcd','abcd','abc.pdf')

    """
    # Import Section
    import os

    from pathlib import Path
    import yagmail

    # Validation Section
    if not gmail_username:
        raise ValueError(f'Gmail username cannot be empty')

    if not gmail_app_password:
        raise ValueError(f'Gmail app password cannot be empty')

    if not to_email_id:
        raise ValueError(f'To email id cannot be empty')

    if not subject:
        raise ValueError(f'Subject cannot be empty')

    if not message:
        raise ValueError(f'Message cannot be empty')

    yag = yagmail.SMTP(gmail_username, gmail_app_password)

    if attachment_path:
        yag.send(to_email_id, subject, message,
                 attachments=attachment_path)
    else:
        yag.send(to=to_email_id, subject=subject, contents=message)

        # Alternatively, with a simple one-liner:
        # yagmail.SMTP(gmail_username).send(to_email_id, subject, message)
