from flask import Flask, request, jsonify
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
from flask import Flask, render_template, request

app = Flask(__name__)
client = genai.Client() # Automatically uses the GEMINI_API_KEY env variable

# The endpoint where the frontend sends the image
@app.route('/')
def index():
    # Renders the HTML file with the form
    return render_template('index.html')
@app.route('/simplify', methods=['POST'])
def simplify_prescription():
    # 1. Get the Base64 image data from the request
    data = request.json
    base64_image_data = data.get('image_data').split(',')[1] # Remove the 'data:image/jpeg;base64,' prefix

    try:
        # 2. Convert Base64 data into a PIL Image object
        image_bytes = base64.b64decode(base64_image_data)
        img = Image.open(BytesIO(image_bytes))

        # 3. Define the Multimodal Prompt
        prompt = (
            "You are a professional medical information translator. Analyze the provided image of a prescription, label, or leaflet. Extract and summarize the key information, including Medication Name, Dosage, Purpose, and Instructions. Present the final output using clear headings, normal professional language, and use Markdown bolding (**word**) for important terms and headings. Do not mention 5th grade or children in the response."
        )

        # 4. Call the Gemini API with BOTH the image and the text prompt
        response = client.models.generate_content(
            model='gemini-2.5-flash', # Fast and effective multimodal model
            contents=[img, prompt]
        )

        # 5. Return the raw AI-generated text to the frontend
        return jsonify({'simplified_text': response.text}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Add debug=True for easier hackathon development
    app.run(debug=True, port=5000)
    
# app.py (Make sure you have this structure)

from flask import Flask, request, jsonify # ... and other imports

app = Flask(__name__) # <-- Gunicorn looks for this variable named 'app'

# ... your @app.route functions ...

if __name__ == '__main__':
    # This section is for local development only and is ignored by Render/Gunicorn
    app.run(debug=True)    