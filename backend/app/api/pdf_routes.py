"""
PDF upload and management endpoints
"""
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from app.services.pdf_service import PDFService
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService
from app.utils.validators import allowed_file

pdf_bp = Blueprint('pdf', __name__)

@pdf_bp.route('/upload', methods=['POST'])
def upload_pdf():
    """Upload and process a PDF file"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process PDF
        pdf_service = PDFService()
        text_data = pdf_service.extract_text(filepath)
        chunks = pdf_service.chunk_text(text_data)
        
        # Generate embeddings
        embedding_service = EmbeddingService()
        embeddings = embedding_service.generate_embeddings(chunks)
        
        # Store in vector database
        vector_service = VectorService()
        doc_id = vector_service.add_document(filename, chunks, embeddings)
        
        return jsonify({
            'message': 'PDF processed successfully',
            'document_id': doc_id,
            'filename': filename,
            'chunks_count': len(chunks)
        }), 201
        
    except Exception as e:
        current_app.logger.error(f"Error uploading PDF: {str(e)}")
        return jsonify({'error': f'Failed to process PDF: {str(e)}'}), 500

@pdf_bp.route('/list', methods=['GET'])
def list_pdfs():
    """List all uploaded PDF documents"""
    try:
        vector_service = VectorService()
        documents = vector_service.list_documents()
        
        return jsonify({
            'documents': documents,
            'count': len(documents)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pdf_bp.route('/delete/<doc_id>', methods=['DELETE'])
def delete_pdf(doc_id):
    """Delete a PDF document from the system"""
    try:
        vector_service = VectorService()
        success = vector_service.delete_document(doc_id)
        
        if success:
            return jsonify({'message': 'Document deleted successfully'}), 200
        else:
            return jsonify({'error': 'Document not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
