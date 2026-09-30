import streamlit as st
import requests
import pytesseract
import fitz
from PIL import Image
import io


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="StudyLens AI",
    page_icon="📚",
    layout="wide"
)

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
OLLAMA_URL = "http://localhost:11434/api/generate"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 0px;
}

.subtitle {
    font-size: 18px;
    color: #666;
    margin-bottom: 25px;
}

.card {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #ddd;
    margin-bottom: 15px;
}

.success-box {
    padding: 12px;
    border-radius: 8px;
    background-color: #e8f5e9;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = ""

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = None

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False


# ============================================================
# FUNCTIONS
# ============================================================

def check_tesseract():
    try:
        version = pytesseract.get_tesseract_version()
        return True, str(version)
    except Exception as e:
        return False, str(e)


def extract_text_from_image(image):
    try:
        image = image.convert("RGB")

        text = pytesseract.image_to_string(
            image,
            config="--psm 6"
        )

        return text.strip()

    except Exception as e:
        return f"OCR Error: {str(e)}"


def extract_text_from_pdf(uploaded_file):

    try:
        pdf_bytes = uploaded_file.read()

        document = fitz.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        text = ""

        for page_number, page in enumerate(document):

            page_text = page.get_text()

            if page_text.strip():
                text += f"\n\n--- Page {page_number + 1} ---\n"
                text += page_text

            else:
                # OCR scanned PDF page
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

                image = Image.open(
                    io.BytesIO(pix.tobytes("png"))
                )

                ocr_text = extract_text_from_image(image)

                text += f"\n\n--- Page {page_number + 1} ---\n"
                text += ocr_text

        document.close()

        return text.strip()

    except Exception as e:
        return f"PDF Error: {str(e)}"


def extract_text(uploaded_file):

    file_type = uploaded_file.type

    if file_type == "text/plain":

        try:
            return uploaded_file.read().decode("utf-8")

        except Exception as e:
            return f"TXT Error: {str(e)}"

    elif file_type == "application/pdf":

        return extract_text_from_pdf(uploaded_file)

    elif file_type.startswith("image/"):

        image = Image.open(uploaded_file)

        return extract_text_from_image(image)

    else:

        return "Unsupported file type."


def ask_ollama(prompt, model_name):

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )

        if response.status_code != 200:

            return (
                f"Ollama Error: HTTP {response.status_code}\n\n"
                f"{response.text}"
            )

        data = response.json()

        return data.get(
            "response",
            "No response received from Ollama."
        )

    except requests.exceptions.ConnectionError:

        return (
            "Cannot connect to Ollama.\n\n"
            "Make sure Ollama is running."
        )

    except requests.exceptions.Timeout:

        return (
            "Ollama request timed out.\n"
            "Try using a shorter note."
        )

    except Exception as e:

        return f"Ollama Error: {str(e)}"


def explain_notes(text, model):

    prompt = f"""
You are StudyLens AI, an educational assistant.

Explain the following study material in simple language.

Requirements:
- Use simple English.
- Explain important concepts.
- Give examples where useful.
- Use headings and bullet points.
- Make it suitable for a college student.
- Do not add unrelated information.

STUDY MATERIAL:

{text}
"""

    return ask_ollama(prompt, model)


def summarize_notes(text, model):

    prompt = f"""
You are StudyLens AI.

Create concise revision notes from the following study material.

Requirements:
- Identify the most important points.
- Use bullet points.
- Include important definitions.
- Keep the answer easy to revise before an exam.
- Do not include unrelated information.

STUDY MATERIAL:

{text}
"""

    return ask_ollama(prompt, model)


def generate_quiz(text, model, number_of_questions):

    prompt = f"""
You are StudyLens AI.

Create exactly {number_of_questions} multiple-choice questions
from the study material below.

For every question use this format:

QUESTION 1:
Question text

A) option
B) option
C) option
D) option

ANSWER: A

QUESTION 2:
...

Important:
- Questions must be based ONLY on the supplied study material.
- Each question must have exactly four options.
- Only one option should be correct.
- Keep questions suitable for college students.

STUDY MATERIAL:

{text}
"""

    return ask_ollama(prompt, model)


def answer_question(text, question, model):

    prompt = f"""
You are StudyLens AI.

Answer the student's question using ONLY the supplied study material.

If the answer is not present in the material, clearly say:
"The answer is not available in the uploaded notes."

Give a simple and understandable explanation.

STUDY MATERIAL:

{text}

STUDENT QUESTION:

{question}
"""

    return ask_ollama(prompt, model)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">📚 StudyLens AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your AI-powered study assistant using OCR + Local Ollama'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Settings")

    model_name = st.text_input(
        "Ollama Model",
        value="llama3.2:3b"
    )

    number_of_questions = st.slider(
        "Quiz Questions",
        min_value=3,
        max_value=10,
        value=5
    )

    st.divider()

    st.subheader("System Status")

    tesseract_ok, tesseract_info = check_tesseract()

    if tesseract_ok:

        st.success("✅ Tesseract OCR Ready")

    else:

        st.error("❌ Tesseract OCR Error")

    st.info(
        "🤖 AI runs locally through Ollama."
    )

    st.divider()

    if st.button("🗑️ Clear Session"):

        st.session_state.extracted_text = ""
        st.session_state.quiz_data = ""
        st.session_state.quiz_score = None
        st.session_state.quiz_submitted = False

        st.rerun()


