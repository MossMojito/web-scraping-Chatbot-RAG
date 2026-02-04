from flask import Blueprint, request, jsonify
from app.agents.orchestrator import chatbot
from app.services.llm import vectorstore

api_bp = Blueprint('api', __name__)

@api_bp.route('/', methods=['GET'])
def health():
    # Check vectorstore status
    vs_size = vectorstore.index.ntotal if vectorstore else 0
    
    return jsonify({
        'status': 'Chatbot API is running!',
        'service': 'Yellow Pages Sports Chatbot',
        'version': '2.0',
        'vectorstore_size': vs_size
    })

@api_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get chatbot response
        response = chatbot(message)
        
        return jsonify({'response': response})
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
