import requests


class StudyLensAI:

    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "llama3.2:3b"

    def generate(self, prompt):
        try:
            response = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )

            response.raise_for_status()

            data = response.json()
            return data.get("response", "").strip()

        except requests.exceptions.ConnectionError:
            return (
                "StudyLens AI is not running.\n\n"
                "Please start Ollama and try again."
            )

        except requests.exceptions.Timeout:
            return "The local AI model took too long to respond."

        except Exception as e:
            return f"AI Error: {str(e)}"

    def explain(self, text):

        if not text.strip():
            return "No study material was provided."

        prompt = f"""
You are StudyLens, an AI tutor for college students.

Analyze the following study material.

Give the answer using this structure:

1. TOPIC
2. SIMPLE EXPLANATION
3. KEY POINTS
4. IMPORTANT TERMS
5. EXAMPLE
6. EXAM-ORIENTED POINTS
7. QUICK SUMMARY

Rules:
- Use simple student-friendly language.
- Explain technical concepts clearly.
- Correct obvious OCR mistakes when the meaning is clear.
- Do not invent information.
- Use bullet points where useful.

STUDY MATERIAL:

{text}
"""

        return self.generate(prompt)

    def summarize(self, text):

        if not text.strip():
            return "No study material was provided."

        prompt = f"""
You are StudyLens.

Summarize the following study material for a college student.

Provide:

1. Main Topic
2. Five Key Points
3. Important Terms
4. Short Summary

Use simple and clear language.

STUDY MATERIAL:

{text}
"""

        return self.generate(prompt)

    def generate_quiz(self, text, number_of_questions=5):

        if not text.strip():
            return "No study material was provided."

        prompt = f"""
You are StudyLens, an AI tutor.

Create {number_of_questions} multiple-choice questions
from the following study material.

For every question provide:

Question:
A.
B.
C.
D.

Correct Answer:
Explanation:

Rules:
- Questions must be based only on the provided material.
- Include easy, medium and difficult questions.
- Avoid duplicate questions.
- Make them useful for exam preparation.

STUDY MATERIAL:

{text}
"""

        return self.generate(prompt)


if __name__ == "__main__":

    print("=" * 60)
    print("StudyLens Local AI Engine")
    print("=" * 60)

    ai = StudyLensAI()

    sample_text = """
    A transistor is a semiconductor device used to amplify
    or switch electronic signals. It has three terminals:
    emitter, base and collector. A small current at the base
    controls a larger current flowing between the collector
    and emitter.
    """

    print("\nTesting local AI...\n")

    result = ai.explain(sample_text)

    print(result)

    print("\n" + "=" * 60)
    print("LOCAL AI ENGINE TEST COMPLETED")
    print("=" * 60)