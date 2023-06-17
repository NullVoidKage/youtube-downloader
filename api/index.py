import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from flask import Flask, request, redirect, url_for
from pytube import YouTube

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    link = request.form['link']
    try:
        yt = YouTube(link)
        stream = yt.streams.get_highest_resolution()
        filename = f"{yt.title}.mp4"
        stream.download(filename)
        return redirect(url_for('success'))
    except Exception as e:
        return str(e)

@app.route('/success')
def success():
    return 'Download successful!'

# This route is for Vercel's health check
@app.route('/api/health')
def health():
    return 'OK'

# This route is for any other requests
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
