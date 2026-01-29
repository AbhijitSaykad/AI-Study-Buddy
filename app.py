import streamlit as st
from utils.study_engine import generate_study_content
from fpdf import FPDF
import os

# 1. Page Configuration for a Modern Look
st.set_page_config(page_title="AI Study Buddy", page_icon="📘", layout="wide")

# 2. Session State Initialization
if "study_data" not in st.session_state:
    st.session_state.study_data = None
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

# 3. Sidebar for Controls
with st.sidebar:
    st.header("⚙️ Controls")
    topic = st.text_input("Enter Topic / Question", placeholder="e.g. Photosynthesis")
    
    if st.button("🚀 Generate Content", use_container_width=True):
        if topic.strip():
            with st.spinner("Generating..."):
                st.session_state.study_data = generate_study_content(topic)
                st.session_state.quiz_submitted = False # Reset quiz for new topic
        else:
            st.warning("Please enter a topic.")

    st.markdown("---")
    if st.button("🧹 Clear History", use_container_width=True):
        st.session_state.study_data = None
        st.session_state.quiz_submitted = False
        st.rerun()

# 4. Main Display Area
st.title("📘 AI-Powered Study Buddy")

if st.session_state.study_data:
    data = st.session_state.study_data
    
    # Use tabs to organize content clearly
    tab1, tab2, tab3 = st.tabs(["📖 Explanation", "📝 Notes", "🧠 Quiz"])
    
    with tab1:
        st.subheader("Deep Dive Explanation")
        st.write(data["explanation"])
    
    with tab2:
        st.subheader("Key Takeaways")
        st.markdown(data["notes"])
        
        # PDF Download Section inside Notes tab
        # Modified PDF function for 2026 library standards
        def create_pdf(explanation, notes):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Study Notes", ln=1, align='C')
            pdf.ln(10)
            
            # Clean text to remove any characters that cause encoding errors
            clean_exp = explanation.encode('latin-1', 'ignore').decode('latin-1')
            clean_notes = notes.encode('latin-1', 'ignore').decode('latin-1')
            
            pdf.multi_cell(0, 10, txt=f"Explanation:\n{clean_exp}\n\nNotes:\n{clean_notes}")
            
            # Use bytearray conversion for Streamlit compatibility
            return bytes(pdf.output())

        # Logic to handle the download
        try:
            pdf_bytes = create_pdf(data["explanation"], data["notes"])
            
            st.download_button(
                label="📥 Download as PDF",
                data=pdf_bytes,  # This must be a 'bytes' object
                file_name=f"study_notes.pdf",
                mime="application/pdf",
                key="download_pdf_btn"
            )
        except Exception as e:
            st.error(f"PDF Error: {str(e)}")

    

    with tab3:
        st.subheader("Test Your Knowledge")
        q_raw = data["quiz_raw"]
        
        # Simple parsing (Assumes format: Question... Options... Correct: X)
        if "Correct:" in q_raw:
            parts = q_raw.split("Correct:")
            question_and_options = parts[0]
            correct_answer = parts[1].strip()
            
            st.write(question_and_options)
            user_choice = st.radio("Select your answer:", ["A", "B", "C", "D"], key="user_quiz_choice")
            
            if st.button("Submit Answer"):
                st.session_state.quiz_submitted = True
            
            if st.session_state.quiz_submitted:
                if user_choice in correct_answer:
                    st.success(f"🎉 Correct! The answer is {correct_answer}")
                else:
                    st.error(f"❌ Incorrect. The correct answer is {correct_answer}")
else:
    st.info("👈 Enter a topic in the sidebar to get started!")