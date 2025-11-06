from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>BedsideBot Healthcare System</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .header { text-align: center; margin-bottom: 30px; }
            .logo { font-size: 2.5em; color: #2c3e50; margin-bottom: 10px; }
            .subtitle { color: #7f8c8d; font-size: 1.2em; }
            .nav-buttons { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 30px; }
            .nav-btn { padding: 15px 20px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; text-align: center; transition: background 0.3s; }
            .nav-btn:hover { background: #2980b9; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">BedsideBot Healthcare System</div>
                <div class="subtitle">Advanced Patient Monitoring Platform</div>
            </div>
            <div class="nav-buttons">
                <a href="/hospital" class="nav-btn">Register Hospital</a>
                <a href="/staff" class="nav-btn">Register Staff</a>
                <a href="/patient" class="nav-btn">Register Patient</a>
                <a href="/icu_dashboard" class="nav-btn">ICU Dashboard</a>
                <a href="/interface" class="nav-btn">Patient Interface</a>
                <a href="/demo" class="nav-btn">Demo Mode</a>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)