from flask import Flask, request, render_template, send_file, jsonify
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

progress_data = {"status": "idle", "progress": 0}

def progress_hook(d):
    if d['status'] == 'downloading':
        progress_data['status'] = 'downloading'
        progress_data['progress'] = d.get('_percent_str', '0%').strip()

    elif d['status'] == 'finished':
        progress_data['status'] = 'completed'
        progress_data['progress'] = "100%"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        link = request.form.get("link")
        if not link:
            return render_template("index.html", error="Please enter a valid YouTube link.")

        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
                'progress_hooks': [progress_hook]
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=True)
                filename = ydl.prepare_filename(info)

            return send_file(filename, as_attachment=True)

        except Exception as e:
            return render_template("index.html", error=f"Error: {str(e)}")

    return render_template("index.html", error=None)

@app.route("/progress")
def progress():
    return jsonify(progress_data)

if __name__ == "__main__":
    app.run(debug=True)
