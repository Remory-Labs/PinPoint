from flask import Flask, render_template, Response, request, redirect, url_for
import cv2

from camera import Camera
from cameraMatcher import Matcher

app = Flask(__name__)
app.secret_key = b"@meki?'4y>RBm#r"

cams = []
images = []

@app.route('/')
def index():
    global images
    return render_template("index.html", images=images)

def getCamFrame(id):
    while 0 < len(cams):
        if(len(cams) == int(id[1])):
            return

        frame = None

        #m = Matcher(190, cams)
        #h = m.calcPosition()

        #frame, recs = h[0]

        #(center, personHeight, personPosBox) = recs
        #if(len(personPosBox) != 0):
        #    (x1, y1, x2, y2) = personPosBox
        #    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0))

        try:
            frame = cams[int(id[1])].getFrame(1280)

            frame = cv2.imencode('.jpg', cv2.resize(frame, (0, 0), fx=0.5, fy=0.5))[1].tobytes()
        except:
            frame = cv2.imencode('.jpg', cv2.imread("static/endOfStream.png"))[1].tobytes()

        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            

@app.route("/feeds<id>")
def feeds(id):
    return Response(getCamFrame(id), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route('/new_cam', methods=["POST", "GET"])
def addcam():
    side = request.form["cSide"]
    ctype = request.form["cType"]
    method = request.form["detectMethod"]
    path = request.form["arguments"]

    global cams
    global images

    if(len(images) == 4):
        return redirect(url_for("index"))

    c = Camera(ctype, side, method, path)
    cams.append(c)
    images.append("/feeds<{0}>".format(len(cams) - 1))

    return redirect(url_for("index"))

@app.route('/delete_cam', methods=["POST", "GET"])
def delcam():
    global cams
    global images

    for idx in request.form.keys():
        del images[int(idx)]
        del cams[int(idx)]

    tmpImage = []
    for idx in range(len(cams)):
        tmpImage.append("/feeds<{0}>".format(idx))

    images = tmpImage
           
    return redirect(url_for("index"))

def tryParse(string):
    try:
        return int(string), True
    except:
        return string, False

@app.route('/purge', methods=["POST", "GET"])
def purge():
    global cams
    global images

    cams.clear()
    images.clear()

    print("All cameras got deleted.")

    return redirect(url_for("index"))

@app.route('/replay', methods=["POST", "GET"])
def replay():
    global cams
    global images

    for cam in cams:
        cam.replay()

    print("Reseted cameras.")

    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True, host="localhost")