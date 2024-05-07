import os
import cv2
import easyocr
import concurrent.futures

def extract_text(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use EasyOCR to extract text from the image
    reader = easyocr.Reader(['en'])  # Language parameter can be adjusted as needed
    result = reader.readtext(gray_image)

    # Extracted text
    extracted_text = ' '.join([text[1] for text in result])
    

    return os.path.basename(image_path), extracted_text

if __name__ == "__main__":
    # Get list of files in current directory
    files = os.listdir('.')
    # Filter out image files (you can adjust the image extensions as needed)
    image_files = [f for f in files if f.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
    
    if not image_files:
        print("No image files found in the current directory.")
    else:
        # Open output.txt file for writing
        with open('output.txt', 'w', encoding='utf-8') as file:
            # Use concurrent.futures.ThreadPoolExecutor to multithread OCR processing
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Submit OCR tasks for each image
                futures = {executor.submit(extract_text, image_path): image_path for image_path in image_files}
                # Process completed OCR tasks
                for future in concurrent.futures.as_completed(futures):
                    image_path, extracted_text = future.result()
                    # Print image title
                    file.write(f"{image_path}\n\n")
                    # Split extracted text into words and write each word on a new line
                    words = extracted_text.split()
                    for word in words:
                        file.write(word + '\n')
                    file.write('\n')
        
        print("Extracted words from all images in the current directory have been written to output.txt.")
