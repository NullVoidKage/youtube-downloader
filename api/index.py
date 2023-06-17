import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from flask import Flask, render_template, request, redirect, url_for, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    link = request.form['link']
    try:
        yt = YouTube(link)
        stream = yt.streams.get_highest_resolution()
        filename = f"{yt.title}.mp4"
        file_path = os.path.join(app.root_path, 'downloads', filename)
        stream.download(output_path=file_path)
        return redirect(url_for('success', filename=filename))
    except Exception as e:
        return render_template('index.html', error=str(e))

@app.route('/success/<filename>')
def success(filename):
    file_path = os.path.join(app.root_path, 'downloads', filename)
    return send_file(
        file_path,
        attachment_filename=filename,
        as_attachment=True
    )

os.makedirs(os.path.join(app.root_path, 'downloads'), exist_ok=True)
 
if __name__ == '__main__':
    app.run()
