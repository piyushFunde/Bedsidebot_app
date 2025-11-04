import cv2
from flask import Flask, Response

app = Flask(__name__)

def generate_frames():
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (640, 480))
            cv2.putText(frame, 'Camera Working!', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html>
<head><title>Simple Camera Test</title></head>
<body style="text-align: center; padding: 50px;">
    <h1>Camera Test</h1>
    <img src="/video_feed" style="border: 2px solid #333; width: 640px; height: 480px;">
    <p>You should see yourself above!</p>
</body>
</html>'''

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("Simple camera test running at http://localhost:5001")
    app.run(debug=True, port=5001)