"""
Vector database service using FAISS
"""
import faiss
import numpy as np
import pickle
import os
from flask import current_app
from datetime import datetime

class VectorService:
    """Service for managing vector database operations"""
    
    def __init__(self):
        """Initialize vector service"""
        self.index_path = os.path.join(
            current_app.config['VECTOR_DB_PATH'],
            'faiss_index.bin'
        )
        self.metadata_path = os.path.join(
            current_app.config['METADATA_PATH'],
            'metadata.pkl'
        )
        
        # Load or create index
        self.index = self._load_or_create_index()
        self.metadata = self._load_metadata()
    
    def _load_or_create_index(self):
        """Load existing FAISS index or create new one"""
        if os.path.exists(self.index_path):
            return faiss.read_index(self.index_path)
        else:
            dimension = current_app.config['EMBEDDING_DIMENSION']
            return faiss.IndexFlatL2(dimension)
    
    def _load_metadata(self):
        """Load chunk metadata"""
        if os.path.exists(self.metadata_path):
            with open(self.metadata_path, 'rb') as f:
                return pickle.load(f)
        return {'chunks': [], 'documents': {}}
    
    def _save_index(self):
        """Save FAISS index to disk"""
        faiss.write_index(self.index, self.index_path)
    
    def _save_metadata(self):
        """Save metadata to disk"""
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)
    
    def add_document(self, filename, chunks, embeddings):
        """Add document chunks to vector database"""
        try:
            doc_id = f"doc_{len(self.metadata['documents']) + 1}_{int(datetime.now().timestamp())}"
            
            # Convert embeddings to numpy array
            embeddings_array = np.array(embeddings).astype('float32')
            
            # Add to FAISS index
            start_idx = self.index.ntotal
            self.index.add(embeddings_array)
            
            # Store metadata
            for i, chunk in enumerate(chunks):
                self.metadata['chunks'].append({
                    'doc_id': doc_id,
                    'document': filename,
                    'index': start_idx + i,
                    'text': chunk['text'],
                    'page': chunk.get('page', 0)
                })
            
            self.metadata['documents'][doc_id] = {
                'filename': filename,
                'chunk_count': len(chunks),
                'uploaded_at': datetime.now().isoformat()
            }
            
            # Save to disk
            self._save_index()
            self._save_metadata()
            
            current_app.logger.info(f"Added document {doc_id} with {len(chunks)} chunks")
            return doc_id
            
        except Exception as e:
            current_app.logger.error(f"Error adding document: {str(e)}")
            raise Exception(f"Failed to add document: {str(e)}")
    
    def search(self, query_embedding, top_k=5):
        """Search for similar chunks"""
        try:
            if self.index.ntotal == 0:
                return []
            
            query_vector = np.array([query_embedding]).astype('float32')
            distances, indices = self.index.search(query_vector, min(top_k, self.index.ntotal))
            
            results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(self.metadata['chunks']):
                    chunk = self.metadata['chunks'][idx].copy()
                    chunk['score'] = float(distances[0][i])
                    results.append(chunk)
            
            return results
            
        except Exception as e:
            current_app.logger.error(f"Error searching: {str(e)}")
            raise Exception(f"Search failed: {str(e)}")
    
    def list_documents(self):
        """List all documents"""
        return [
            {
                'doc_id': doc_id,
                **info
            }
            for doc_id, info in self.metadata['documents'].items()
        ]
    
    def delete_document(self, doc_id):
        """Delete a document (marks for deletion, rebuild index needed)"""
        if doc_id not in self.metadata['documents']:
            return False
        
        # Remove from metadata
        del self.metadata['documents'][doc_id]
        self.metadata['chunks'] = [
            chunk for chunk in self.metadata['chunks']
            if chunk['doc_id'] != doc_id
        ]
        
        self._save_metadata()
        current_app.logger.info(f"Deleted document {doc_id}")
        return True
