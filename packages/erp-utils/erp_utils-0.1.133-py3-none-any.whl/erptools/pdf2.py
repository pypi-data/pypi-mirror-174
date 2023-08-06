import copy
from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa




### https://xhtml2pdf.readthedocs.io/en/latest/format_html.html

def save_pdf_to_S3(data, filename,storage):
    storage.save(name=filename, content=data)
    return storage.signed_url(filename)


def save_pdf(html_text, filename, storage):
    copy_data = create_pdf(html_text)
    if copy_data:
        return_data = copy.deepcopy(copy_data)
        save_pdf_to_S3(copy_data, filename, storage)
        return return_data
    return None


def create_pdf(html):
    result = BytesIO()
    # This part will create the pdf.
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return result
    return None


def render_to_pdf(template_src, context_dict={}, as_byte_io=False):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = create_pdf(html)
    if result:
        if as_byte_io:
            return result
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def open_pdf(html_text):
    return create_pdf(html_text)


def save_from_template(filename, template_src, storage, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    data = create_pdf(html)
    return save_pdf_to_S3(data, filename,storage)
