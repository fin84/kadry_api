from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import google.generativeai as genai
from PIL import Image
import io

app = FastAPI()


genai.configure(api_key="AIzaSyDsew44Tp85JUa_w980KOLojgVxCJjEJHw")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
     
        image = Image.open(io.BytesIO(await file.read()))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image file")

   
    image_bytes = io.BytesIO()
    image.save(image_bytes, format=image.format)
    image_bytes = image_bytes.getvalue()

  
    model = genai.GenerativeModel('gemini-1.5-flash')

    
    response = model.generate_content(["Determine the type of image if it is (CT), (MRI), or (X-ray) or (not).", image_bytes], stream=True)
    response.resolve()

    result = response.text

    return JSONResponse(content={"classification": result})
