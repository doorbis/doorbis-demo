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
import base64
import pathlib

# ---------- CONFIGURATION ----------

# Set the AI model to use from environment variable or default to gpt-5
# Ensure you set the AI_MODEL environment variable before running the app
aiModel = os.getenv("AI_MODEL", "gpt-5")  # Default to gpt-5 if not set
if aiModel not in openai_models:
    raise ValueError(f"Unsupported AI model: {aiModel}. Supported models are: {openai_models}.")

# Set the AI model to use from environment variable or default to gpt-5
# Ensure you set the AI_MODEL environment variable before running the app
aiTemperature = os.getenv("AI_TEMPERATURE", 1.0)  # Default to 1.0 if not set


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


# --- Read query params (compatible across Streamlit versions) ---
def get_query_params():
    try:
        # Newer Streamlit may have st.query_params
        return dict(st.query_params)
    except Exception:
        # Fallback for older Streamlit
        return st.experimental_get_query_params()

def first(v, default=""):
    if v is None:
        return default
    if isinstance(v, list):
        return v[0] if v else default
    return v

params = get_query_params()
goto = first(params.get("goto"))

# --- Handle "click-through" ---
if goto == "logo":
    # Navigate by setting the official multipage ?page=... param.
    # NOTE: Page name must match how Streamlit derives it from filename:
    # pages/doorbis_demo.py  ->  "Doorbis Demo"
    try:
        st.experimental_set_query_params(page="Doorbis Demo")  # clears other params
    except Exception:
        # Very-old fallback: try updating then rerunning
        try:
            st.query_params.clear()
            st.query_params["page"] = "Doorbis Demo"
        except Exception:
            pass
    # Force navigation
    try:
        st.rerun()
    except Exception:
        st.experimental_rerun()

# --- Page body: show a clickable logo ---
# st.title("Welcome")
st.set_page_config(page_title="doorbis demo", page_icon="🟩", layout="centered")

# Path to your logo file
logo_path = pathlib.Path(__file__).parent / "doorbis_logo_2.png"
if not logo_path.exists():
    st.error(f"Logo not found at {logo_path}")
else:
    # Make the image itself clickable by embedding it in an <a> tag
    b64 = base64.b64encode(logo_path.read_bytes()).decode("utf-8")
    html = f'''
        <a href="?goto=logo" style="text-decoration:none; border:0; outline:0;">
            <img src="data:image/png;base64,{b64}"
                 alt="Doorbis logo"
                 style="max-width: 280px; height: auto; display:block; margin: 2rem auto;" />
        </a>
        <div style="text-align:center; font-size:0.9rem; opacity:0.7;">
            Click the logo to continue
        </div>
    '''
    st.markdown(html, unsafe_allow_html=True)

# Optional: text-link fallback (if HTML clicking were ever blocked)
st.write("[Continue ➜](./?goto=logo)")

# ---------- UI ----------

# Footer
st.markdown("---")
st.caption("Your visit was logged by Kossel Corp. Pre-seed RealAgentic AI angel pitch slides: https://realagentic.ai")