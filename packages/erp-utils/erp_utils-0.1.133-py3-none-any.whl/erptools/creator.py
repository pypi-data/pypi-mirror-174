import json
import os
import re
import time

from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.template.loader import render_to_string

from erptools import pdf2, email, sqs


class DocumentCreator:
    email_templates = {}
    pdf_templates = {}

    def __init__(self, instance, media_storage):
        self._instance = instance
        self._media_storage = media_storage()
        self._context_object = instance.get_context_instance()

    def _get_context(self, value_list, context=None):
        if context is None:
            context = {}
        return self._context_object.get_context(value_list, context=context)

    def email(self, title, email_sender, recipients, context=None, request=None):
        if context is None:
            context = {}
        template_type = 'email'
        subject = self.email_subject(title)
        txt_text = self.render_template(request, template_type, title, context, text_only=True)
        html_text = self.render_template(request, template_type, title, context, text_only=False)
        attachments = []

        # dynamic attachments
        for pdf_template_name in self.email_templates[title]['attachments']:
            self.save_pdf(pdf_template_name, context)
            path = self.get_pdf_path(pdf_template_name)
            filename = self.get_pdf_filename(pdf_template_name)
            attachments.append(
                {
                    'data': self._media_storage.open(path.strip(self._media_storage.location)),
                    'filename': filename
                }
            )

        # Static Attachments

        for static_file in self.get_context_value(f"static_attachment_{title}".replace(" ", "_").lower()):
            attachments.append(
                {
                    'data': self._media_storage.open(static_file["path"].strip(self._media_storage.location)),
                    'filename': static_file["filename"]
                }
            )



        email.send_mail(
            email_sender, recipients, subject, txt_text, html_text, attachments
        )

    def pdf_exists(self, title):
        path = self.get_pdf_path(title)
        return self._media_storage.exists(path)

    def view_html(self, request, title, context=None):
        if context is None:
            context = {}
        template_type = 'email'
        # template_values = self.get_template_values(template_type, title)
        html_text = self.render_template(request, template_type, title, context, text_only=False)
        return HttpResponse(html_text)

    def view_pdf(self, request, title, context=None, resave=False):
        """
        :param request:
        :param title:
        :param context:
        :return: HttpResponse Object containing pdf
        """
        if context is None:
            context = {}
        if not self.pdf_exists(title) or resave:
            self.save_pdf(title, context)
        return self.render_pdf(title)

    def get_pdf_filename(self, pdf_template_name):
        value = self.pdf_templates[pdf_template_name]['context_name']
        return self._get_context([value]).get(value)

    def get_pdf_path(self, pdf_template_name):
        value = self.pdf_templates[pdf_template_name]['context_path']
        return self._get_context([value]).get(value)

    def get_pdf_relative_path(self, pdf_template_name):
        absolute = self.get_pdf_path(pdf_template_name)
        quote_dir = self.get_context_value('quote_directory')
        return absolute[len(quote_dir) + 1:]

    def get_attachement_filenames(self, request, title, context, resave=False):
        file_list = []
        pdf_template_names = self.email_templates[title]['attachments']

        for pdf_template_name in pdf_template_names:
            file_list.append(self.get_pdf_relative_path(pdf_template_name))
            if resave or not self.pdf_exists(pdf_template_name):
                print("Creating PDF")
                self.save_pdf(pdf_template_name, context)
        return file_list

    def email_endpoint_data(self, request, template_type, title, context=None, text_only=True, resave=False):
        if context is None:
            context = {}
        attachments = self.get_attachement_filenames(request, title, context, resave=resave)

        recipients = []
        for recipient in self.email_templates[title]['recipients']:
            if recipient == 'client':
                recipients.extend(self.quote_recipients())
            elif recipient == 'manufacturer':
                recipients.append(self._context_object.get_value('manufacturer_email'))


        return {
            "html": self.render_template(request, template_type, title, context, text_only),
            "subject": self.email_subject(title),
            "recipients": recipients,
            "s3_attachments": attachments

        }

    @staticmethod
    def _html_to_text(html):
        soup = BeautifulSoup(html)
        # remove extra White space
        text = re.sub(' +', ' ', soup.get_text('\n'))
        text = re.sub('\n\n+', '\n\n', text)
        return text

    def get_template_values(self, template_type, title):
        if template_type == 'email':
            templates = self.email_templates
        elif template_type == 'pdf':
            templates = self.pdf_templates

        else:
            raise Exception("template_type must be either 'email' or 'pdf'")
        return templates[title]

    def render_template(self, request, template_type, title, context=None, text_only=True):

        if context is None:
            context = {}
        template = self.get_template_values(template_type, title)
        email_template = template['template_name']
        value_list = template['value_list']
        context['title'] = template['title']
        html = render_to_string(email_template, self._get_context(value_list, context), request)
        if text_only:
            return self._html_to_text(html)
        return html

    def save_pdf(self, title, context=None):
        if context is None:
            context = {}
        template = self.get_template_values('pdf', title)
        template_src = template['template_name']
        value_list = template['value_list']
        context['title'] = template['title']
        context['reference'] = self._context_object.get_value(template['reference'])
        context['reference_number'] = self._context_object.get_value(template['reference'])
        context = self._get_context(value_list, context)
        path = self._context_object.get_value(template['context_path'])
        print(
            f'''
            saving pdf: {title}
            to path: {path}
            from template: {template_src}
            with values:
            {context}
            '''
        )
        pdf2.save_from_template(path, template_src, self._media_storage, context_dict=context)
        return path

    def render_pdf(self, title):
        path = self.get_pdf_path(title)
        file = self._media_storage.open(path.strip(self._media_storage.location))
        return HttpResponse(file, content_type='application/pdf')

    def email_subject(self, title):
        template_values = self.get_template_values('email', title)
        subject = template_values['subject']
        reference = template_values['reference']
        context = self._get_context([reference])
        reference_value = context.get(reference, '')
        return subject.format(reference=reference_value)

    def quote_recipients(self):
        client = self._context_object.get_value('client')
        return [client.email]

    def get_context_value(self, value):
        return self._instance.get_context_value(value)

    def get_recipients(self, template_type):
        template_values = self.get_template_values('email', template_type)
        recipients = []
        for r in template_values['recipients']:
            if r == 'sales_rep':
                recipients.append(self.get_context_value("sales_rep_email"))
            elif r == 'client':
                recipients.append(self.get_context_value("client_email"))
        return recipients

    def sqs_auto_save_document(self, template_type):
        template_values = self.get_template_values('pdf', template_type)
        reference_object = template_values['reference_object']
        reference = self.get_context_value(template_values["reference"])
        message_body = json.dumps(
            {
                "job": "save_pdf",
                "data": {
                    "api_name": template_values["api_name"],
                    "document_type": template_type,
                    "reference": reference,
                    "reference_object": reference_object,
                }
            }
        )
        queue_name = os.environ.get("ERP_WORKER")
        message_deduplication_id = f'{template_type}-{reference}-pdf-saved-time-{int(time.mktime(time.gmtime()))}'
        print(message_deduplication_id)

        sqs.send_message(message_body, message_deduplication_id, queue_name,
                         message_group_id=f'email', message_attributes=None)
        print(f"SQS Message SENT: {message_body}")

    def sqs_auto_email(self, template_type):

        template_values = self.get_template_values('email', template_type)
        reference_object = template_values['reference_object']
        recipient = self.get_recipients(template_type)
        email_sender = "no_reply@thefurnitureguys.ca"
        reference = self.get_context_value(template_values["reference"])
        message_body = json.dumps(
            {
                "job": "email",
                "data": {
                    "api_name": template_values["api_name"],
                    "email_type": template_type,
                    "reference": reference,
                    "reference_object": reference_object,
                    "recipients": recipient,  # customer email
                    "email_sender": email_sender,
                }
            }
        )
        # todo: change to env variable
        queue_name = os.environ.get("ERP_WORKER")
        message_deduplication_id = re.sub(r'\W+', '', f'{template_type}-{reference}-{str(recipient)}')

        sqs.send_message(message_body, message_deduplication_id, queue_name,
                         message_group_id=f'email', message_attributes=None)
        print(f"SQS Message SENT: {message_body}")

    def auto_email(self, template_type):
        recipient = self.get_recipients(template_type)
        email_sender = "no_reply@thefurnitureguys.ca"
        self.email(template_type, email_sender, recipient)
