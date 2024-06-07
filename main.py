import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, AutoModelForSequenceClassification
import streamlit as st
import os
import time
from animation_worker import *

# Ensure the offload folder exists
offload_folder = "./offload_folder"
os.makedirs(offload_folder, exist_ok=True)

#########################################################
# Model Loading
#########################################################

@st.cache_resource
def load_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    tokenizer = AutoTokenizer.from_pretrained("MedAliFarhat/TinyLLama_Chat_Medication")
    model = AutoModelForCausalLM.from_pretrained("MedAliFarhat/TinyLLama_Chat_Medication", 
                                                torch_dtype=torch.float16 if device == "cuda" else torch.float32, 
                                                device_map="auto", 
                                                offload_folder=offload_folder)
    print(f"Model device:{next(model.parameters()).device}")

    # Chatbot pipeline
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer
    )

    return pipe

pipe = load_model()

#########################################################
# Animations
#########################################################

# Check if animations have already been run
if 'animations_run' not in st.session_state:
    st.session_state.animations_run = False

if not st.session_state.animations_run:
    run_animations()
    st.session_state.animations_run = True
else:
    show_static()

#########################################################
# Main Loop
#########################################################

if "history" not in st.session_state:
    st.session_state.history = []

# Process prompt function
def process_prompt(user_input):
    user_input = user_input.strip()
    if user_input:
        if user_input[-1] != "?":
            user_input += " ?"
        start_time = time.time()
        st.session_state.history.append({"role": "user", "content": user_input})
        messages = [
            {"role": "system", "content": "If the question isn't related to the medical or pharmaceutical field, respond by saying that you are designed to answer questions related to the aforementionned fields only.\
             Your name is Opia and you are part of the 'Optichain' team. You're an expert in the medical and pharmaceutical fields so I want a detailed response to the next questions, if the message is thanking or welcome or goodbye so give a clear and direct response."},
            {"role": "user", "content": user_input},
        ]

        try:
            prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            outputs = pipe(
                prompt, 
                max_new_tokens=500,
                do_sample=True, 
                temperature=0.01, 
                top_k=1, 
                top_p=0.1
            )

            response = outputs[0]["generated_text"].split("?")[1].strip()
            response_lines = response[19:]
            st.session_state.history.append({"role": "bot", "content": response_lines})
            print(f"Total prompt time : {time.time() - start_time:.3f}s")
                
        except Exception as e:
            st.error(f"Error generating response: {e}")

# Text Field & 'Send' Button
user_input = st.text_input("Input message", "", placeholder="Message", autocomplete='off')
send_btn = st.button("Send")
if send_btn:
    process_prompt(user_input)


for i, msg in enumerate(st.session_state.history):
    if msg["role"] == "user":
        st.text_area("You:", value=msg["content"], height=len(msg["content"])//10+1, key=f"user_{i}", disabled=True)
    else:
        st.text_area("Opia:", value=msg["content"], height=len(msg["content"])*4//10+1, key=f"bot_{i}", disabled=True)
