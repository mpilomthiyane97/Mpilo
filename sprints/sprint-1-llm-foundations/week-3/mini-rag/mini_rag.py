import os
from dotenv import load_dotenv
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

# Load .env
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Setup tokenizer callback
token_counter = TokenCountingHandler(
    tokenizer=tiktoken.encoding_for_model("gpt-3.5-turbo").encode
)
callback_manager = CallbackManager([token_counter])

# Settings
Settings.llm = OpenAI(model="gpt-3.5-turbo")
Settings.embed_model = OpenAIEmbedding()
Settings.callback_manager = callback_manager

# Load docs
print("🔍 Loading documents ...")
documents = SimpleDirectoryReader("./data", recursive=True).load_data()

# Parse & embed
print("🧠 Indexing documents ...")
pipeline = IngestionPipeline(transformations=[SentenceSplitter(), Settings.embed_model])
nodes = pipeline.run(documents=documents)

# Store context
storage_context = StorageContext.from_defaults()
vector_index = VectorStoreIndex(nodes, storage_context=storage_context)
keyword_index = KeywordTableIndex(nodes)

# Query engines
vector_engine = vector_index.as_query_engine(similarity_top_k=3)
keyword_engine = keyword_index.as_query_engine(similarity_top_k=3)

print("\n✅ Hybrid Mini-RAG is ready! Type your question below.\n")

csv_log = []

while True:
    user_query = input("You: ")
    if user_query.lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break

    # Run both retrievers
    keyword_response = keyword_engine.query(user_query)
    vector_response = vector_engine.query(user_query)

    # Combine (basic hybrid by concatenation here; customize as needed)
    combined_answer = (
        f"[Keyword Match]\n{keyword_response.response}\n\n"
        f"[Vector Match]\n{vector_response.response}"
    )

    print("\n📄 Answer:\n", combined_answer)

    # Print sources for Keyword Match
    print("\n📚 Sources for Keyword Match:")
    for node in getattr(keyword_response, "source_nodes", []):
        file_path = node.metadata.get("file_path", "Unknown")
        score = getattr(node, "score", None)
        score_display = f"{score:.2f}" if score is not None else "N/A"
        print(f" - {file_path} (score: {score_display})")

    # Print sources for Vector Match
    print("\n📚 Sources for Vector Match:")
    for node in getattr(vector_response, "source_nodes", []):
        file_path = node.metadata.get("file_path", "Unknown")
        score = getattr(node, "score", None)
        score_display = f"{score:.2f}" if score is not None else "N/A"
        print(f" - {file_path} (score: {score_display})")

    # Get token counts
    embedding_tokens = token_counter.total_embedding_token_count
    prompt_tokens = token_counter.prompt_llm_token_count
    completion_tokens = token_counter.completion_llm_token_count
    total_llm_tokens = token_counter.total_llm_token_count

    # === Calculate Costs ===
    # Prices per 1K tokens
    EMBEDDING_COST_PER_1K = 0.0001  # $0.0001 per 1K tokens
    PROMPT_COST_PER_1K = 0.0015     # GPT-3.5 Turbo prompt cost
    COMPLETION_COST_PER_1K = 0.002  # GPT-3.5 Turbo completion cost

    # Calculate actual cost
    embedding_cost = (embedding_tokens / 1000) * EMBEDDING_COST_PER_1K
    prompt_cost = (prompt_tokens / 1000) * PROMPT_COST_PER_1K
    completion_cost = (completion_tokens / 1000) * COMPLETION_COST_PER_1K
    total_cost = embedding_cost + prompt_cost + completion_cost

    # Log entry with cost
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
    print(f"💰 Total cost this query: ${total_cost:.6f}")
    print("-" * 50)

# Save cost log on exit
df = pd.DataFrame(csv_log)
df.to_csv("token_usage_log.csv", index=False)
print("✅ Token usage saved to token_usage_log.csv")
