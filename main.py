from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import google.generativeai as genai
from PIL import Image

# Configure Google Generative AI
genai.configure(api_key="AIzaSyDsew44Tp85JUa_w980KOLojgVxCJjEJHw")

app = FastAPI()

@app.post("/classify-image")
async def classify_image(file: UploadFile = File(...)):
    # Save the uploaded file to a temporary location
    temp_file_path = f"{file.filename}"
    with open(temp_file_path, "wb") as f:
        f.write(await file.read())
    
    # Open the image file
    img = Image.open(temp_file_path)
    
    # Use Google Generative AI model for image classification
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(["Determine the type of image if it is (CT), (MRI), or (X-ray) or (not).", img], stream=True)

    # Return the result as JSON
    return JSONResponse(content={"classification": response.text})
