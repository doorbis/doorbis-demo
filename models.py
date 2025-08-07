"""
Created on Wed Aug  6 18:42:42 2025
@project: doorbis.com demo
@author: russ
"""

openai_models = [
    # Current flagship & popular production LLMs
    "gpt-4o",                # omni flagship :contentReference[oaicite:0]{index=0}
    "gpt-4o-128k",
    "gpt-4o-mini",           # small, cost-efficient :contentReference[oaicite:1]{index=1}
    "gpt-4o-mini-high",
    "gpt-4-turbo",
    "gpt-4",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0125",

    # Research / legacy language models
    "text-davinci-003",
    "text-davinci-002",
    "code-davinci-002",
    "davinci",
    "curie",
    "babbage",
    "ada",

    # Multimodal & media-generation models
    "dall-e-3",
    "dall-e-2",
    "whisper-large-v3",
    "whisper-large-v4-preview",
    "sora-2025-02-video",    # text-to-video :contentReference[oaicite:2]{index=2}

    # Widely-rumored / imminently expected next models
    "gpt-4.5-turbo",
    "gpt-5",                 # slated for August 2025 launch :contentReference[oaicite:3]{index=3}
    "gpt-5-turbo",
    "dall-e-4",
    "whisper-large-v5"
]
