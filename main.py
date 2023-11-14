from flask import Flask, request, render_template, jsonify,redirect, url_for
import os
import openai
from pdf_reader import get_text_from_pdf
from  mind_map_creator import generate_mind_map_json
import requests as req
import re
app = Flask(__name__)
openai.api_key = '<api_key>'

messages = [
    {"role": "system", "content": "For every question I ask from now, give every answer in less than 100 words and in a paragraph. Not even one word above 100."}
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, ' ', text)

app.config['UPLOAD_FOLDER'] = 'uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.mkdir(app.config['UPLOAD_FOLDER'])
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST','GET'])
def submit():
    user_input = request.form['message']
    message = user_input
    conversation = [message]

    try:
        file_path = "output.txt"
        file_content = ""
        with open(file_path, 'r') as file:
            file_content = file.read()
    except:
        file_content=""

    messages.append({"role": "user", "content": " now only answer questions from this please if the question I'm asking is not here say data not available"+file_content + "|"})
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo-1106", messages=messages)

    if message:
        messages.append({"role": "user", "content": message})
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo-1106", messages=messages)
        reply = chat['choices'][0]['message']['content']
        print(reply)
        messages.append({"role": "assistant", "content": reply})
        conversation.append(reply)
        return render_template("chat.html", messages = conversation)

    else:
        return render_template("chat.html")

@app.route('/chat', methods=['POST','GET'])
def chat():
    return render_template("chat.html")

@app.route('/upload', methods=['POST','GET'])
def upload_file():

    if 'file' not in request.files:
        data = request.form["url"]
        try:
            data = data.split("?v=")[1]
            data = data.split("&")[0]
        except:
            return render_template("index.html", message="Invalid Link")
        # print(data)
        response = req.get("https://youtubetranscript.com/?server_vid2="+data)
        print("https://youtubetranscript.com/?server_vid2="+data)
        # print(response.text)
        # print(remove_html_tags(response.text))
        print("yt transcript received")

        message = remove_html_tags(response.text)
        transcript = message.replace("&apos;","'")

        summary = generate_mind_map_json(transcript)

        print("mind map generated")

        limited_content = transcript[:4000]

        file_path = "output.txt"

        with open(file_path, 'w') as file:
            file.write(limited_content)

        print("mind map generated")
        image = True

        try:
            short_summary=summary['Summary']
        except:
            short_summary =summary['summary']

        return render_template("index.html", message=f"{short_summary}", image=image)

    file = request.files['file']

    if file.filename == '':
        return render_template("index.html", message="No file selected")

    if file and allowed_file(file.filename):
        try:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        except:
            return "Error while uploading file"

        message = get_text_from_pdf(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        limited_content = message[:4000]

        file_path = "output.txt"

        with open(file_path, 'w') as file:
            file.write(limited_content)

        print("mind map generated")

        summary = generate_mind_map_json(message)

        image = True

        try:
            short_summary=summary['Summary']
        except:
            short_summary =summary['summary']

        return render_template("index.html", message=f"{short_summary}", image=image)



            # return jsonify({"response": reply})


    return 'Invalid file format.'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
