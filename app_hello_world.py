from datetime import datetime

from flask import Flask, send_file

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/name/<name>")
def name(name):
    return f"Hello, {name}!"


@app.route("/error")
def error():
    return "error is fixed"

@app.route("/time")
def get_current_time():
    return datetime.now().strftime("%A, %d %B %Y %H:%M:%S")


# Flask returns HTML page
@app.route("/html")
def get_html():
    return """
    <html>
    <head>
        <title>My Page</title>
    </head>
    <body>
        <h1>Hello, World!</h1>
        <p>This is a paragraph</p>
        <p>This is another paragraph</p>
    </body>
    </html>
    """


# Flask returns image
@app.route("/image")
def get_image():
    image_path = 'static/img.png'

    # Return download image
    return send_file(image_path, as_attachment=True)


# Flask returns page with javascript
# Current time which increments every second
@app.route("/time_js")
def get_time_js():
    return """
    <html>
    <head>
        <title>Time</title>
        <script>
            function updateTime() {
                const time = new Date();
                document.getElementById("time").innerText = time;
            }
            setInterval(updateTime, 1000);
        </script>
    </head>
    <body>
        <h1>Current Time</h1>
        <p id="time"></p>
    </body>
    </html>
    """


# Flask returns JSON
@app.route("/json")
def get_json():
    return [
        {
            "name": "Alice",
            "age": 25
        },
        {
            "name": "Bob",
            "age": 30
        }
    ]


if __name__ == "__main__":
    app.run(port=5001, debug=True)
