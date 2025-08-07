# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 20:06:22 2025

@author: russ
@model: 
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 10:56:18 2025

@author: russ
@model: 
"""

import openai
import PyPDF2
# import os
from typing import Literal
import pyttsx3
from acronym_expander import acronym_expander


# Speech output function
def speak(text, voice_properties=None):
    engine = pyttsx3.init()
    if voice_properties:
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[voice_properties.get('voice_id', 0)].id)
        ## match agent rate of speech with client rate of speech.
        ## new client on-boarding process.
        engine.setProperty('rate', voice_properties.get('rate', 220))
    engine.say(text)
    engine.runAndWait()

# Main interaction function
def interact_with_client(pdf_file:str,
                         interaction_mode:Literal['text', 'speech']='text',
                         voice_characteristics:dict=None,
                         conversational_personality:str="friendly and professional",
                         client_language:str='en') -> Literal['yes', 'unsure', 'no']:
    loc = LOCALIZATION.get(client_language, LOCALIZATION['en'])

    pdf_text = extract_pdf_text(pdf_file)
    
    conversation_history = [
        {"role": "system", "content": f"You are a real estate disclosure expert. Your personality is {conversational_personality}. You answer questions honestly based on the seller disclosure PDF provided: {pdf_text}. Do not make up answers. If unsure, clearly say you do not know."}
    ]
   

    print(loc['start_interaction'])

    while True:
        if interaction_mode == 'speech':
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print(loc['listening'])
                audio = recognizer.listen(source)
                try:
                    user_input = recognizer.recognize_google(audio)
                    print(f"{loc['client']} (voice): {user_input}")
                except sr.UnknownValueError:
                    speak(loc['did_not_catch'], voice_characteristics)
                    continue
        else:
            user_input = input(f"{loc['client']}: ")

        if user_input.lower() in ['exit', 'quit', 'end', 'stop', 'done', 'bored']:
            break

        conversation_history.append({"role": "user", "content": user_input})

        response = openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=conversation_history,
            temperature=0.3
        )
        # To get the response text:
        reply = response.choices[0].message.content
        print(f"{loc['agent']}: {reply}")

        if interaction_mode == 'speech':
            speak(acronym_expander(reply), voice_characteristics)

        conversation_history.append({"role": "assistant", "content": reply})

    print(f"{loc['agent']}: {loc['closing_message']}")
    if interaction_mode == 'speech':
        speak(loc['closing_message'], voice_characteristics)

    decision_input = input(loc['client_decision']).strip().lower()
    if decision_input in ['ok', 'yes', 'okay', 'sure', 'definitely', 'yup', 'y']:
        decision_input = 'yes'
    elif decision_input in ['not ok', 'no', 'not okay', 'never', 'nope', 'no way', 'definitely not', 'n']:
            decision_input = 'no'
    else:
        decision_input = 'unsure'

    transcript_choice = input(loc['transcript_question']).strip().lower()
    if transcript_choice == 'yes':
        print(loc['transcript_confirmation'])
        if interaction_mode == 'speech':
            speak(loc['transcript_confirmation'], voice_characteristics)

    next_meeting = input(loc['next_meeting_question']).strip().lower()
    if next_meeting == 'yes':
        next_appointment = input(loc['next_meeting_schedule'])
        print(loc['appointment_scheduled'].format(appointment=next_appointment))
        if interaction_mode == 'speech':
            speak(loc['appointment_scheduled'].format(appointment=next_appointment), voice_characteristics)

    print(loc['interaction_concluded'])
    return decision_input

# Example usage
if __name__ == "__main__":
    decision = interact_with_client(
        pdf_file="I:/Shared drives/technology/RealAgentic.ai/REALdisclosures/Disclosures-207-San-Antonio-Pl-San-Jose-CA-95116.pdf",
        interaction_mode="speech",
        voice_characteristics={"voice_id": 1, "rate": 220},  # 220 is Angel speed;  0 is male;  1 is female on Win11
        conversational_personality="warm, supportive, and knowledgeable",
        client_language='en'
    )
    print(LOCALIZATION['en']['final_decision'].format(decision=decision))
