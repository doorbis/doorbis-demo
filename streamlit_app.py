# -*- coding: utf-8 -*-
"""
Created on Sat Jul  26 02:42:42 2025

@project: doorbis.com demo
 @author: sterling
  @model: 4o
"""

from pyexpat import model
import streamlit as st
import openai
import logging
import os
import datetime

# ---------- CONFIGURATION ----------

# Your OpenAI API key (set this as an env var in production!)
openai.api_key = os.getenv("OPENAI_API_KEY")
aiModel = "gpt-4o"

# Logging config
LOG_FILE = "visitors.log"
logging.basicConfig(
    filename = LOG_FILE,
    level = logging.INFO,
    format = "%(asctime)s | %(message)s",
)

# ---------- UTILS ----------

def get_visitor_ip():
    params = st.query_params
    cf_ip = params.get("cf-connecting-ip", [None])[0]
    fallback_ip = os.environ.get("REMOTE_ADDR", "unknown")
    return cf_ip or fallback_ip


def log_visitor(ip, user_input):
    timestamp = datetime.datetime.now().isoformat()
    logging.info(f"{timestamp} | IP: {ip} | Prompt: {user_input}")


def call_openai(prompt):
    try:
        response = openai.chat.completions.create(
            model=aiModel,
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

st.set_page_config(page_title="doorbis demo", layout="centered")

st.title("💡 doorbis demo")
st.markdown("Ask a question, get an AI-generated response. Your IP will be logged.")

user_input = st.text_area("Enter your message:", height = 100)

if st.button("Send"):
    if user_input.strip():
        ip = get_visitor_ip()
        st.spinner(f"Processing your request from internet protocol address {ip} using {aiModel} LLM...")
        log_visitor(ip, user_input)
        
        with st.spinner("Talking to GPT-4o..."):
            response = call_openai(user_input)
        st.success("AI response:")
        st.write(response)
    else:
        st.warning("Please enter a message before sending.")

# Footer
st.markdown("---")
st.caption("Your visit was logged by Kossel Corp. Pre-seed RealAgentic AI angel pitch slides: https://realagentic.ai")
