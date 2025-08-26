
import os
import json
import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="Mental Health AI Chatbot", page_icon="🧠", layout="centered")
st.title("🧠 Mental Health AI Chatbot")
st.markdown("""
<div style='background-color:#4a90e2;padding:10px;border-radius:8px;'>
    <h3 style='color:white;'>Your confidential assistant for well-being and support</h3>
</div>
""", unsafe_allow_html=True)
st.write("Type your mental health question below. Type 'bye' to end the chat.")

system_prompt = (
    "You are a helpful, professional AI assistant specialized in mental health. "
    "Answer questions only about mental health, well-being, stress, anxiety, and related topics. "
    "If asked about anything else, politely redirect the user to mental health topics."
)
generator = pipeline('text-generation', model='microsoft/DialoGPT-small')

if 'history' not in st.session_state:
    st.session_state.history = []
if 'conversation' not in st.session_state:
    # Load previous conversation if exists
    if os.path.exists("conversation.json"):
        with open("conversation.json", "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                st.session_state.conversation = data
                st.session_state.history = [msg["user"] for msg in data] + [msg["bot"] for msg in data]
            except Exception:
                st.session_state.conversation = []
    else:
        st.session_state.conversation = []

user_input = st.text_input("You:", "", key="user_input")
if st.button("Send", key="send_button_2"):
    if user_input.strip():
        # Add user input to conversation history
        st.session_state.conversation.append({"user": user_input, "bot": ""})
        # Build prompt from all previous turns
        prompt_history = []
        for msg in st.session_state.conversation:
            prompt_history.append(f"User: {msg['user']}")
            if msg['bot']:
                prompt_history.append(f"AI: {msg['bot']}")
        prompt = system_prompt + "\n" + "\n".join(prompt_history) + "\nAI:"
        try:
            response = generator(prompt, max_new_tokens=100, pad_token_id=generator.tokenizer.eos_token_id)
            generated = response[0]['generated_text']
            bot_reply = generated[len(prompt):].strip() if generated.startswith(prompt) else generated.strip()
        except Exception as e:
            bot_reply = "Sorry, I couldn't generate a response. Please try again."
        # Fallback if reply is empty, too short, or off-topic
        if (not bot_reply or len(bot_reply) < 10 or bot_reply.lower() in ["???", "i don't know.", "i don't know"] or not any(word in bot_reply.lower() for word in ["mental health", "stress", "anxiety", "wellbeing", "support", "therapy", "counseling", "emotion", "feeling", "cope", "help", "advice", "talk", "listen", "safe", "confidential", "mindfulness", "self-care"])):
            bot_reply = "I'm here to help with mental health topics like stress, anxiety, wellbeing, and support. Can you ask something specific about these?"
        # Update last conversation turn with bot reply
        st.session_state.conversation[-1]["bot"] = bot_reply

if st.session_state.conversation:
    for msg in st.session_state.conversation:
        st.markdown(f"""
        <div style='background-color:#eaf1fb;padding:12px 16px;border-radius:8px;margin-bottom:10px;color:#222222;'>
            <b>You:</b> {msg['user']}<br>
            <b>Bot:</b> {msg['bot']}
        </div>
        """, unsafe_allow_html=True)

if st.button("Save Conversation"):
    with open("conversation.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.conversation, f, indent=2, ensure_ascii=False)
    st.success("Conversation saved to conversation.json.")
