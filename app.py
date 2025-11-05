import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>BedsideBot - Patient Monitoring System</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { max-width: 1200px; margin: 0 auto; text-align: center; }
            .header { margin-bottom: 40px; }
            .title { font-size: 3em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
            .subtitle { font-size: 1.2em; opacity: 0.9; }
            .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 40px 0; }
            .feature { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; backdrop-filter: blur(10px); }
            .feature h3 { color: #ffd700; margin-bottom: 15px; }
            .nav-buttons { margin: 40px 0; }
            .btn { display: inline-block; padding: 15px 30px; margin: 10px; background: rgba(255,255,255,0.2); color: white; text-decoration: none; border-radius: 25px; transition: all 0.3s; }
            .btn:hover { background: rgba(255,255,255,0.3); transform: translateY(-2px); }
            .status { background: rgba(0,255,0,0.2); padding: 15px; border-radius: 10px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 class="title">🏥 BedsideBot</h1>
                <p class="subtitle">Advanced Patient Monitoring & Communication System</p>
                <div class="status">✅ System Online - Ready for Multi-Device Access</div>
            </div>
            
            <div class="features">
                <div class="feature">
                    <h3>🏥 Hospital Management</h3>
                    <p>Complete hospital registration and management system for healthcare facilities.</p>
                </div>
                <div class="feature">
                    <h3>👤 Patient Portal</h3>
                    <p>Patient registration, monitoring, and communication interface.</p>
                </div>
                <div class="feature">
                    <h3>👨‍⚕️ Staff Dashboard</h3>
                    <p>Healthcare staff management and real-time patient monitoring.</p>
                </div>
                <div class="feature">
                    <h3>📊 ICU Monitoring</h3>
                    <p>Real-time intensive care unit dashboard with patient status tracking.</p>
                </div>
            </div>
            
            <div class="nav-buttons">
                <a href="/hospital" class="btn">🏥 Hospital Registration</a>
                <a href="/patient" class="btn">👤 Patient Portal</a>
                <a href="/staff" class="btn">👨‍⚕️ Staff Dashboard</a>
                <a href="/icu" class="btn">📊 ICU Monitoring</a>
            </div>
            
            <div class="feature">
                <h3>🌐 Multi-Device Access</h3>
                <p><strong>Share this URL with your team:</strong></p>
                <p style="background: rgba(0,0,0,0.3); padding: 10px; border-radius: 5px; word-break: break-all;">
                    <script>document.write(window.location.href);</script>
                </p>
                <p>✅ Works on computers, tablets, and mobile devices<br>
                ✅ Multiple users can access simultaneously<br>
                ✅ No installation required - just open in browser</p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/hospital')
def hospital():
    return '<h1>🏥 Hospital Registration</h1><p>Hospital management system</p><a href="/">← Back to Home</a>'

@app.route('/patient')
def patient():
    return '<h1>👤 Patient Portal</h1><p>Patient monitoring and communication</p><a href="/">← Back to Home</a>'

@app.route('/staff')
def staff():
    return '<h1>👨‍⚕️ Staff Dashboard</h1><p>Healthcare staff management</p><a href="/">← Back to Home</a>'

@app.route('/icu')
def icu():
    return '<h1>📊 ICU Monitoring</h1><p>Real-time patient monitoring dashboard</p><a href="/">← Back to Home</a>'

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)