import streamlit as st
import pdfplumber
import google.generativeai as genai

# Configure Gemini API
API_KEY = "AIzaSyB7_NrE5fs9CK9vUIrHwFGit--pLM58Opg"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    return text

# Function to generate flashcards using Gemini API
def generate_flashcards(content, num_cards):
    prompt = f"""
    Generate {num_cards} flashcards based on the following content:
    
    {content}
    
    Each flashcard should be formatted as follows:
    
    Flashcard 1:
    Front: <Question>
    Back: <Answer>
    
    Flashcard 2:
    Front: <Question>
    Back: <Answer>
    
    Ensure each flashcard starts with 'Front:' and 'Back:' on separate lines.
    """
    
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.title("🃏 AI Flashcard Generator")
st.write("Generate flashcards from uploaded notes (PDF) or enter a topic.")

# Flashcard generation option
option = st.radio("Select an option:", ["Upload Notes (PDF)", "Enter Topic Manually"])

content = ""

if option == "Upload Notes (PDF)":
    uploaded_file = st.file_uploader("Upload your PDF notes", type=["pdf"])
    
    if uploaded_file:
        st.success("File uploaded successfully!")
        with st.spinner("Extracting text..."):
            content = extract_text_from_pdf(uploaded_file)
        if content:
            st.text_area("Extracted Notes", content, height=200)
        else:
            st.error("Could not extract text from the PDF. Try another file.")

elif option == "Enter Topic Manually":
    content = st.text_input("Enter a topic:")

# Select number of flashcards
num_flashcards = st.slider("Number of flashcards:", min_value=3, max_value=20, value=5)

# Generate flashcards
if st.button("Generate Flashcards"):
    if content:
        with st.spinner("Generating flashcards..."):
            flashcards = generate_flashcards(content, num_flashcards)

        st.subheader("📚 Flashcards:")
        flashcard_list = flashcards.split("\n\n")  # Splitting flashcards

        for card in flashcard_list:
            if "Front:" in card and "Back:" in card:
                front, back = card.split("Back:")  # Splitting front and back
                st.markdown(f"**{front.strip()}**")  # Display Front
                st.markdown(f"**Back:** {back.strip()}")  # Display Back
                st.markdown("---")  # Separator between flashcards
    else:
        st.error("Please upload a PDF or enter a topic!")
