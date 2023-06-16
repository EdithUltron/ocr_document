from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import cv2
import pytesseract
from pytesseract import Output
import pandas as pd
import os
from pdf2image import convert_from_path

app = Flask(__name__)

# Configure upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_image(file):
    # Load and preprocess the image
    img = cv2.imread(file)
    img = cv2.resize(img, (int(img.shape[1] + (img.shape[1] * .1)),
                           int(img.shape[0] + (img.shape[0] * .25))),
                     interpolation=cv2.INTER_AREA)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    custom_config = r'-l eng --oem 3 --psm 6 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-:.$%./@& *"'
    d = pytesseract.image_to_data(img_rgb, config=custom_config, output_type=Output.DICT)
    df = pd.DataFrame(d)

    # Clean up blanks
    df1 = df[(df.conf != '-1') & (df.text != ' ') & (df.text != '')]

    # Sort blocks vertically
    sorted_blocks = df1.groupby('block_num').first().sort_values('top').index.tolist()
    text = ''
    for block in sorted_blocks:
        curr = df1[df1['block_num'] == block]
        sel = curr[curr.text.str.len() > 3]
        char_w = (sel.width / sel.text.str.len()).mean()
        prev_par, prev_line, prev_left = 0, 0, 0
        for ix, ln in curr.iterrows():
            # Add new line when necessary
            if prev_par != ln['par_num']:
                text += '\n'
                prev_par = ln['par_num']
                prev_line = ln['line_num']
                prev_left = 0
            elif prev_line != ln['line_num']:
                text += '\n'
                prev_line = ln['line_num']
                prev_left = 0

            added = 0  # Num of spaces that should be added
            if ln['left'] / char_w > prev_left + 1:
                added = int((ln['left']) / char_w) - prev_left
                text += ' ' * added
            text += ln['text'] + ' '
            prev_left += len(ln['text']) + added + 1
        text += '\n'

    return text

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the POST request has a file part
        if 'file' not in request.files:
            return render_template('index.html', error='No file selected.')
        
        file = request.files['file']
        
        # Check if the file is allowed and has a filename
        if file.filename == '':
            return render_template('index.html', error='No file selected.')
        
        if file and allowed_file(file.filename):
            # Save the file to the upload folder
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            if file_path.split('.')[-1].lower() == 'pdf':
                text = extract_text_from_pdf(file_path)
            else:
                text = extract_text_from_image(file_path)            
            
            # Render the result page with the extracted text
            return render_template('result.html', text=text)
        else:
            return render_template('index.html', error='Invalid file format.')
    
    return render_template('index.html')

def extract_text_from_pdf(file):
    pdfs = file
    pages = convert_from_path(pdfs, 350)

    text=''
    i = 1
    for page in pages:
        text+=str(i)+" . \n"
        image_name = "Page_" + str(i) + ".jpg"  
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
        page.save(image_path, "JPEG")
        text+=extract_text_from_image(image_path)
        text+="\n"
        i = i+1  
    
    return text

if __name__ == '__main__':
    app.run(debug=True)
