"""Declara, a library for generating Boreas declaration forms"""

__version__ = "1.0.4"

import base64
from collections import namedtuple
from datetime import date, timedelta
from importlib import resources
from io import BytesIO
from os import environ

import PIL
import requests
import yagmail
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


class Declara:
    Row = namedtuple("Row", ["description", "amount"])
    Attachment = namedtuple("Attachment", ["buffer", "is_image", "is_pdf"])

    def __init__(self):
        self.reader = PdfReader(resources.open_binary("declara", "Declaratieformulier_v3F.pdf"))
        self.writer = PdfWriter()

        page = self.reader.pages[0]
        self.writer.add_page(page)

        self.rows = []
        self.attachments = []

        self.name = ""
        self.iban = ""

    def get_description(self, idx):
        try:
            return self.rows[idx].description
        except IndexError:
            return ""

    def get_amount(self, idx):
        try:
            return f"{self.rows[idx].amount:.2f}".replace(".", ",")
        except IndexError:
            return ""

    def send_email(
        self,
        extra_addresses=[],
        only_extra_addresses=False,
        custom_date=None,
    ):
        _date = custom_date

        if not _date:
            _date = date.today()

        pdf, ds = self.produce(_date)

        expiry_date = _date + timedelta(days=56)

        while expiry_date.day != _date.day:
            expiry_date += timedelta(days=1)

        yag = yagmail.SMTP(
            user=environ["SMTP_USERNAME"],
            password=environ["SMTP_PASSWORD"],
            host=environ["SMTP_HOST"],
            port=int(environ["SMTP_PORT"] if "SMTP_PORT" in environ else 587),
            smtp_ssl=True,
        )

        # Get the joke?!
        r = requests.get(
            "https://v2.jokeapi.dev/joke/Miscellaneous,Dark,Pun?blacklistFlags=nsfw,racist,sexist,explicit&format=txt&type=single"
        )

        # Compute total
        total = 0
        for row in self.rows:
            total += float(row.amount)

        body = resources.read_text("declara", "default_email_body.txt")

        if "DECLARA_EMAIL_BODY_B64" in environ:
            body = base64.b64decode(environ["DECLARA_EMAIL_BODY_B64"]).decode("utf-8")

        body = (
            body.replace("[EXPIRY]", expiry_date.strftime("%d-%m-%Y"))
            .replace("[NAME]", self.name)
            .replace("[TOTAL]", f"€{total:.2f}".replace(".", ","))
            .replace("[JOKE]", "\n".join(map(lambda s: ">  " + s, r.content.decode("utf-8").splitlines())))
        )

        pdf.name = f"Declaratie {ds[2]}-{ds[1]}-{ds[0]}.pdf"

        subject = environ["DECLARA_EMAIL_SUBJECT"] if "DECLARA_EMAIL_SUBJECT" in environ else "Declaratie"

        if only_extra_addresses:
            to = extra_addresses
            cc = None
        else:
            to = environ["SMTP_DEFAULT_RECIPIENT"]
            cc = extra_addresses

        yag.send(to=to, cc=cc, subject=subject, contents=body, attachments=pdf)

    def produce(self, _date):
        ds = _date.isoformat().split("-")

        year = ds[0]
        month = ds[1]
        day = ds[2]

        total = 0
        for row in self.rows:
            total += float(row.amount)

        data = {
            "Date-dd": day,
            "date-mm": month,
            "date-jjjj": year,
            "name": self.name,
            "iban": self.iban,
            "omschr1": self.get_description(0),
            "Text1": self.get_description(1),
            "Text2": self.get_description(2),
            "Text3": self.get_description(3),
            "Text4": self.get_description(4),
            "Text5": self.get_description(5),
            "Text6": self.get_description(6),
            "Text7": self.get_description(7),
            "bedrag1": self.get_amount(0),
            "Text15": self.get_amount(1),
            "Text16": self.get_amount(2),
            "Text17": self.get_amount(3),
            "Text18": self.get_amount(4),
            "Text19": self.get_amount(5),
            "Text20": self.get_amount(6),
            "Text21": self.get_amount(7),
            "Text22": f"{total:.2f}".replace(".", ","),
        }

        self.writer.update_page_form_field_values(self.writer.pages[0], data)

        for attachment in self.attachments:
            if type(attachment) == str:
                r = requests.get(attachment)
                f = BytesIO(r.content)
                is_image = attachment.split(".")[-1].lower() in ["png", "jpeg", "jpg"]
                is_pdf = attachment.lower().endswith(".pdf")
            elif isinstance(attachment, Declara.Attachment):
                is_image = attachment.is_image
                is_pdf = attachment.is_pdf
                f = attachment.buffer
            else:
                continue

            if is_image:
                page = self.writer.add_blank_page(
                    self.writer.pages[0].mediaBox.width,
                    self.writer.pages[0].mediaBox.height,
                )

                buf = BytesIO()
                can = canvas.Canvas(buf)
                img = PIL.Image.open(f)
                size = img.size
                max_w = 600
                max_h = 900
                if size[0] > max_w:
                    size = (max_w, size[1] / size[0] * max_w)

                if size[1] > max_h:
                    size = (size[0] / size[1] * max_h, max_h)

                if size != img.size:
                    img.thumbnail(size)

                can.drawImage(
                    ImageReader(img),
                    100,
                    75,
                    width=400,
                    preserveAspectRatio=True,
                    anchor="sw",
                )
                can.save()
                buf.seek(0)

                new_pdf = PdfReader(buf)
                page.mergePage(new_pdf.getPage(0))
            elif is_pdf:
                pdf = PdfReader(f)
                for i in range(pdf.getNumPages()):
                    self.writer.add_page(pdf.getPage(i))

        output_buf = BytesIO()
        self.writer.write(output_buf)
        output_buf.seek(0)
        return output_buf, ds
