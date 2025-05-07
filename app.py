from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    try:
        return render_template('home.html')
    except Exception as e:
        # This will help with debugging
        return jsonify({"error": str(e)}), 500

# For local development
if __name__ == '__main__':
    app.run(debug=True)

# This is needed for Vercel
app.debug = False
