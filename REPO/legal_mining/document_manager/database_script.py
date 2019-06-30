"""
Script to load by 'python3 manage.py shell < document_manager/database_script.py'
to add full text and slug to database.

Retrieves Text from TXT and PDF. Uses filepath from database. So files must be
located in "../Testing/Content" relative to manage.py.

"""

from PyPDF2 import PdfFileReader
from django.utils.text import slugify
from document_manager import models as m


def pdf_as_text(file):
    text = ""
    pdf = PdfFileReader(open(file, "rb"))
    for i in range(0, pdf.getNumPages()):
        text += pdf.getPage(i).extractText() + " \n"
    return text


def __get_txt_data(path):
    return open(path, "r", encoding="UTF-8").read()


def __get_pdf_data(path):
    return pdf_as_text(path)


def save_text_to_db():
    documents = m.Documentstorage.objects.filter(filepath__endswith='.txt')
    i = 0
    for doc in documents:
            i += 1
            if doc.filepath.endswith('.txt'):
                doc.text = __get_txt_data(doc.filepath)
            if doc.filepath.endswith('.pdf'):
                try:
                    doc.text = __get_pdf_data(doc.filepath)
                except Exception:
                    print ("ignoring Error")
            doc.slug = slugify(doc.title)
            doc.save()
            print(i)


def save_slug_to_db():
    documents = m.Documentstorage.objects.filter(filepath__endswith='.pdf')
    i = 0
    for doc in documents:
            doc.slug = slugify(doc.title)
            doc.save()
            print(i)


#save_text_to_db()
save_slug_to_db()
