import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key from the environment
api_key = os.getenv("GENAI_API_KEY")

# Initialize the client using the environment variable
client = genai.Client(api_key=api_key)

def generate_study_content(topic):
    # This prompt strictly defines the structure
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
        # Use gemini-2.5-flash for stable 2026 performance
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