from flask import Flask, Response, render_template
import random
import time
import json
import os

app = Flask(__name__)

image_folder = "static/images"
image_urls = [
    f"/static/images/{img}"
    for img in os.listdir(image_folder)
    if img.endswith((".webp", ".png", ".jpg", ".jpeg"))
]


historical_data = []


@app.route("/stream")
def stream():
    def event_stream():
        while True:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            image_url = random.choice(image_urls)
            name = os.path.splitext(os.path.basename(image_url))[0]

            data = {"name": name, "timestamp": timestamp, "image": image_url}

            historical_data.append(data)

            if len(historical_data) > 100:  # Keep only the latest 100 events
                historical_data.pop(0)

            data_json = json.dumps(data)
            yield f"data: {data_json}\n\n"

            time.sleep(random.uniform(1, 3))

    return Response(event_stream(), mimetype="text/event-stream")


@app.route("/")
def index():
    return render_template("index.html")
    # return app.send_static_file("index.html")


@app.route("/history")
def history():
    return render_template("history.html", historical_data=reversed(historical_data))


if __name__ == "__main__":
    app.run(debug=True)
