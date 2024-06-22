from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import google.generativeai as genai
from PIL import Image

# Configure Google Generative AI
genai.configure(api_key="AIzaSyAFAmVIP6l33PQUj5G0Yk05RyH9u42g1gg")
model = genai.GenerativeModel('gemini-pro')

app = FastAPI()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Open the uploaded file
        image = Image.open(file.file)
        
        # Since the AI model might need raw bytes, we will directly read the file content
    
        
        # Generate the AI response
        response = model.generate_content(["choose the type of image only if it is CT, MRI, or X-ray or not select  only one  and not explain anything   .", image], stream=True)
        response.resolve()
        
        # Extract and return the response text
        return {"image_type": response.text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {e}")
