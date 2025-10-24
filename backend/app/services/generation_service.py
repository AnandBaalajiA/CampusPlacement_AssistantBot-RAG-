"""
Text generation service using Gemini
"""
from google import genai
from google.genai import types
from flask import current_app
from app.config.prompts import create_rag_prompt

class GenerationService:
    """Service for generating answers using Gemini"""
    
    def __init__(self):
        """Initialize Gemini client"""
        self.client = genai.Client(
            api_key=current_app.config['GEMINI_API_KEY']
        )
        self.model = current_app.config['GENERATION_MODEL']
    
    def generate_answer(self, query, relevant_chunks):
        """Generate answer based on retrieved context"""
        try:
            # Combine chunks into context
            context = "\n\n".join([
                f"[From {chunk.get('document', 'Unknown')} - Page {chunk.get('page', 'N/A')}]\n{chunk['text']}"
                for chunk in relevant_chunks
            ])
            
            # Create prompt
            prompt = create_rag_prompt(context, query)
            
            # Generate response
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=current_app.config['TEMPERATURE'],
                    max_output_tokens=current_app.config['MAX_OUTPUT_TOKENS']
                )
            )
            
            answer = response.text
            current_app.logger.info("Generated answer successfully")
            return answer
            
        except Exception as e:
            current_app.logger.error(f"Error generating answer: {str(e)}")
            raise Exception(f"Answer generation failed: {str(e)}")
