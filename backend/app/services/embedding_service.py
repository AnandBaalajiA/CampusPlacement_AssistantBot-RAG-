"""
Gemini embedding generation service
"""
from google import genai
from google.genai import types
from flask import current_app
import time

class EmbeddingService:
    """Service for generating embeddings using Gemini"""
    
    def __init__(self):
        """Initialize Gemini client"""
        self.client = genai.Client(
            api_key=current_app.config['GEMINI_API_KEY']
        )
        self.model = current_app.config['EMBEDDING_MODEL']
        self.dimension = current_app.config['EMBEDDING_DIMENSION']
    
    def generate_embeddings(self, chunks, task_type="RETRIEVAL_DOCUMENT"):
        """Generate embeddings for text chunks"""
        try:
            texts = [chunk['text'] for chunk in chunks]
            
            # Generate embeddings in batches
            batch_size = 100
            all_embeddings = []
            
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i + batch_size]
                
                # Updated for text-embedding-004
                result = self.client.models.embed_content(
                    model=self.model,
                    contents=batch_texts,
                    config=types.EmbedContentConfig(
                        task_type=task_type,
                        output_dimensionality=self.dimension
                    )
                )
                
                batch_embeddings = [e.values for e in result.embeddings]
                all_embeddings.extend(batch_embeddings)
                
                if i + batch_size < len(texts):
                    time.sleep(0.5)
            
            current_app.logger.info(f"Generated {len(all_embeddings)} embeddings")
            return all_embeddings
            
        except Exception as e:
            current_app.logger.error(f"Error generating embeddings: {str(e)}")
            raise Exception(f"Failed to generate embeddings: {str(e)}")
    
    def generate_query_embedding(self, query):
        """Generate embedding for a query"""
        try:
            result = self.client.models.embed_content(
                model=self.model,
                contents=query,
                config=types.EmbedContentConfig(
                    task_type="RETRIEVAL_QUERY",
                    output_dimensionality=self.dimension
                )
            )
            return result.embeddings[0].values
            
        except Exception as e:
            current_app.logger.error(f"Error generating query embedding: {str(e)}")
            raise Exception(f"Failed to generate query embedding: {str(e)}")
