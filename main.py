import os
import random
from PIL import Image
from gradio_client import Client
from moviepy.editor import VideoFileClip
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

TEMP_VIDEO_FOLDER = 'temp_videos/'

if not os.path.exists(TEMP_VIDEO_FOLDER):
    os.makedirs(TEMP_VIDEO_FOLDER)


def get_random_frame(video_path):
    video = VideoFileClip(video_path)
    random_time = random.uniform(0, video.duration)
    frame = video.get_frame(random_time)
    video.close()

    image = Image.fromarray(frame)
    image.save("random_frame.jpg")


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/get_video_description', methods=['POST'])
def get_video_description_gradio():
    video_file = request.files['video']

    video_path = os.path.join(TEMP_VIDEO_FOLDER, video_file.filename)
    video_file.save(video_path)

    get_random_frame(video_path)

    client = Client("https://tonyassi-image-story-teller.hf.space/--replicas/m3hm6/")
    result = client.predict(
        "random_frame.jpg",
        api_name="/predict"
    )
    return jsonify({'data': result})


if __name__ == '__main__':
    app.run(debug=True)
