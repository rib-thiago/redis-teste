from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from translate import Translator


class PDFHandler:
    def extract_text(self, pdf_path):
        pdf_reader = PdfReader(pdf_path)

        extracted_text = ""
        for page in pdf_reader.pages:
            extracted_text += page.extract_text()

        return extracted_text

    def merge_pdfs(self, pdf_paths):
        merger = PdfWriter()
        for pdf_path in pdf_paths:
            merger.append(pdf_path)

        merged_pdf = BytesIO()
        merger.write(merged_pdf)
        merged_pdf.seek(0)
        return merged_pdf

    def edit_metadata(self, pdf_path, author=None, title=None, pub_date=None):
        pdf_reader = PdfReader(pdf_path)

        if author:
            pdf_reader.Info.Author = author
        if title:
            pdf_reader.Info.Title = title
        if pub_date:
            pdf_reader.Info.ModDate = pub_date

        edited_pdf = BytesIO()
        pdf_reader.write(edited_pdf)
        edited_pdf.seek(0)
        return edited_pdf

    def generate_reference(self, pdf_path):
        pdf_reader = PdfReader(pdf_path)
        author = pdf_reader.Info.Author
        title = pdf_reader.Info.Title
        pub_date = pdf_reader.Info.ModDate

        reference = f"{author}. ({pub_date}). {title}."
        return reference

    def split_pdf(self, pdf_file, page_input):
        pdf_reader = PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)

        pdf_writer = PdfWriter()

        if ',' in page_input:
            page_nums = map(int, page_input.split(','))
            for page_num in page_nums:
                if 1 <= page_num <= num_pages:
                    pdf_writer.add_page(pdf_reader.pages[page_num - 1])
        elif '-' in page_input:
            start, end = map(int, page_input.split('-'))
            start = max(start, 1)
            end = min(end, num_pages)
            for i in range(start - 1, end):
                pdf_writer.add_page(pdf_reader.pages[i])

        output_pdf = BytesIO()
        pdf_writer.write(output_pdf)
        output_pdf.seek(0)
        return output_pdf

    def translate_text(self, pdf_path, target_language='pt'):
        translated_text = ""

        # Extract text from PDF
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            for page in pdf_reader.pages:
                translated_page_text = page.extract_text()

                # Translate each page's text
                translator = Translator(to_lang=target_language)

                # Split text into smaller chunks
                chunk_size = 500
                chunks = [translated_page_text[i:i + chunk_size]
                          for i in range(0, len(translated_page_text), chunk_size)]

                for chunk in chunks:
                    translated_chunk = translator.translate(chunk)
                    translated_text += translated_chunk

        return translated_text
