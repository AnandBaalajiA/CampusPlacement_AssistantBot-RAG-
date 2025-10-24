"""
Query/chat endpoints for RAG
"""
from flask import Blueprint, request, jsonify, current_app
from app.services.retrieval_service import RetrievalService
from app.services.generation_service import GenerationService

query_bp = Blueprint('query', __name__)

@query_bp.route('/ask', methods=['POST'])
def ask_question():
    """Process a user query and return an answer"""
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({'error': 'Query is required'}), 400
        
        user_query = data['query']
        top_k = data.get('top_k', current_app.config['TOP_K_CHUNKS'])
        
        # Retrieve relevant chunks
        retrieval_service = RetrievalService()
        relevant_chunks = retrieval_service.retrieve(user_query, top_k=top_k)
        
        if not relevant_chunks:
            return jsonify({
                'answer': 'I couldn\'t find relevant information in the uploaded documents. Please upload study materials first.',
                'sources': []
            }), 200
        
        # Generate answer
        generation_service = GenerationService()
        answer = generation_service.generate_answer(user_query, relevant_chunks)
        
        # Prepare response with sources
        sources = [
            {
                'text': chunk['text'][:200] + '...',
                'document': chunk.get('document', 'Unknown'),
                'score': float(chunk.get('score', 0))
            }
            for chunk in relevant_chunks
        ]
        
        return jsonify({
            'answer': answer,
            'sources': sources,
            'chunks_used': len(relevant_chunks)
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error processing query: {str(e)}")
        return jsonify({'error': f'Failed to process query: {str(e)}'}), 500
