# 📚 StudyLens AI

> **An AI-powered study assistant that transforms notes, PDFs, and images into understandable explanations, summaries, quizzes, and answers.**

StudyLens AI is an intelligent learning assistant designed to help students understand and revise study materials more efficiently. It combines **OCR, PDF processing, and local AI** to extract content from study materials and provide useful learning assistance.

The application can process **text files, images, and PDF documents**, extract their content, and use a locally running **Ollama LLM** to explain concepts, summarize notes, generate quizzes, and answer questions.

---

## ✨ Features

* 📄 **PDF Text Extraction** — Extract text from digital and scanned PDF documents.
* 🖼️ **OCR Support** — Extract text from handwritten/printed images using Tesseract OCR.
* 📝 **Manual Text Input** — Enter notes directly into the application.
* 🤖 **AI Explanations** — Get easy-to-understand explanations of study material.
* 📋 **Summarization** — Convert lengthy notes into concise summaries.
* 🧠 **Quiz Generation** — Generate multiple-choice questions from study material.
* ❓ **Ask Your Notes** — Ask questions based on the uploaded study content.
* 🔒 **Local AI Processing** — Uses Ollama for local AI inference instead of requiring a paid cloud AI API.
* 💻 **Simple Web Interface** — Built with Streamlit for an easy-to-use interface.
* 📚 **Multiple Input Formats** — Supports TXT, PDF, PNG, JPG, JPEG, and other common image formats.

---

## 🛠️ Technology Stack

| Technology       | Purpose                             |
| ---------------- | ----------------------------------- |
| 🐍 Python        | Core programming language           |
| 🌐 Streamlit     | Web application interface           |
| 🤖 Ollama        | Local AI/LLM inference              |
| 🧠 Llama 3.2     | Local language model                |
| 🔍 Tesseract OCR | Text extraction from images         |
| 📄 PyMuPDF       | PDF processing                      |
| 🖼️ Pillow       | Image processing                    |
| 🌐 Requests      | Communication with local Ollama API |

---

## 🏗️ Project Architecture

```text
StudyLens AI
│
├── app.py
│   └── Main Streamlit application
│
├── ai_engine.py
│   └── Local AI processing and Ollama integration
│
├── core/
│   └── Core application modules
│
├── ui/
│   └── User interface components
│
├── scanned_pages/
│   └── OCR/scanned document content
│
├── study_materials/
│   └── Study notes and learning materials
│
├── requirements.txt
│   └── Python dependencies
│
├── .gitignore
│   └── Git ignored files
│
└── README.md
    └── Project documentation
```

---

## 🔄 How It Works

```text
                ┌─────────────────────┐
                │   Study Material    │
                │                     │
                │ PDF / Image / TXT   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Content Extraction │
                │                     │
                │ PyMuPDF / Tesseract │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   Extracted Notes   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │     Ollama LLM      │
                │    Llama 3.2:3b     │
                └──────────┬──────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
         Explanation    Summary       Quiz
              │            │            │
              └────────────┼────────────┘
                           ▼
                  ┌─────────────────┐
                  │  Student Output │
                  └─────────────────┘
```

---

## ⚙️ Requirements

Before running StudyLens AI, install the following:

* Python 3.10 or later
* Git
* Tesseract OCR
* Ollama
* Llama 3.2 model

---

## 📥 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/masterpooja43-del/StudyLens-AI.git
```

Navigate to the project:

```bash
cd StudyLens-AI
```

---

### 2. Create a Virtual Environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

---

### 3. Install Python Dependencies

```powershell
pip install -r requirements.txt
```

---

## 🔍 Install Tesseract OCR

StudyLens AI uses **Tesseract OCR** to extract text from images and scanned documents.

Install Tesseract OCR and make sure the executable is available at:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

The application is currently configured to use this path.

If Tesseract is installed elsewhere, update the path in `app.py`.

---

## 🤖 Install and Configure Ollama

StudyLens AI uses Ollama to run the AI model locally.

Install Ollama and then download the model:

```powershell
ollama pull llama3.2:3b
```

Check the installed models:

```powershell
ollama list
```

You should see:

```text
llama3.2:3b
```

Make sure Ollama is running before starting the StudyLens application.

---

## ▶️ Run the Application

Start the Streamlit application with:

```powershell
python -m streamlit run app.py
```

Streamlit will provide a local address similar to:

```text
http://localhost:8501
```

Open the address in your web browser.

---

## 📖 How to Use

### Step 1 — Upload Study Material

Upload one of the supported file types:

* PDF
* TXT
* PNG
* JPG
* JPEG

Or enter your study material manually.

### Step 2 — Extract Content

StudyLens AI extracts the text automatically.

For images and scanned PDFs, Tesseract OCR is used when necessary.

### Step 3 — Choose an AI Function

You can use:

**Explain**

Get a simple explanation of the study material.

**Summarize**

Convert lengthy notes into concise revision material.

**Generate Quiz**

Generate multiple-choice questions based on the notes.

**Ask Your Notes**

Ask questions and receive answers based on the extracted study
