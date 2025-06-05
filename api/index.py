from flask import Flask
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def home():
    return 'Hellooe, World!'

@app.route('/about')
def about():
    return 'About'

@app.get("/api/health")
async def health_check():
    print("Uploading PDF...")

    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == '__main__':
    app.run(debug=True)