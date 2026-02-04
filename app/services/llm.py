from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_classic.memory import ConversationBufferWindowMemory
from app.core.config import Config

# Initialize LLM
llm = ChatOpenAI(
    model=Config.LLM_MODEL,
    temperature=Config.TEMPERATURE,
    openai_api_key=Config.OPENAI_API_KEY
)

# Initialize Embeddings
embeddings = OpenAIEmbeddings(
    model=Config.EMBEDDING_MODEL,
    openai_api_key=Config.OPENAI_API_KEY
)

# Load FAISS vectorstore
try:
    vectorstore = FAISS.load_local(
        Config.VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    print(f"📊 Vectorstore loaded: {vectorstore.index.ntotal} vectors")
except Exception as e:
    print(f"⚠️ Error loading vectorstore: {e}")
    vectorstore = None

# Memory Factory (We need a new memory instance per session/request ideally, 
# but for the simple demo version sticking to the original global-ish pattern or factory)
# The original code used a global memory, which is not thread-safe for multi-user.
# For now, I will provide a factory function.

def get_memory():
    return ConversationBufferWindowMemory(
        memory_key="chat_history",
        k=3,
        return_messages=True,
        input_key="input",
        output_key="output"
    )

# Global memory for single-session demo (to minimize changes from original logic)
# Ideally this should be handled per user session.
# keeping it simple as per original implementation for now.
global_memory = get_memory()
