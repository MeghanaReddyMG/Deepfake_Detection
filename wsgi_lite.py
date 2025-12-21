from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>FalsifyX</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #f0f0f0; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; }
            h1 { color: #333; text-align: center; }
            .status { background: #4CAF50; color: white; padding: 15px; border-radius: 5px; text-align: center; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 FalsifyX</h1>
            <div class="status">✅ System Online</div>
            <p>AI-Powered Deepfake Detection System</p>
            <p>This is a serverless deployment running on Vercel.</p>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return {'status': 'ok', 'service': 'falsifyx'}

# This is required for Vercel
application = app