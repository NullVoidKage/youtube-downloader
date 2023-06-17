import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from pytube import YouTube
import os

app = Flask(__name__)
DOWNLOADS_DIR = 'downloads'  # Directory to store downloaded videos

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
        filepath = os.path.join(DOWNLOADS_DIR, filename)
        stream.download(output_path=DOWNLOADS_DIR, filename=filename)
        return redirect(url_for('success', filename=filename))
    except Exception as e:
        return render_template('index.html', error=str(e))

@app.route('/success/<filename>')
def success(filename):
    return send_from_directory(DOWNLOADS_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run()
