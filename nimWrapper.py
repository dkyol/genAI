import requests
from flask import Flask, jsonify, request
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/response', methods=['POST', 'GET'])
def handle_data():
    if request.method == 'POST':
        query = request.get_json()

        #print('Question:', query['question'])
        print(os.getenv('KEY'))
        
        client = ChatNVIDIA(
            model = "meta/llama-3.1-405b-instruct",
            api_key = os.getenv('KEY'),
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024
        )
        
        answer = []
        for chunk in client.stream([{"role": "user", "content" : query['question']}]): 
            #print(chunk.content, end="")
            answer.append(chunk.content)

    return ' '.join(answer)
    

if __name__ == '__main__':
    app.run(debug=True)

# curl -H "Content-Type: application/json" -d "{\"question\": \"question\"}" -X POST http://127.0.0.1:5000/response