from PIL import Image, ImageOps, ImageFilter
import pytesseract
from io import BytesIO
import fitz

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

pdf_path = 'image_path\scan.pdf'
output_file = 'source_documents\output.txt'

# Integrate OCR
def extract_text_from_image(image):

    #extracted_text = pytesseract.image_to_string(image)
    #return extracted_text
    return pytesseract.image_to_string(image)

# Image Preprocessing
def preprocess_image(image):
    #image = Image.open(image)
    # Convert to grayscale
    image = image.convert('L')
    # Enhance contrast
    image = ImageOps.autocontrast(image)
    # Apply Gaussian blur to reduce noise
    image = image.filter(ImageFilter.GaussianBlur(radius=1))
    return image


pdf_document = fitz.open(pdf_path)
extracted_text = ''
    
for page_num in range(pdf_document.page_count):
    page = pdf_document[page_num]
    image_list = page.get_images(full=True)
        
    for img_index, img in enumerate(image_list):
        xref = img[0]
        base_image = pdf_document.extract_image(xref)
            
        image = Image.open(BytesIO(base_image["image"]))
        preprocessed_image = preprocess_image(image)
        text = extract_text_from_image(preprocessed_image)
        extracted_text += text
    
pdf_document.close()
    #return extracted_text

    
    #extracted_text = extract_text_from_pdf(pdf_path)
    #print("Text extracted and saved to extracted_text.txt")
    #print(extracted_text)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(extracted_text)

print("Text extracted and saved to", output_file)

# Path to the Tesseract executable (update this to your installation path)