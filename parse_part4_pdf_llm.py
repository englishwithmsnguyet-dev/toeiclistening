import fitz # PyMuPDF
import sys
import os
import google.generativeai as genai

# Setup your Gemini API key (Ensure this is set in your environment before running)
# export GEMINI_API_KEY="YOUR_API_KEY"

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY environment variable not set.")
    sys.exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-pro-latest')

pdf_path = 'TOEIC TEST 2025_ TEST 1.pdf'
doc = fitz.open(pdf_path)

print("Extracting images from pages 10 to 30...")
images = []
for i in range(10, min(30, doc.page_count)):
    page = doc[i]
    pix = page.get_pixmap(dpi=150)
    img_bytes = pix.tobytes("png")
    
    import io
    from PIL import Image
    image = Image.open(io.BytesIO(img_bytes))
    images.append(image)

print(f"Extracted {len(images)} images. Sending to Gemini for parsing...")

prompt = """
Look at these pages from a TOEIC Listening test. Find "PART 4".
Extract all the questions and choices for Part 4 exactly as they appear.
Format the output as a JSON array of objects, where each object represents a question set (e.g. 71-73) and contains:
- q_num: "71-73"
- questions: array of question objects, each with:
  - id: integer (e.g., 71)
  - question: string
  - choices: object with keys "A", "B", "C", "D" and their string values.

Return ONLY the raw JSON array.
"""

try:
    response = model.generate_content([prompt] + images)
    print("Response from Gemini:")
    print(response.text)
except Exception as e:
    print(f"Error calling Gemini: {e}")
