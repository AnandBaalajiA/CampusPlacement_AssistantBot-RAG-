from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv

load_dotenv()

print("="*50)
print("VECTOR STORE REBUILD SCRIPT")
print("="*50)

# Initialize embeddings
print("\n1. Loading Gemini embeddings model...")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env file!")
    exit(1)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=api_key,
    task_type="retrieval_document"
)
print("   ✓ Embeddings loaded!")

# Load PDFs
print("\n2. Loading PDF documents...")
pdf_folder = "./data"  # Change this if your PDFs are elsewhere

if not os.path.exists(pdf_folder):
    print(f"   ERROR: PDF folder '{pdf_folder}' not found!")
    print(f"   Please create the folder and add your PDF files there.")
    exit(1)

# List PDF files
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
if len(pdf_files) == 0:
    print(f"   ERROR: No PDF files found in '{pdf_folder}'!")
    print(f"   Please add your placement feedback PDF files to this folder.")
    exit(1)

print(f"   Found {len(pdf_files)} PDF file(s):")
for pdf in pdf_files:
    print(f"     - {pdf}")

loader = DirectoryLoader(
    pdf_folder,
    glob="**/*.pdf",
    loader_cls=PyPDFLoader,
    show_progress=True
)

documents = loader.load()
print(f"   ✓ Loaded {len(documents)} pages from PDFs")

# Split documents
print("\n3. Splitting documents into chunks...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)

chunks = text_splitter.split_documents(documents)
print(f"   ✓ Created {len(chunks)} text chunks")

# Create FAISS vector store
print("\n4. Creating FAISS vector store...")
print("   (This may take a few minutes depending on the number of documents)")
vectorstore = FAISS.from_documents(chunks, embeddings)

# Save vector store
output_path = "./vector_db"
print(f"\n5. Saving vector store to '{output_path}'...")

# Remove old vector store if exists
if os.path.exists(output_path):
    import shutil
    print(f"   Removing old vector store...")
    shutil.rmtree(output_path)

vectorstore.save_local(output_path)

print("\n" + "="*50)
print("✓ VECTOR STORE CREATED SUCCESSFULLY!")
print("="*50)
print(f"\nVector store saved to: {output_path}")
print("\nNext steps:")
print("1. Restart your FastAPI server: uvicorn app.main:app --reload")
print("2. Test your chatbot at http://localhost:3000")
print("="*50)
