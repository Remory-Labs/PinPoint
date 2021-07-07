from flask import Flask, render_template, Response, request, redirect, url_for
import cv2

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
Camera.WIDTH = 1280
staticF = cv2.imread("static/endOfStream.png")

@app.route('/')
def index():
    global images
    return render_template("index.html", imgs=images)

def getCamFrame(id):
    global staticF
    while 0 < len(cams):
        frame = staticF
        global halt
        global track

        if(not halt):
            if(len(cams) == int(id[1])):
                return

            try:
                if(track == True):
                    p = m.calcPosition(int(id[1]))

                    pos = m.matchIt(p)
                    for cam in p:
                        for detection in range(0, len(cam[1][0])):
                            g = cam[1]
                            center = g[0][detection]
                            height = g[1][detection]
                            #sides = g[2][detection]
                            rec = g[3][detection]
                            #idx = g[4]

                            cv2.rectangle(cam[0], (rec[0], rec[1]), (rec[2], rec[3]), (255, 0, 0), 3)
                            #cv2.circle(cam[0], center, 10, (255, 0, 255), -1)
                            #cv2.putText(cam[0], str(height), (center[0] + 60, center[1]), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 3)

                            frame = cam[0]

                            if(Database.getRecogsNums() == 1):
                                Database.logRecogs()
                            Database.logPos(pos)
                else:
                    frame = cams[int(id[1])].getFrame()

                frame = cv2.imencode('.jpg', frame)[1].tobytes()
            except:
                frame = cv2.imencode('.jpg', staticF)[1].tobytes()
                #Database.logError('Minor')
        else:
             frame = cv2.imencode('.jpg', staticF)[1].tobytes()

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