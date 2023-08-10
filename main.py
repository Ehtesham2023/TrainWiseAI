from flask import Flask, render_template ,Response
from camera2 import VideoCamera
from camera import VideoCamera
from camera3 import VideoCamera

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashbord.html")
def dashbord():
    return render_template("dashbord.html")

@app.route("/exercise_select.html")
def exercise_select():
    return render_template("exercise_select.html")

@app.route("/planworkout.html")
def planworkout():
    return render_template("planworkout.html")


@app.route('/shoulder.html' )
def sample():
    return render_template('/shoulder.html')
def gen(camera2):
    while True:
        frame = camera2.get_frame()
        yield(b'--frame\r\n' 
              b'Content-Type : image/jpeg\r\n\r\n'+ frame + b'\r\n\r\n')
@app.route('/video_feed1')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/biceps.html' )
def biceps():
    return render_template('/biceps.html')
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n' 
              b'Content-Type : image/jpeg\r\n\r\n'+ frame + b'\r\n\r\n')
@app.route('/video_feed2')
def video_feed2():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')





@app.route('/legs.html' )
def legs():
    return render_template('/legs.html')
def gen(camera3):
    while True:
        frame = camera3.get_frame()
        yield(b'--frame\r\n' 
              b'Content-Type : image/jpeg\r\n\r\n'+ frame + b'\r\n\r\n')
@app.route('/video_feed3')
def video_feed3():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



app.run(debug=True)