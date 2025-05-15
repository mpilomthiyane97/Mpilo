import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.query_engine import CitationQueryEngine
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.core.storage.storage_context import StorageContext
from llama_index.core.settings import Settings
from dotenv import load_dotenv

# Load environment variables (your .env file should contain OPENAI_API_KEY=your-key)
load_dotenv()

# Set OpenAI API key from environment
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Set LLM and Embedding models
Settings.llm = OpenAI(model="gpt-3.5-turbo")
Settings.embed_model = OpenAIEmbedding()

# 1. Load documents (PDFs, TXTs, etc.)
print("🔍 Loading documents from /data ...")
documents = SimpleDirectoryReader("./data", recursive=True).load_data()

# 2. Ingest & index documents
print("🧠 Indexing documents ...")
pipeline = IngestionPipeline(transformations=[SentenceSplitter(), Settings.embed_model])
nodes = pipeline.run(documents=documents)

# Print vectors for each chunk
print("\n🔢 Vector embeddings for each chunk:\n")
for i, node in enumerate(nodes):
    print(f"--- Chunk {i+1} ---")
    print(f"Text: {node.text[:20]}")  #Print first 20 characters
    print(f"Vector: {node.embedding[:10]}")  # Print first 10 dimensions for readability
    print()

storage_context = StorageContext.from_defaults()
index = VectorStoreIndex(nodes, storage_context=storage_context)

# 3. Create Query Engine with citation support
query_engine = index.as_query_engine(similarity_top_k=3)

# 4. Interactive Q&A loop
print("\n✅ Mini-RAG is ready! Ask questions about your documents.")
print("Type 'exit' or 'quit' to end.\n")

while True:
    user_query = input("You: ")
    if user_query.lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break

    response = query_engine.query(user_query)

    print("\n📄 Answer:")
    print(response.response)

    print("\n📚 Sources:")
    for node in response.source_nodes:
        file_path = node.metadata.get("file_path", "Unknown")
        print(f" - {file_path} (score: {node.score:.2f})")

    print("\n" + "-" * 50)
