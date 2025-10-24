# Campus Placement Assistant Bot (RAG)

An AI-powered chatbot leveraging Retrieval-Augmented Generation (RAG) to assist students with campus placement queries by processing and retrieving information from company placement documents.

## 🛠️ Technology Stack

### Backend Technologies

**Core Framework**
- **FastAPI**: Modern, high-performance Python web framework for building the REST API
- **Python 3.8+**: Primary programming language

**AI & Machine Learning**
- **LangChain**: Framework for developing LLM-powered applications
- **Sentence Transformers**: State-of-the-art text embeddings for semantic search
- **FAISS (Facebook AI Similarity Search)**: Vector database for efficient similarity search and document retrieval
- **Hugging Face Transformers**: Pre-trained language models for natural language understanding

**Document Processing**
- **PyPDF2/PDFPlumber**: PDF parsing and text extraction
- **tiktoken**: Token counting and text splitting utilities

**Data & Storage**
- **Pickle**: Serialization for metadata storage
- **NumPy**: Numerical operations for vector computations

**API & Utilities**
- **Pydantic**: Data validation and settings management
- **uvicorn**: ASGI server for running FastAPI
- **python-dotenv**: Environment variable management

### Frontend Technologies

- **React.js**: Component-based UI library for building interactive user interfaces
- **JavaScript/ES6+**: Core programming language
- **Axios**: HTTP client for API communication
- **CSS3**: Styling and responsive design
- **React Hooks**: State management and lifecycle methods

### Development Tools

- **Git**: Version control system
- **Virtual Environment (venv)**: Python dependency isolation
- **npm**: JavaScript package management

## 📁 Project Directory Structure

CampusPlacement_AssistantBot-RAG/
│
├── backend/ # Backend application root
│ ├── app/ # Main application package
│ │ ├── init.py # Package initializer
│ │ │
│ │ ├── api/ # API route handlers
│ │ │ ├── health_routes.py # Health check endpoints
│ │ │ ├── pdf_routes.py # PDF upload and processing endpoints
│ │ │ └── query_routes.py # Query processing endpoints
│ │ │
│ │ ├── config/ # Configuration management
│ │ │ ├── init.py
│ │ │ ├── prompts.py # LLM prompt templates
│ │ │ └── settings.py # Application settings and environment variables
│ │ │
│ │ ├── models/ # Data models
│ │ │ └── request_models.py # Pydantic models for request/response validation
│ │ │
│ │ ├── services/ # Business logic layer
│ │ │ ├── embedding_service.py # Text embedding generation
│ │ │ ├── generation_service.py# LLM response generation
│ │ │ ├── pdf_service.py # PDF processing and text extraction
│ │ │ ├── retrieval_service.py # Document retrieval from vector store
│ │ │ └── vector_service.py # Vector database operations
│ │ │
│ │ ├── utils/ # Utility functions
│ │ │ ├── logger.py # Logging configuration
│ │ │ ├── text_splitter.py # Document chunking utilities
│ │ │ └── validators.py # Input validation functions
│ │ │
│ │ └── main.py # FastAPI application entry point
│ │
│ ├── vector_db/ # Vector database storage
│ │ ├── indexes/ # FAISS index files
│ │ │ ├── faiss_index.faiss # FAISS vector index
│ │ │ └── faiss_index.pkl # Pickled index metadata
│ │ └── metadata/ # Document metadata
│ │ └── metadata.pkl # Stored document metadata
│ │
│ ├── vector_db_old/ # Backup of previous vector database
│ │
│ ├── .gitignore # Git ignore rules for backend
│ ├── batch_upload.py # Batch PDF upload utility
│ ├── rebuild_vectorstore.py # Vector database rebuild script
│ ├── requirements.txt # Python dependencies
│ ├── run.py # Application runner
│ └── test_complete.py # Integration tests
│
├── frontend/ # Frontend React application
│ ├── public/ # Static assets
│ ├── src/ # Source code
│ │ ├── components/ # React components
│ │ ├── services/ # API service layer
│ │ ├── styles/ # CSS styling
│ │ ├── App.js # Root component
│ │ └── index.js # Application entry point
│ ├── package.json # Node.js dependencies
│ └── package-lock.json # Locked dependency versions
│
├── dataset/ # Company placement PDFs
│ ├── TCS.pdf # Company-wise placement documents
│ ├── ZOHO.pdf
│ ├── BOSCH.pdf
│ └── ... (50+ company PDFs)
│
├── .gitignore # Root-level Git ignore rules
└── README.md # Project documentation

text

## ✨ Key Features

### 1. **Intelligent Query Processing**
- Natural language understanding for placement-related questions
- Context-aware response generation
- Support for multiple query types (eligibility, salary, interview process, etc.)

### 2. **RAG-Powered Architecture**
- **Retrieval**: Searches through 50+ company placement documents
- **Augmentation**: Enriches queries with relevant context from documents
- **Generation**: Produces accurate, contextual responses using LLMs

### 3. **Vector Database Management**
- Efficient document indexing using FAISS
- Semantic similarity search for relevant information retrieval
- Fast query response times (<1 second typical)

### 4. **PDF Document Processing**
- Automated PDF text extraction
- Intelligent document chunking for optimal retrieval
- Batch upload support for multiple documents
- Metadata preservation (source, page numbers, timestamps)

### 5. **RESTful API**
- `/health`: System health monitoring
- `/upload-pdf`: Document ingestion endpoint
- `/query`: Natural language query processing
- CORS-enabled for frontend integration

### 6. **Interactive Chat Interface**
- Real-time query responses
- Clean, user-friendly React-based UI
- Conversation history tracking
- Mobile-responsive design

### 7. **Scalable Architecture**
- Modular service-based design
- Easy to add new document sources
- Extensible for additional features
- Environment-based configuration

### 8. **Data Privacy**
- Local vector database storage
- No external data transmission beyond API calls
- Configurable LLM endpoints

## 🔧 Technical Highlights

### Backend Architecture Patterns
- **Service Layer Pattern**: Separation of business logic from API routes
- **Dependency Injection**: Modular, testable service components
- **Repository Pattern**: Abstracted data access through vector service

### Vector Search Implementation
- **Embedding Model**: Sentence-BERT or similar transformer models
- **Similarity Metric**: Cosine similarity for document ranking
- **Index Type**: FAISS Flat or HNSW for fast approximate search
- **Chunk Size**: Optimized 500-1000 token chunks with overlap

### API Design
- RESTful principles
- Pydantic validation for type safety
- Async request handling for performance
- Error handling and logging middleware

---

**Built by**: Anand Baalaji A  
**Repository**: [github.com/AnandBaalajiA/CampusPlacement_AssistantBot-RAG-](https://github.com/AnandBaalajiA/CampusPlacement_AssistantBot-RAG-.git)
