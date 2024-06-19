import pathlib
import os
import google.generativeai as genai
from pdf2image import convert_from_path
import io
from PIL import Image

# Configure your API key as an environment variable
genai.configure(api_key=os.getenv('API_KEY'))

# Choose a model that's appropriate for your use case
model = genai.GenerativeModel('gemini-1.5-flash')

# Load the PDF file
pdf_path = pathlib.Path('data/conta.pdf')
if not pdf_path.exists():
    raise FileNotFoundError(f"PDF file not found: {pdf_path}")

# Convert PDF to images
pages = convert_from_path(str(pdf_path))

# Save images to bytes
images_data = []
for page in pages:
    img_byte_arr = io.BytesIO()
    page.save(img_byte_arr, format='PNG')
    images_data.append(img_byte_arr.getvalue())

# Prepare data for the model
prompt = """
Extraia os seguintes valores da imagem:
- Valor total da conta de luz.
- Consumo (kWh) do Mês atual.
- Data de vencimento.
- Conta Mês
"""
pdf_data = [{'mime_type': 'image/png', 'data': img} for img in images_data]

# Generate content using the model
response = model.generate_content([prompt] + pdf_data)

# Print the response text
if hasattr(response, 'text'):
    print(response.text)
else:
    print("No text found in the response.")
