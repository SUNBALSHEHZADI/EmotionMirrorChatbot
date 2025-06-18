import streamlit as st
import random
import time
from streamlit.components.v1 import html

# Set page config with light purple theme
st.set_page_config(
    page_title="Emotion Mirror Chatbot",
    page_icon="😊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for enhanced light purple theme
st.markdown("""
<style>
:root {
    --primary: #b19cd9;
    --primary-dark: #8a7faa;
    --background: linear-gradient(135deg, #f5f0ff, #e6d7ff);
    --secondary-background: #e6e0fa;
    --text: #4a4a4a;
    --font: "Arial", sans-serif;
}
body {
    background-image: var(--background);
    background-attachment: fixed;
    color: var(--text);
    font-family: var(--font);
}
.stTextInput>div>div>input {
    background-color: var(--secondary-background) !important;
    color: var(--text) !important;
    border: 2px solid var(--primary) !important;
    border-radius: 12px;
}
.stButton>button {
    background-color: var(--primary) !important;
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 8px 16px;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background-color: var(--primary-dark) !important;
    transform: scale(1.05);
}
.stMarkdown {
    font-family: monospace !important;
    font-size: 16px !important;
}
.chat-message {
    padding: 12px 16px;
    border-radius: 16px;
    margin: 10px 0;
    max-width: 80%;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
.user-message {
    background-color: var(--secondary-background);
    margin-left: auto;
    text-align: left;
    border-bottom-right-radius: 4px;
}
.bot-message {
    background-color: var(--primary);
    color: white;
    margin-right: auto;
    border-bottom-left-radius: 4px;
}
.face-container {
    text-align: center;
    padding: 20px;
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(5px);
    border-radius: 20px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    margin: 20px auto;
    max-width: 300px;
    border: 2px solid var(--primary);
}
.header {
    text-align: center;
    margin-bottom: 20px;
}
.title {
    color: var(--primary);
    font-size: 2.5rem;
    margin-bottom: 10px;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
}
.subtitle {
    color: var(--text);
    font-size: 1.1rem;
    margin-bottom: 30px;
}
.footer {
    text-align: center;
    margin-top: 30px;
    color: var(--primary);
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# Emotion databases
POSITIVE_WORDS = {"happy", "awesome", "great", "joy", "excited", "good", "wonderful", "fantastic", "amazing", "yay", "ecstatic"}
NEGATIVE_WORDS = {"sad", "depressed", "angry", "cry", "lonely", "bad", "terrible", "awful", "miserable", "upset", "grief"}
LOVE_WORDS = {"love", "heart", "adore", "crush", "romance", "affection", "passion"}
HELP_RESPONSES = [
    "Would you like to talk about it? 💬",
    "I'm here to listen whenever you need 💙",
    "Want some uplifting quotes? 📜",
    "Would a virtual hug help? 🤗",
    "Let's focus on something positive 🌈",
    "Remember: this too shall pass 🌤️"
]

# ASCII Art Library
FACES = {
    "happy": r"""
  ╔════════════╗
  😄 AWESOME DAY!  
  ╚════════════╝
    """,
    "sad": r"""
  ╔════════════╗
  😢 TOUGH TIMES?  
  ╚════════════╝
    """,
    "neutral": r"""
  ╔════════════╗
  😐 HELLO THERE   
  ╚════════════╝
    """,
    "love": r"""
  ╔════════════╗
  😍 LOVELY FEELING!  
  ╚════════════╝
    """,
    "angry": r"""
  ╔════════════╗
  😠 TAKE A DEEP BREATH  
  ╚════════════╝
    """
}

# Confetti effect using JavaScript
def confetti_effect():
    confetti_js = """
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <script>
    const count = 200;
    const defaults = {
        origin: { y: 0.7 }
    };
    function fire(particleRatio, opts) {
        confetti(Object.assign({}, defaults, opts, {
            particleCount: Math.floor(count * particleRatio),
            colors: ['#b19cd9', '#e6d7ff', '#8a7faa', '#ffffff']
        }));
    }
    fire(0.25, { spread: 26, startVelocity: 55 });
    fire(0.2, { spread: 60 });
    fire(0.35, { spread: 100, decay: 0.91, scalar: 0.8 });
    fire(0.1, { spread: 120, startVelocity: 25, decay: 0.92, scalar: 1.2 });
    fire(0.1, { spread: 120, startVelocity: 45 });
    </script>
    """
    html(confetti_js)

# Emotion detection function
def detect_emotion(text):
    text = text.lower()
    if any(word in text for word in POSITIVE_WORDS):
        return "happy"
    elif any(word in text for word in NEGATIVE_WORDS):
        return "sad"
    elif any(word in text for word in LOVE_WORDS):
        return "love"
    elif "angry" in text or "mad" in text or "furious" in text:
        return "angry"
    return "neutral"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.current_emotion = "neutral"

# Header with title and description
st.markdown('<div class="header"><div class="title">✨ Emotion Mirror Chatbot</div><div class="subtitle">I\'m a reactive AI agent that mirrors your emotions! Try words like <i>happy, sad, love,</i> or <i>awesome</i></div></div>', unsafe_allow_html=True)

# Display current face
with st.container():
    st.markdown(f"<div class='face-container'>\n{FACES[st.session_state.current_emotion]}\n</div>", 
                unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(f"<div class='chat-message {message['role']}-message'>{message['content']}</div>", 
                    unsafe_allow_html=True)

# User input
if prompt := st.chat_input("How are you feeling today?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Detect emotion
    emotion = detect_emotion(prompt)
    st.session_state.current_emotion = emotion
    
    # Generate bot response
    if emotion == "happy":
        response = FACES["happy"] + "\n\n🌟 That's wonderful to hear! Keep spreading positivity!"
        confetti_effect()
    elif emotion == "sad":
        response = FACES["sad"] + "\n\n" + random.choice(HELP_RESPONSES)
    elif emotion == "love":
        response = FACES["love"] + "\n\n💖 Love is the most beautiful feeling! Treasure it."
    elif emotion == "angry":
        response = FACES["angry"] + "\n\n☁️ Take a deep breath. Count to ten. You've got this."
    else:
        response = FACES["neutral"] + "\n\nTell me more about your feelings..."
    
    # Add bot response to chat history
    st.session_state.messages.append({"role": "bot", "content": response})
    
    # Rerun to update the display
    st.rerun()

# Add reset button
if st.button("Reset Conversation"):
    st.session_state.messages = []
    st.session_state.current_emotion = "neutral"
    st.rerun()
