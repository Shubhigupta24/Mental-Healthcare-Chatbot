from flask import Flask, render_template, request, jsonify, send_from_directory
import logging
import time

app = Flask(__name__, static_folder='static')

# Enable logging
logging.basicConfig(level=logging.DEBUG)


# ✅ Serve Static Files like CSS
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)


# ✅ Home Route to Render Chatbot Page
@app.route('/')
def home():
    app.logger.debug("Loading chatbot frontend.")
    return render_template('index.html')


# ✅ Function to Simulate Healthcare Chatbot Response
def chatbot_response(user_message):
    app.logger.debug(f"User message received: {user_message}")
    
    # Convert user message to lowercase
    user_message_lower = user_message.lower().strip()
    
    # ✅ Predefined Responses
    responses = {
        "hey": "Response: Hello! How can I assist you today?<br>Follow-Up: Are you looking for emotional support or tips to manage stress?",
        "hello": "Response: Hi there! How are you feeling today?<br>Follow-Up: Let me know if there's anything specific you'd like help with.",
        "feeling sad": "Response: I’m sorry to hear that. Would you like to talk about what’s making you feel this way?<br>Follow-Up: I can also suggest activities to help lift your mood if you'd like.",
        "feeling anxious": "Response: I understand. Would you like some tips to manage anxiety or just someone to listen?<br>Follow-Up: Let me know how I can best support you.",
        "stressed out": "Response: I’m here to help. Would you like to try a breathing exercise or talk about what’s causing stress?<br>Follow-Up: Let’s find strategies to make things feel more manageable.",
        "giving up": "Response: I’m really sorry you’re feeling this way. You’re not alone, and help is available.<br>Follow-Up: Would you like me to connect you to resources?",
        "need to relax": "Response: How about trying a deep breathing exercise?<br>Inhale for 4 seconds, hold for 4, and exhale for 4 seconds.",
        "meditation guidance": "Response: Sure! Close your eyes and take a deep breath.<br>Let me guide you through a meditation session if you'd like.",
        "calm down": "Response: Let’s try grounding.<br>Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste."
    }

    # ✅ Exact Match
    for condition, response in responses.items():
        if condition in user_message_lower:
            app.logger.debug(f"Exact match found for condition: {condition}")
            return response
    
    # ✅ No Match Found - Default Response
    return "I understand you have a health-related query.<br>Could you please be more specific about your symptoms or condition?"


# ✅ Backend Route to Handle Chatbot Messages
@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_message = request.form.get('message')
    app.logger.debug(f"Message received: {user_message}")
    
    if user_message:
        # ✅ Simulate Typing Delay
        time.sleep(1.5)
        response = chatbot_response(user_message)
        app.logger.debug(f"Response sent: {response}")
        return jsonify({"response": response})
    else:
        return jsonify({"response": "No message received"}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5001)
