"""
Retrieval service for finding relevant chunks
"""
from flask import current_app
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService

class RetrievalService:
    """Service for retrieving relevant document chunks"""
    
    def __init__(self):
        """Initialize retrieval service"""
        self.embedding_service = EmbeddingService()
        self.vector_service = VectorService()
    
    def retrieve(self, query, top_k=5):
        """Retrieve most relevant chunks for query"""
        try:
            # Generate query embedding
            query_embedding = self.embedding_service.generate_query_embedding(query)
            
            # Search vector database
            results = self.vector_service.search(query_embedding, top_k=top_k)
            
            current_app.logger.info(f"Retrieved {len(results)} chunks for query")
            return results
            
        except Exception as e:
            current_app.logger.error(f"Error retrieving chunks: {str(e)}")
            raise Exception(f"Retrieval failed: {str(e)}")
