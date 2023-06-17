import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from flask import Flask, render_template, request, redirect, url_for
from pytube import YouTube

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
        stream.download(filename)
        return redirect(url_for('success', filename=filename))
    except Exception as e:
        return render_template('index.html', error=str(e))

@app.route('/success/<filename>')
def success(filename):
    return f'<a href="/api/downloads/{filename}" download>Click here to download the video</a>'

if __name__ == '__main__':
    app.run()
