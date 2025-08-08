# -*- coding: utf-8 -*-
"""
Created on Sat Jul  26 02:42:42 2025

@project: doorbis.com demo
 @author: russ
  @model: 4o
"""

from pyexpat import model
import streamlit as st
from openai import OpenAI
import logging
import os
import datetime
from models import openai_models  # Importing the list of models
from PIL import Image

# ---------- CONFIGURATION ----------

# Set the AI model to use from environment variable or default to gpt-5
# Ensure you set the AI_MODEL environment variable before running the app
aiModel = os.getenv("AI_MODEL", "gpt-5")  # Default to gpt-5 if not set
if aiModel not in openai_models:
    raise ValueError(f"Unsupported AI model: {aiModel}. Supported models are: {openai_models}.")

# Set the AI model to use from environment variable or default to gpt-5
# Ensure you set the AI_MODEL environment variable before running the app
aiTemperature = os.getenv("AI_TEMPERATURE", 1.0)  # Default to 1.0 if not set

# OpenAI API key from the environment variable
# Ensure you set the OPENAI_API_KEY environment variable before running the app
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))  # Use environment variable for security
if not client.api_key:
    raise ValueError("OpenAI API key not set. Please set the OPENAI_API_KEY environment variable.")


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
        response = client.chat.completions.create(
            model = aiModel,
            messages=[
                {"role": "system", "content": "You're a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=aiTemperature,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error calling OpenAI: {e}"

# ---------- UI ----------

st.set_page_config(page_title="doorbis demo", layout="centered")
logo = Image.open("doorbis_logo.png")  # Ensure you have a logo image in the same directory 
# st.title("💡 doorbis demo")
st.image(logo, width=100, use_container_width=True)

st.markdown("Ask a question, get an AI-generated response. Your IP will be logged.")

user_input = st.text_area("Enter your message:", height = 100)

if st.button("Send"):
    if user_input.strip():
        ip = get_visitor_ip()
        st.spinner(f"Processing your request from internet protocol address {ip} using {aiModel} LLM...")
        log_visitor(ip, user_input)
        
        with st.spinner(f"Talking to {aiModel}..."):
            response = call_openai(user_input)
        st.success("Response:")
        st.write(response)
    else:
        st.warning("Please enter a message before sending.")

# Footer
st.markdown("---")
st.caption("Your visit was logged by Kossel Corp. Pre-seed RealAgentic AI angel pitch slides: https://realagentic.ai")
