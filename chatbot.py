import json
from transformers import pipeline
import tkinter as tk
from tkinter import scrolledtext
from tkinter import font

print("Starting chatbot...")

def get_ai_reply(history, generator, system_prompt):
    prompt = system_prompt + "\n" + "\n".join(history)
    response = generator(prompt, max_new_tokens=100, pad_token_id=generator.tokenizer.eos_token_id)
    generated = response[0]['generated_text']
    bot_reply = generated[len(prompt):].strip() if generated.startswith(prompt) else generated.strip()
    if not bot_reply or len(bot_reply) < 5 or bot_reply in ["???", "I don't know.", "I don't know"]:
        bot_reply = "I'm still learning! Can you ask something else or rephrase your question?"
    return bot_reply

def run_gui():
    conversation = []
    system_prompt = (
        "You are a helpful, professional AI assistant specialized in mental health. "
        "Answer questions only about mental health, well-being, stress, anxiety, and related topics. "
        "If asked about anything else, politely redirect the user to mental health topics."
    )
    generator = pipeline('text-generation', model='microsoft/DialoGPT-small')
    history = []

    root = tk.Tk()
    root.title("Mental Health AI Chatbot")
    root.configure(bg="#f0f4f8")
    root.geometry("600x500")

    # Custom fonts
    header_font = font.Font(family="Helvetica", size=18, weight="bold")
    chat_font = font.Font(family="Arial", size=12)
    button_font = font.Font(family="Arial", size=11, weight="bold")

    # Header
    header_frame = tk.Frame(root, bg="#4a90e2")
    header_frame.pack(fill=tk.X)
    header_label = tk.Label(header_frame, text="Mental Health AI Chatbot", font=header_font, fg="white", bg="#4a90e2", pady=10)
    header_label.pack()
    subtitle_label = tk.Label(header_frame, text="Your confidential assistant for well-being and support", font=("Arial", 11), fg="white", bg="#4a90e2")
    subtitle_label.pack(pady=(0,10))

    # Chat window
    chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', width=70, height=18, font=chat_font, bg="#ffffff", fg="#222222", padx=10, pady=10)
    chat_window.pack(padx=15, pady=(10,5), fill=tk.BOTH, expand=True)

    # Entry and button frame
    entry_frame = tk.Frame(root, bg="#f0f4f8")
    entry_frame.pack(fill=tk.X, padx=15, pady=10)
    entry = tk.Entry(entry_frame, width=50, font=chat_font, bg="#eaf1fb", fg="#222222", relief=tk.FLAT)
    entry.pack(side=tk.LEFT, padx=(0,10), ipady=6)
    send_button = tk.Button(entry_frame, text="Send", font=button_font, bg="#4a90e2", fg="white", activebackground="#357abd", activeforeground="white", relief=tk.FLAT, command=lambda: send_message())
    send_button.pack(side=tk.LEFT, ipadx=10, ipady=6)

    def send_message():
        user_input = entry.get().strip()
        if not user_input:
            return
        chat_window.config(state='normal')
        chat_window.insert(tk.END, f"You: {user_input}\n")
        chat_window.config(state='disabled')
        entry.delete(0, tk.END)
        if user_input.lower() == "bye":
            bot_reply = "Goodbye! Take care of your mental health!"
            chat_window.config(state='normal')
            chat_window.insert(tk.END, f"Bot: {bot_reply}\n")
            chat_window.config(state='disabled')
            conversation.append({"user": user_input, "bot": bot_reply})
            root.quit()
            return
        if user_input.lower() == "help":
            bot_reply = "You can ask me anything about mental health, well-being, stress, or anxiety. Type 'bye' to exit."
        else:
            history.append(user_input)
            bot_reply = get_ai_reply(history, generator, system_prompt)
            history.append(bot_reply)
        chat_window.config(state='normal')
        chat_window.insert(tk.END, f"Bot: {bot_reply}\n")
        chat_window.config(state='disabled')
        conversation.append({"user": user_input, "bot": bot_reply})

    entry.bind('<Return>', lambda event: send_message())
    chat_window.config(state='normal')
    chat_window.insert(tk.END, "Welcome to your Mental Health AI Chatbot! Type 'help' for options or 'bye' to exit.\n")
    chat_window.config(state='disabled')
    root.mainloop()
    with open("conversation.json", "w") as f:
        json.dump(conversation, f, indent=2)
    print("Conversation saved to conversation.json.")

if __name__ == "__main__":
    run_gui()
