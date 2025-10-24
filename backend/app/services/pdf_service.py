"""
PDF extraction and processing service
"""
import fitz  # PyMuPDF
from flask import current_app
from app.utils.text_splitter import chunk_text

class PDFService:
    """Service for handling PDF operations"""
    
    def extract_text(self, pdf_path):
        """Extract text from PDF file"""
        try:
            document = fitz.open(pdf_path)
            pdf_text = {}
            
            for page_num in range(document.page_count):
                page = document.load_page(page_num)
                text = page.get_text()
                
                if text.strip():  # Only add non-empty pages
                    pdf_text[page_num + 1] = text
            
            document.close()
            
            current_app.logger.info(f"Extracted text from {len(pdf_text)} pages")
            return pdf_text
            
        except Exception as e:
            current_app.logger.error(f"Error extracting PDF text: {str(e)}")
            raise Exception(f"Failed to extract PDF: {str(e)}")
    
    def chunk_text(self, pdf_text):
        """Convert PDF text to chunks"""
        all_chunks = []
        
        for page_num, text in pdf_text.items():
            if not text.strip():
                continue
            
            page_chunks = chunk_text(text)
            
            # Add metadata to each chunk
            for chunk in page_chunks:
                all_chunks.append({
                    'text': chunk,
                    'page': page_num,
                    'length': len(chunk)
                })
        
        current_app.logger.info(f"Created {len(all_chunks)} chunks")
        return all_chunks
