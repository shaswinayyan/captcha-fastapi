from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
import io
import re

app = FastAPI()

EMAIL = "23f1000266@ds.study.iitm.ac.in"

@app.post("/captcha")
async def solve_captcha(file: UploadFile = File(...)):
    try:
        # Read uploaded image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))

        # OCR to get text
        text = pytesseract.image_to_string(image)

        # Extract multiplication numbers using regex
        match = re.search(r"(\d{8})\s*[\*x×]\s*(\d{8})", text.replace(",", ""))
        if not match:
            return JSONResponse(status_code=400, content={"error": "Couldn't detect valid equation"})

        num1, num2 = int(match.group(1)), int(match.group(2))
        result = num1 * num2

        return {"answer": result, "email": EMAIL}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
