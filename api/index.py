import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from pytube import YouTube
import tempfile
import os
import dropbox

app = Flask(__name__)
DOWNLOADS_DIR = tempfile.mkdtemp()  # Create a temporary directory to store downloaded videos
DROPBOX_ACCESS_TOKEN = 'sl.BgfdEz36PiCM5P5Orb-BPmkrgCF7Ita-3YwdDfRf25W8FzrUh7ZmVXAoiH_UwjkjJ3nB_NgD2QSirhyzykkj8Zex4hdh3Ylqqv4wIv_dpLeAe3wMtNAXEEhPbkMT_SOSwP3SeOk'  # Replace with your Dropbox access token

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

        # Upload the file to Dropbox
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

        with open(filepath, 'rb') as file:
            dbx.files_upload(file.read(), f"/{filename}")

        return redirect(url_for('success', filename=filename))
    except Exception as e:
        return render_template('index.html', error=str(e))

@app.route('/success/<filename>')
def success(filename):
    return f"The video '{filename}' has been downloaded and uploaded to Dropbox successfully!"

if __name__ == '__main__':
    app.run()
