import fitz
import os
import pytesseract
from PIL import Image
import io

folder = "docs"
all_text = ""

for file in os.listdir(folder):
    if file.endswith(".pdf"):
        path = os.path.join(folder, file)
        doc = fitz.open(path)

        print("Reading:", file)

        for page_num, page in enumerate(doc, start=1):
            text = page.get_text("text")
            all_text += f"\n--- PAGE {page_num} ---\n{text}\n"

            for img in page.get_images(full=True):
                xref = img[0]
                base = doc.extract_image(xref)
                image_bytes = base["image"]

                image = Image.open(io.BytesIO(image_bytes))
                ocr = pytesseract.image_to_string(image)

                if ocr.strip():
                    all_text += "\n[OCR IMAGE TEXT]\n" + ocr + "\n"

with open("content.txt", "w", encoding="utf-8") as f:
    f.write(all_text)

print("Saved content.txt")
print("Characters:", len(all_text))