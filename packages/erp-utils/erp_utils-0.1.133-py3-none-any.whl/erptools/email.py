import boto3
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from django.template.loader import render_to_string

from erptools import pdf2

CONFIGURATION_SET = "ConfigSet"
AWS_REGION = "ca-central-1"
CHARSET = "UTF-8"


def create_multipart_message(
        sender: str, recipients: list, title: str, text: str = None, html: str = None, attachments: list = None) \
        -> MIMEMultipart:
    """
    Creates a MIME multipart message object.
    Uses only the Python `email` standard library.
    Emails, both sender and recipients, can be just the email string or have the format 'The Name <the_email@host.com>'.

    :param sender: The sender.
    :param recipients: List of recipients. Needs to be a list, even if only one recipient.
    :param title: The title of the email.
    :param text: The text version of the email body (optional).
    :param html: The html version of the email body (optional).
    :param attachments: List of files to attach in the email.
    :return: A `MIMEMultipart` to be used to send the email.
    """
    multipart_content_subtype = 'alternative' if text and html else 'mixed'
    msg = MIMEMultipart(multipart_content_subtype)
    msg['Subject'] = title
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    # Record the MIME types of both parts - text/plain and text/html.
    # According to RFC 2046, the last part of a multipart message, in this case the HTML message, is best and preferred.
    if text:
        part = MIMEText(text, 'plain')
        msg.attach(part)
    if html:
        part = MIMEText(html, 'html')
        msg.attach(part)

    # Add attachments
    container = MIMEMultipart('mixed')
    # alternative = MIMEMultipart('alternative')
    # container.attach(alternative)

    for attachment in attachments or []:
        f = attachment['data']
        f.seek(0)
        part = MIMEApplication(f.read())
        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment['filename']))
        container.attach(part)

    msg.attach(container)
    return msg


def send_mail(
        sender: str, recipients: list, title: str, text: str = 'None', html: str = None,
        attachments: list = None) -> dict:
    """
    Send email to recipients. Sends one mail to all recipients.
    The sender needs to be a verified email in SES.
    """
    msg = create_multipart_message(sender, recipients, title, text, html, attachments)
    ses_client = boto3.client('ses', region_name=os.environ.get('AWS_SES_REGION_NAME'))

    responses = []
    sales_email = os.environ.get('SALES_EMAIL', default='')
    if sales_email:
        recipients.append(sales_email)
    else:
        responses.append({'email': 'sales email', 'error': 'sales email not found'})
    for recipient in recipients:
        try:
            responses.append(
                ses_client.send_raw_email(
                    Source=sender,
                    Destinations=[recipient],
                    RawMessage={'Data': msg.as_string()})
            )
        except Exception as e:
            responses.append({'email': recipient, 'error': e})
    return {'responses': str(responses)}


def compose_email(sender, recipients, subject, context, email_template, txt_template, pdf_template=None,
                  filename_prefix=None):
    # create html data

    html_content = render_to_string(email_template, context)
    txt_content = render_to_string(txt_template, context)

    attachments = []
    if pdf_template:
        pdf_html_content = render_to_string(pdf_template, context)
        attachments.append(
            {'data': pdf2.open_pdf(pdf_html_content), 'filename': f'{filename_prefix}.pdf'}
        )
    return send_mail(sender, recipients, subject, txt_content, html_content, attachments)