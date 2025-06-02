#Load environment variables from .env (e.g., OpenAI API key)
import os
from dotenv import load_dotenv

#Import core components from LlamaIndex
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    KeywordTableIndex,
    StorageContext,
    Settings,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.callbacks import CallbackManager, TokenCountingHandler
import tiktoken
import pandas as pd

#Load environment variables and set OpenAI API key
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

#Setup callback for token counting (used for cost monitoring)
token_counter = TokenCountingHandler(
    tokenizer=tiktoken.encoding_for_model("gpt-3.5-turbo").encode
)
callback_manager = CallbackManager([token_counter])

#Configure LlamaIndex global settings
Settings.llm = OpenAI(model="gpt-3.5-turbo")
Settings.embed_model = OpenAIEmbedding()
Settings.callback_manager = callback_manager

#Load local documents from /data directory
print("🔍 Loading documents ...")
documents = SimpleDirectoryReader("./data", recursive=True).load_data()

# Here I split docs into chunks and embed them for retrieval
print("🧠 Indexing documents ...")
pipeline = IngestionPipeline(transformations=[SentenceSplitter(), Settings.embed_model])
nodes = pipeline.run(documents=documents) #Run the ingestion pipeline: splits documents into sentences, generates 
#embeddings for each chunk(node)

#  Store vector and keyword indexes in memory
storage_context = StorageContext.from_defaults()
vector_index = VectorStoreIndex(nodes, storage_context=storage_context) # Create a vector index for semantic search 
#using embeddings(supports similarity-based retrieval)
keyword_index = KeywordTableIndex(nodes) #Create a keyword table index for keyword-based search (supports exact term matching)

#Setup query engines for both indexes
vector_engine = vector_index.as_query_engine(similarity_top_k=3) #Create a query engine from the vector index that retrieves 
#the top 3 most semantically similar nodes
keyword_engine = keyword_index.as_query_engine(similarity_top_k=3)#Create a query engine from the keyword index that retrieves 
#the top 3 most relevant keyword matches

print("\n✅ Hybrid Mini-RAG is ready! Type your question below.\n")

#Track token usage + costs
csv_log = []

# 💬 Interactive loop for user queries
while True:
    user_query = input("You: ")
    if user_query.lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break

    # 🔍 Run both keyword and vector-based retrieval
    keyword_response = keyword_engine.query(user_query)
    vector_response = vector_engine.query(user_query)

    # 🧩 Combine answers from both retrieval engines
    combined_answer = (
        f"[Keyword Match]\n{keyword_response.response}\n\n"
        f"[Vector Match]\n{vector_response.response}"
    )

    print("\n📄 Answer:\n", combined_answer)

    #Show sources for keyword-based match
    print("\n📚 Sources for Keyword Match:")
    for node in getattr(keyword_response, "source_nodes", []):
        file_path = node.metadata.get("file_path", "Unknown")
        score = getattr(node, "score", None)
        score_display = f"{score:.2f}" if score is not None else "N/A"
        print(f" - {file_path} (score: {score_display})")

    #Show sources for vector-based match
    print("\n📚 Sources for Vector Match:")
    for node in getattr(vector_response, "source_nodes", []):
        file_path = node.metadata.get("file_path", "Unknown")
        score = getattr(node, "score", None)
        score_display = f"{score:.2f}" if score is not None else "N/A"
        print(f" - {file_path} (score: {score_display})")

    #Token usage tracking
    embedding_tokens = token_counter.total_embedding_token_count
    prompt_tokens = token_counter.prompt_llm_token_count
    completion_tokens = token_counter.completion_llm_token_count
    total_llm_tokens = token_counter.total_llm_token_count

    #Pricing based on OpenAI's rates (per 1K tokens)
    EMBEDDING_COST_PER_1K = 0.0001
    PROMPT_COST_PER_1K = 0.0015
    COMPLETION_COST_PER_1K = 0.002

    #Calculate actual cost
    embedding_cost = (embedding_tokens / 1000) * EMBEDDING_COST_PER_1K
    prompt_cost = (prompt_tokens / 1000) * PROMPT_COST_PER_1K
    completion_cost = (completion_tokens / 1000) * COMPLETION_COST_PER_1K
    total_cost = embedding_cost + prompt_cost + completion_cost

    #Log query, tokens, and cost to memory
    log_entry = {
        "query": user_query,
        "embedding_tokens": embedding_tokens,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_llm_tokens": total_llm_tokens,
        "embedding_cost_usd": round(embedding_cost, 6),
        "prompt_cost_usd": round(prompt_cost, 6),
        "completion_cost_usd": round(completion_cost, 6),
        "total_cost_usd": round(total_cost, 6),
    }
    csv_log.append(log_entry)

    print("\n📊 Token usage logged.")
    print(f"💰 Total cost on this query: ${total_cost:.6f}")
    print("-" * 50)

#Save token usage log to CSV file on exit
df = pd.DataFrame(csv_log)
df.to_csv("token_usage_log.csv", index=False)
print("✅ Token usage saved to token_usage_log.csv")
