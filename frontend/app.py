import streamlit as st
import requests


# Streamlit UI
st.title("LLM Prompt Tuning Interface")
st.write("Adjust parameters and see how they affect AI-generated responses.")

# Layout: Two columns for knobs
col1, col2 = st.columns(2)

with col1:
    temperature = st.number_input("Temperature (0.0 - 1.0)", 0.0, 1.0, 0.7, step=0.01, key="temp", help="Controls randomness. Lower = more predictable responses.")
    top_p = st.number_input("Top-P (0.0 - 1.0)", 0.0, 1.0, 0.9, step=0.01, key="top_p", help="Nucleus sampling. Lower = more focused responses.")
    top_k = st.number_input("Top-K (0 - 100)", 0, 100, 50, step=1, key="top_k", help="Limits choices to top-K most probable words.")

with col2:
    max_tokens = st.number_input("Max Tokens (50 - 500)", 50, 500, 100, step=10, key="max_tokens", help="Maximum number of words in response.")
    frequency_penalty = st.number_input("Frequency Penalty (0.0 - 2.0)", 0.0, 2.0, 0.0, step=0.1, key="freq_penalty", help="Penalizes frequent words. Higher = more unique words.")
    presence_penalty = st.number_input("Presence Penalty (0.0 - 2.0)", 0.0, 2.0, 0.0, step=0.1, key="presence_penalty", help="Encourages new words. Higher = more diverse responses.")

# User Input Box
prompt = st.text_area("Enter your prompt:", "Tell me a story about AI.")

# Submit Button
if st.button("Generate Response"):
    backend_url = "http://127.0.0.1:5000/api/generate"  # Update if deployed
    payload = {
        "input": prompt,
        "settings": {
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_tokens": max_tokens,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
        }
    }
    
    response = requests.post(backend_url, json=payload)
    
    if response.status_code == 200:
        st.subheader("Generated Response:")
        st.write(response.json()["response"])
    else:
        st.error("Error generating response. Check backend.")