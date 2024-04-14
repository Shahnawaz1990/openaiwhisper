from flask import Flask, request, redirect, url_for, jsonify, render_template
import os
from openai import OpenAI
client = OpenAI()

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        language = request.form['language']
        file = request.files['file']
        if file:
            filename = file.filename
        try:
          file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        except Exception as e:
          print("An error occurred while saving the file:", e)

        audio_file= open(filename, "rb")
        transcript = client.audio.translations.create(model="whisper-1", file=audio_file)
        response = client.chat.completions.create(
                    model="gpt-4",
                    messages = [{ "role": "system", "content": f"You will be provided with a sentence in English, and your task is to translate it into {language}" }, { "role": "user", "content": transcript.text }],
                    temperature=0,
                    max_tokens=256
                  )
        return response.choices[0].message.content


            # return redirect(url_for('uploaded_file', filename=filename))
            # return redirect(url_for('uploaded_file', filename=filename))
    return render_template('index.html')

# @app.route('/static/<filename>')
# def uploaded_file(filename):
#     return 'file uploaded successfully'

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
