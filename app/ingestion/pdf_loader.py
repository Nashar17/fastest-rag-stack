from pathlib import Path
from pypdf import PdfReader


class PDFLoader:
    """
    Responsible for loading and extracting text from PDF files.
    """

    def __init__(self, pdf_directory: str):
        self.pdf_directory = Path(pdf_directory)

    def load_pdfs(self):
        """
        Load all PDFs from the directory.
        """
        pdf_files = list(self.pdf_directory.glob("*.pdf"))
        return pdf_files

    def extract_text(self):
        """
        Extract text from all PDFs.
        """
        documents = []

        for pdf_file in self.load_pdfs():
            reader = PdfReader(pdf_file)

            text = ""
            for page in reader.pages:
                text += page.extract_text()

            documents.append({
                "file_name": pdf_file.name,
                "content": text
            })

        return documents