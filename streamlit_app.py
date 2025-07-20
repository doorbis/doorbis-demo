import streamlit as st
import openai
import logging
import os
import datetime

# ---------- CONFIGURATION ----------

# Your OpenAI API key (set this as an env var in production!)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Logging config
LOG_FILE = "visitors.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
)

# ---------- UTILS ----------

def get_visitor_ip():
    headers = st.experimental_get_query_params()
    cf_ip = headers.get("cf-connecting-ip", [None])[0]
    fallback_ip = os.environ.get("REMOTE_ADDR", "unknown")
    return cf_ip or fallback_ip

def log_visitor(ip, user_input):
    timestamp = datetime.datetime.now().isoformat()
    logging.info(f"{timestamp} | IP: {ip} | Prompt: {user_input}")

def call_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You're a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error calling OpenAI: {e}"

# ---------- UI ----------

st.set_page_config(page_title="doorbis.com – AI Demo", layout="centered")

st.title("💡 doorbis.com AI Chat Demo")
st.markdown("Ask a question, get an AI-generated response. Your IP will be logged.")

user_input = st.text_area("Enter your message:", height=100)

if st.button("Send"):
    if user_input.strip():
        ip = get_visitor_ip()
        log_visitor(ip, user_input)
        with st.spinner("Talking to GPT-4o..."):
            response = call_openai(user_input)
        st.success("AI response:")
        st.write(response)
    else:
        st.warning("Please enter a message before sending.")

# Footer
st.markdown("---")
st.caption("Your visit is being logged for demo purposes.")
