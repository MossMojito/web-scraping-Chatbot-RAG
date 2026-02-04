from app.services.llm import llm, vectorstore

def business_search_agent(query: str, chat_history: str = "") -> str:
    """
    Conversational business search - talks like a human!
    """
    
    # Extract search context
    context_prompt = f"""Based on conversation history:
{chat_history}

Current query: "{query}"

Extract:
1. Location mentioned (city, area, district)
2. Sport/activity type
3. Any other requirements

Return as: location: X, sport: Y, requirements: Z
If nothing mentioned, say: none
"""
    
    context_info = llm.invoke(context_prompt).content
    print(f"📍 Context: {context_info}")
    
    # Enhanced search query
    search_query = f"{query} {context_info}"
    
    # Search database
    if vectorstore is None:
        return "ขออภัยค่ะ ระบบฐานข้อมูลไม่พร้อมใช้งานในขณะนี้ 🙏"

    results = vectorstore.similarity_search(search_query, k=5)
    
    if not results:
        return "ขออภัยค่ะ ยังไม่มีข้อมูลในระบบ 🙏"
    
    # Format results
    results_text = ""
    for i, doc in enumerate(results, 1):
        m = doc.metadata
        results_text += f"""
{i}. {m.get('name', 'N/A')}
   ตั้งอยู่ที่ {m.get('address', 'N/A')} 
   โทร {m.get('phone', 'N/A')}
   
"""
    
    # Natural response
    natural_response_prompt = f"""User asked: "{query}"

Conversation history:
{chat_history}

Search results:
{results_text}

Write a warm, conversational Thai response like a helpful female assistant:
**IMPORTANT: Use female Thai politeness - use "ค่ะ" NOT "ครับ"**

1. Acknowledge their request naturally
2. Present the businesses in a friendly way
3. Offer to help with more details
4. Be natural and conversational

Include the business details but make it flow naturally.
"""
    
    response = llm.invoke(natural_response_prompt).content
    return response
