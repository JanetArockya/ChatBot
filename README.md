**Mental Health AI Chatbot**
A conversational AI chatbot specialized in mental health topics, built with Python, Hugging Face Transformers, and Streamlit. The chatbot provides supportive, confidential, and informative responses to questions about stress, anxiety, wellbeing, and related topics

Features
AI-powered conversation using the DialoGPT-small model from Hugging Face.
Streamlit web interface for a modern, user-friendly chat experience.
Multi-turn conversation: Maintains full chat history for ongoing dialogue.
Specialized for mental health: Answers only mental health-related questions and politely redirects off-topic queries.
Conversation logging: Saves all chat history to conversation.json.

Setup Instructions
1. Clone or download the repository.
2. Install dependencies:
   pip install streamlit transformers torch
3. Run the chatbot
   streamlit run app.py
4. Chat with the bot:
   Enter your mental health questions in the input box.
   Click "Send" to receive a response.
   Click "Save Conversation" to save the chat history.

License
This project is for educational and demonstration purposes.
