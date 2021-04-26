from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
import numpy as np

from camera import Camera
from cameraMatcher import Matcher
from handleDatabase import Database

app = Flask(__name__)
app.secret_key = b"@meki?'4y>RBm#r"

cams = []
images = []
height = 180
halt = False
track = False
m = None
blanks = np.zeros((300, 300), np.uint8)
staticF = cv2.imread("static/endOfStream.png")

@app.route('/')
def index():
    global images
    a = images.copy()
    #a.append('/blank')
    print(a)
    return render_template("index.html", images=a)

def getCamFrame(id):
    global staticF
    while 0 < len(cams):
        frame = staticF
        global halt
        global track
        global blanks

        if(not halt):
            blanks = np.zeros((300, 300), np.uint8)
            if(len(cams) == int(id[1])):
                return

            try:
                if(track == True):
                    h = m.calcPosition()
                    p = m.matchPositions()

                    frame, recs = h[0]

                    (center, personHeight, personPosBox) = recs
                    (x1, y1, x2, y2) = personPosBox
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0))

                    cv2.circle(blanks, (p[0], p[1]), 5, (255, 255, 255), cv2.FILLED)
                    
                    if(Database.getRecogsNums() == 1):
                        Database.logRecogs()
                    Database.logPos(p)
                else:
                    frame = cams[int(id[1])].getFrame(1280)

                frame = cv2.imencode('.jpg', frame)[1].tobytes()
            except:
                frame = cv2.imencode('.jpg', staticF)[1].tobytes()
                Database.logError('Minor')
        else:
             frame = cv2.imencode('.jpg', staticF)[1].tobytes()

        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            

@app.route("/feeds<id>")
def feeds(id):
    return Response(getCamFrame(id), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/blank")
def blank():
    return Response(getBlank(), mimetype="multipart/x-mixed-replace; boundary=frame")

def getBlank():
    global blanks
    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', blanks)[1].tobytes() + b'\r\n')

@app.route('/new_cam', methods=["POST", "GET"])
def addcam():
    side = request.form["cSide"]
    ctype = request.form["cType"]
    method = request.form["detectMethod"]
    path = request.form["arguments"]

    global cams
    global images
    global height
    global m

    if(len(images) == 4):
        return redirect(url_for("index"))

    c = Camera(ctype, side, method, path)
    cams.append(c)
    images.append("/feeds<{0}>".format(len(cams) - 1))

    m = Matcher(height, cams)

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

@app.route('/replay', methods=["POST", "GET"])
def replay():
    global cams
    global images
    global halt
    
    halt = True

    for cam in cams:
        cam.replay()

    halt = False
       
    print("Reseted cameras.")

    return redirect(url_for("index"))

@app.route('/calibrate', methods=["POST", "GET"])
def calibrate():
    global height

    height = int(request.form["height"])

    print("New height is set to: " + str(height))

    return redirect(url_for("index"))

@app.route('/track', methods=["POST", "GET"])
def track():
    global track
    
    track = not track

    print("Tracking switched.")

    return redirect(url_for("index"))

@app.route('/purge', methods=["POST", "GET"])
def purge():
    global cams
    global images

    cams.clear()
    images.clear()

    print("All cameras got deleted.")

    return redirect(url_for("index"))

if __name__ == '__main__':
    print(Database.connect())
    app.run(debug=True, host="localhost")