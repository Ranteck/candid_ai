from crewai.tools import BaseTool
from PyPDF2 import PdfReader

class PDFReaderTool(BaseTool):
    name = "PDF Reader"
    description = "Lee archivos PDF con soporte para diferentes codificaciones"

    def _execute(self, file_path: str) -> str:
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            return f"Error al leer el PDF: {str(e)}"

class FileReadTool(BaseTool):
    name = "File Reader"
    description = "Lee archivos de texto con soporte para diferentes codificaciones"
    
    def __init__(self, root_dir: str = './data'):
        super().__init__()
        self.root_dir = root_dir

    def _execute(self, file_path: str) -> str:
        try:
            encodings = ['utf-8', 'latin-1', 'cp1252']
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        return f.read()
                except UnicodeDecodeError:
                    continue
            raise Exception(f"No se pudo leer el archivo con ninguna codificación")
        except Exception as e:
            return f"Error al leer el archivo {file_path}. Error: {str(e)}" 