import streamlit as st
import time

def run_animations():
    # Add a logo in the sidebar
    logo_path = "opia logo.png"  # Replace with your logo file path
    st.sidebar.image(logo_path, use_column_width=True)

    # Animated text in the sidebar
    animated_text = """Hello! I'm OPIA, your friendly and knowledgeable AI assistant created to help you with a wide range of tasks and answer your questions, especially in the medical and pharmaceutical fields.  
    My purpose is to assist you efficiently and accurately, ensuring you receive the best possible information and support."""

    placeholder = st.sidebar.empty()
    current_text = ""
    for line in animated_text.split('\n'):
        for char in line:
            current_text += char
            # Calculate the height based on the number of lines
            placeholder.text_area("", current_text, height=len(current_text)*2//2+1, disabled=True)  # Adjust multiplier as needed
            time.sleep(0.04)
        current_text += "\n"

    # Add space to push buttons to the bottom
    for _ in range(20):
        st.sidebar.empty()

    # Add another logo in the sidebar
    logo_path = "optichain logo.png"  # Replace with your logo file path
    st.sidebar.image(logo_path, use_column_width=True)

    # Animated title
    title_text = "Opia will assist you. Feel free to ask him."
    title_placeholder = st.empty()
    current_title = ""
    for char in title_text:
        current_title += char
        title_placeholder.title(current_title, anchor=False)
        time.sleep(0.05)
    
    # Mark animations as run
    st.session_state.animations_run = True

def show_static():
    logo_path = "opia logo.png"  # Replace with your logo file path
    st.sidebar.image(logo_path, use_column_width=True)
    
    animated_text = """Hello! I'm OPIA, your friendly and knowledgeable AI assistant created to help you with a wide range of tasks and answer your questions, especially in the medical and pharmaceutical fields.  
    My purpose is to assist you efficiently and accurately, ensuring you receive the best possible information and support."""
    st.sidebar.text_area("", animated_text, height=len(animated_text)*2//2+1, disabled=True)

    # Add space to push buttons to the bottom
    for _ in range(20):
        st.sidebar.empty()

    logo_path = "optichain logo.png"  # Replace with your logo file path
    st.sidebar.image(logo_path, use_column_width=True)

    title_text = "Opia will assist you. Feel free to ask him."
    st.title(title_text, anchor=False)

if __name__ == '__main__':
    run_animations()