# ============================================================
# FILE UPLOAD
# ============================================================

st.subheader("📂 Upload Study Material")

uploaded_file = st.file_uploader(
    "Upload an image, PDF, or TXT file",
    type=["png", "jpg", "jpeg", "pdf", "txt"]
)


if uploaded_file:

    st.info(
        f"Selected file: {uploaded_file.name}"
    )

    if st.button("🔍 Extract Study Material"):

        with st.spinner("Extracting text..."):

            extracted = extract_text(uploaded_file)

            st.session_state.extracted_text = extracted

        if extracted.startswith(
            ("OCR Error", "PDF Error", "TXT Error")
        ):

            st.error(extracted)

        else:

            st.success(
                "✅ Study material extracted successfully!"
            )


# ============================================================
# MANUAL TEXT
# ============================================================

st.subheader("✍️ Or Enter Notes Manually")

manual_text = st.text_area(
    "Paste your study material here",
    height=150,
    placeholder="Paste notes, definitions, textbook content, etc."
)

if st.button("📥 Use Manual Text"):

    if manual_text.strip():

        st.session_state.extracted_text = manual_text.strip()

        st.success(
            "Manual text loaded successfully!"
        )

    else:

        st.warning(
            "Please enter some text first."
        )


# ============================================================
# DISPLAY EXTRACTED TEXT
# ============================================================

if st.session_state.extracted_text:

    st.divider()

    st.subheader("📄 Study Material")

    with st.expander(
        "View extracted material",
        expanded=False
    ):

        st.text_area(
            "Extracted Text",
            st.session_state.extracted_text,
            height=250
        )

    text_length = len(
        st.session_state.extracted_text
    )

    st.caption(
        f"Characters extracted: {text_length}"
    )


# ============================================================
# AI FEATURES
# ============================================================

if st.session_state.extracted_text:

    st.divider()

    st.subheader("🧠 AI Study Tools")

    col1, col2, col3 = st.columns(3)

    # --------------------------------------------------------
    # EXPLAIN
    # --------------------------------------------------------

    with col1:

        if st.button(
            "💡 Explain",
            use_container_width=True
        ):

            with st.spinner(
                "Generating explanation..."
            ):

                result = explain_notes(
                    st.session_state.extracted_text,
                    model_name
                )

            st.session_state.explanation = result

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    with col2:

        if st.button(
            "📝 Summarize",
            use_container_width=True
        ):

            with st.spinner(
                "Creating summary..."
            ):

                result = summarize_notes(
                    st.session_state.extracted_text,
                    model_name
                )

            st.session_state.summary = result

    # --------------------------------------------------------
    # QUIZ
    # --------------------------------------------------------

    with col3:

        if st.button(
            "❓ Generate Quiz",
            use_container_width=True
        ):

            with st.spinner(
                "Generating quiz..."
            ):

                result = generate_quiz(
                    st.session_state.extracted_text,
                    model_name,
                    number_of_questions
                )

            st.session_state.quiz_data = result
            st.session_state.quiz_score = None
            st.session_state.quiz_submitted = False


# ============================================================
# EXPLANATION
# ============================================================

if "explanation" in st.session_state:

    st.divider()

    st.subheader("💡 Explanation")

    st.markdown(
        st.session_state.explanation
    )


# ============================================================
# SUMMARY
# ============================================================

if "summary" in st.session_state:

    st.divider()

    st.subheader("📝 Revision Summary")

    st.markdown(
        st.session_state.summary
    )


# ============================================================
# QUIZ
# ============================================================

if st.session_state.quiz_data:

    st.divider()

    st.subheader("❓ AI Generated Quiz")

    st.markdown(
        st.session_state.quiz_data
    )

    st.info(
        "The questions and answers above are generated "
        "from your uploaded study material."
    )


# ============================================================
# ASK YOUR NOTES
# ============================================================

if st.session_state.extracted_text:

    st.divider()

    st.subheader("💬 Ask Your Notes")

    question = st.text_input(
        "Ask a question about your uploaded material",
        placeholder="Example: What is a microcontroller?"
    )

    if st.button(
        "🔎 Ask AI",
        use_container_width=False
    ):

        if question.strip():

            with st.spinner(
                "Searching your notes..."
            ):

                answer = answer_question(
                    st.session_state.extracted_text,
                    question,
                    model_name
                )

            st.markdown("### 🤖 Answer")

            st.markdown(answer)

        else:

            st.warning(
                "Please enter a question."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "StudyLens AI • OCR + Local AI • "
    "Built with Python, Streamlit, Tesseract and Ollama"
)