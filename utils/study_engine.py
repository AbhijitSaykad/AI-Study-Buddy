import os
import streamlit as st
from google import genai

# Get API key from Streamlit Secrets (Cloud) or env (local)
api_key = st.secrets.get("GENAI_API_KEY") or os.getenv("GENAI_API_KEY")

if not api_key:
    raise ValueError("GENAI_API_KEY not found. Add it to Streamlit Secrets.")

# Initialize the client
client = genai.Client(api_key=api_key)

def generate_study_content(topic):
    prompt = f"""
Provide study material for '{topic}'. 
Format your response EXACTLY with '|||' as the separator:
[Explanation: 3 sentences]
|||
[Notes: 3 bullet points]
|||
[Quiz: Question 1, followed by 4 options A,B,C,D, then 'Correct: [Option Letter]']
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        parts = response.text.split("|||")

        return {
            "explanation": parts[0].strip() if len(parts) > 0 else "No explanation provided.",
            "notes": parts[1].strip() if len(parts) > 1 else "No notes provided.",
            "quiz_raw": parts[2].strip() if len(parts) > 2 else "No quiz provided."
        }

    except Exception as e:
        return {"error": str(e)}
