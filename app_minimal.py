from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>BedsideBot - Patient Monitoring System</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f0f8ff; }
            .container { max-width: 800px; margin: 0 auto; }
            .success { color: #28a745; font-size: 28px; margin: 20px 0; }
            .feature { background: white; padding: 20px; margin: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            .btn { display: inline-block; padding: 15px 30px; margin: 10px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
            .btn:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="success">🏥 BedsideBot Deployed Successfully!</h1>
            <p style="font-size: 18px; color: #666;">Your patient monitoring system is now live and accessible from anywhere!</p>
            
            <div class="feature">
                <h3>🎉 Deployment Complete</h3>
                <p>Your BedsideBot application is running on Railway cloud platform</p>
                <p><strong>Status:</strong> <span style="color: green;">✅ Online</span></p>
            </div>
            
            <div class="feature">
                <h3>🌐 Multi-Device Access</h3>
                <p>Access this system from:</p>
                <ul style="text-align: left; display: inline-block;">
                    <li>Multiple computers simultaneously</li>
                    <li>Tablets and mobile devices</li>
                    <li>Any web browser with internet</li>
                </ul>
            </div>
            
            <div class="feature">
                <h3>🔧 System Features</h3>
                <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
                    <a href="/hospital" class="btn">Hospital Registration</a>
                    <a href="/patient" class="btn">Patient Management</a>
                    <a href="/staff" class="btn">Staff Portal</a>
                    <a href="/dashboard" class="btn">ICU Dashboard</a>
                </div>
            </div>
            
            <div class="feature">
                <h3>📱 Share This URL</h3>
                <p>Share this link with your team to access BedsideBot:</p>
                <code style="background: #f8f9fa; padding: 10px; border-radius: 5px; display: block; margin: 10px 0;">
                    <script>document.write(window.location.href);</script>
                </code>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return jsonify({"status": "ok", "message": "BedsideBot is healthy"})

@app.route('/hospital')
def hospital():
    return '<h1>🏥 Hospital Registration</h1><p>Hospital registration system coming soon!</p><a href="/">← Back to Home</a>'

@app.route('/patient')
def patient():
    return '<h1>👤 Patient Management</h1><p>Patient management system coming soon!</p><a href="/">← Back to Home</a>'

@app.route('/staff')
def staff():
    return '<h1>👨‍⚕️ Staff Portal</h1><p>Staff management system coming soon!</p><a href="/">← Back to Home</a>'

@app.route('/dashboard')
def dashboard():
    return '<h1>📊 ICU Dashboard</h1><p>Real-time monitoring dashboard coming soon!</p><a href="/">← Back to Home</a>'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)