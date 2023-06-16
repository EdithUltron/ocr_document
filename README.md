
# Flask Text Extraction Web Application
# ocr_document
## PDF and Images Data Extraction and Rapid Prototyping

This is a Flask-based web application that allows users to upload PDF or image files and extract text from them using optical character recognition (OCR). The extracted text is then displayed on the web page.

## Application URL

The application is hosted at: [https://happyhappie.pythonanywhere.com/](https://happyhappie.pythonanywhere.com/)

## Installation

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Create a virtual environment (optional but recommended).
4. Install the required dependencies by running the following command:

`pip install -r requirements.txt`

## Usage

1. Run the Flask application by executing the following command:
`python app.py`

The application will start running on `http://localhost:5000`.

2. Open your web browser and access the application using the above URL.

3. You will see a file upload form where you can select a PDF or image file to extract text from.

4. Click the "Submit" button to upload the file and initiate the text extraction process.

5. After the extraction is complete, the extracted text will be displayed on the web page.

## Approach and Design Choices

The web application is built using Flask, a lightweight and easy-to-use web framework. The frontend is implemented using HTML templates, CSS, and JavaScript, while the backend handles the file upload, text extraction, and rendering of the extracted text.

The OCR functionality is achieved using the pytesseract library, which is a wrapper for Google's Tesseract OCR engine. The uploaded files are processed using OpenCV and converted to the appropriate format for text extraction.

To handle PDF files, the pdf2image library is used to convert each page of the PDF into an image, which is then passed to the text extraction function. This allows the application to extract text from both PDF and image files seamlessly.

The extracted text is displayed on the web page, making it user-friendly and easy to access. The application supports multiple file uploads, allowing users to extract text from multiple files in one session.

## Challenges Faced

- One of the main challenges was extracting the data accurately from the images (OCR Accuracy).

- Other problem is extracting and detecting the tabular data from the normal data.

- I have gone through many articles and none of them gave an accurate solution in detecting the tables of different formats.

## Future Enhancements

- Implementing advanced text preprocessing techniques to improve OCR accuracy.

- Extracting Tabular data accurately.

- Adding support for additional file formats, such as Microsoft Word documents and scanned PDFs.

- Enhancing the UI with additional features like text formatting, search functionality, and text-to-speech capabilities.
