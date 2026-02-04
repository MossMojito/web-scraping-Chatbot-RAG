from app.services.llm import get_memory, global_memory
from app.agents.router import query_router, out_of_scope_agent
from app.agents.search import business_search_agent
from app.agents.knowledge import sports_knowledge_agent
from app.agents.utils import polish_response

def chatbot(user_input: str) -> str:
    """
    CONVERSATIONAL multi-agent chatbot - talks like a human!
    """
    
    # Get history from global memory (for demo simplicity)
    # in production, pass a session_id to get_memory(session_id)
    history = global_memory.load_memory_variables({})
    chat_history = ""
    
    if history.get('chat_history'):
        for msg in history['chat_history']:
            chat_history += f"{msg.type}: {msg.content}\n"
    
    print(f"💭 User: {user_input}")
    print(f"🧠 Memory: {len(history.get('chat_history', []))} messages")
    
    # Route query
    query_type = query_router(user_input, chat_history)
    print(f"🎯 Route: {query_type}")
    
    # Execute agent
    if query_type == "business_search":
        print("🔍 Agent: Business Search (Conversational RAG)")
        response = business_search_agent(user_input, chat_history)
        
    elif query_type == "sports_knowledge":
        print("🧠 Agent: Sports Knowledge (LLM)")
        response = sports_knowledge_agent(user_input, chat_history)
        
    elif query_type == "out_of_scope":
        print("⚠️ Agent: Out-of-Scope")
        response = out_of_scope_agent(user_input)
        
    else:
        response = "I'm not sure how to help with that. Could you rephrase?"
    
    # Polish response for naturalness
    response = polish_response(response, user_input, chat_history)
    
    # Save to memory
    global_memory.save_context(
        {"input": user_input},
        {"output": response}
    )
    
    print("💾 Saved to memory")
    print("="*60)
    
    return response
