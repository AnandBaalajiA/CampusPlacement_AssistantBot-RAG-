from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Updated LangChain imports
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI


# Initialize FastAPI app
app = FastAPI(title="Placement Prep Bot API")


# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response
class Query(BaseModel):
    question: str


class Response(BaseModel):
    answer: str
    sources: List[str] = []


# Global variables for RAG components
retriever = None
llm = None
embeddings = None
vectorstore = None


@app.on_event("startup")
async def startup_event():
    """Initialize RAG components on startup"""
    global retriever, llm, embeddings, vectorstore
    
    try:
        print("Loading embeddings model...")
        
        # Get API key from environment
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("ERROR: GEMINI_API_KEY not found in environment variables!")
            print("Please create a .env file with: GEMINI_API_KEY=your_key_here")
            return
        
        # Use Google Gemini embeddings (matching your original setup)
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=api_key,
            task_type="retrieval_document"
        )
        print("✓ Gemini embeddings model loaded!")
        
        print("Loading vector store...")
        vectorstore_path = "./vector_db"
        
        if os.path.exists(vectorstore_path):
            print(f"Vector store directory found at: {vectorstore_path}")
            
            try:
                print("Loading FAISS vector store...")
                vectorstore = FAISS.load_local(
                    vectorstore_path, 
                    embeddings,
                    allow_dangerous_deserialization=True
                )
                retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
                print("✓ Vector store loaded successfully!")
                
            except Exception as ve:
                print(f"Error loading vector store: {ve}")
                print("\nPlease rebuild the vector store by running:")
                print("  python rebuild_vectorstore.py")
                import traceback
                traceback.print_exc()
                return
            
            print("Loading Gemini language model...")
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=api_key,
                temperature=0.7
            )
            print("✓ Gemini language model loaded!")
            
            print("="*50)
            print("✓ RAG SYSTEM INITIALIZED SUCCESSFULLY!")
            print("="*50)
        else:
            print(f"ERROR: Vector store directory not found at {vectorstore_path}")
            print("\nPlease rebuild the vector store by running:")
            print("  python rebuild_vectorstore.py")
            
    except Exception as e:
        print(f"ERROR initializing RAG system: {e}")
        import traceback
        traceback.print_exc()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Placement Prep Bot API",
        "status": "running",
        "rag_initialized": retriever is not None and llm is not None
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "rag_system": "initialized" if retriever is not None else "not initialized",
        "components": {
            "embeddings": embeddings is not None,
            "vectorstore": vectorstore is not None,
            "retriever": retriever is not None,
            "llm": llm is not None
        }
    }


@app.post("/api/query", response_model=Response)
async def query_rag(query: Query):
    """Query the RAG system"""
    if retriever is None or llm is None:
        raise HTTPException(
            status_code=503,
            detail="RAG system not initialized. Please rebuild vector store using rebuild_vectorstore.py"
        )
    
    try:
        print(f"\n{'='*50}")
        print(f"Received query: {query.question}")
        print(f"{'='*50}")
        
        # Retrieve relevant documents with error handling
        print("Retrieving relevant documents...")
        try:
            docs = retriever.invoke(query.question)
        except (IndexError, KeyError) as e:
            print(f"Vector store index error: {e}")
            return Response(
                answer="The vector store has an error. Please ask an administrator to rebuild it using: python rebuild_vectorstore.py",
                sources=[]
            )
        
        print(f"Found {len(docs)} relevant documents")
        
        if not docs:
            return Response(
                answer="I couldn't find relevant information to answer your question in the placement feedback documents.",
                sources=[]
            )
        
        # Prepare context from documents
        context = "\n\n".join([doc.page_content for doc in docs[:3]])
        print(f"Context length: {len(context)} characters")
        
        # Create prompt
        prompt = f"""You are a helpful placement preparation assistant. Use the following context to answer the question. If you cannot answer based on the context, say so.

Context:
{context}

Question: {query.question}

Answer:"""
        
        # Generate answer with Gemini
        print("Generating answer with Gemini LLM...")
        response = llm.invoke(prompt)
        
        # Extract text from Gemini response
        if hasattr(response, 'content'):
            answer_text = response.content
        elif isinstance(response, str):
            answer_text = response
        else:
            answer_text = str(response)
        
        # Clean up the answer
        if "Answer:" in answer_text:
            answer_text = answer_text.split("Answer:")[-1].strip()
        
        # Get source snippets
        sources = [doc.page_content[:200] + "..." for doc in docs[:2]]
        
        print(f"Answer generated: {answer_text[:100]}...")
        print(f"{'='*50}\n")
        
        return Response(
            answer=answer_text,
            sources=sources
        )
        
    except Exception as e:
        print(f"ERROR processing query: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing your question: {str(e)}"
        )


@app.get("/api/test")
async def test_endpoint():
    """Test endpoint to verify API is working"""
    return {
        "message": "API is working!",
        "timestamp": "2025-10-24",
        "endpoints": [
            "/",
            "/api/health",
            "/api/query (POST)",
            "/api/test"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
