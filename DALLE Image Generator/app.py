from flask import Flask, render_template, request, jsonify
from tryme import generate_images   # ✅ use your helper

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    try:
        prompt = request.form["prompt"]
        size = request.form.get("size", "512x512")
        n = int(request.form.get("n", 1))

        # Generate & save images locally
        urls = generate_images(prompt, size=size, n=n)

        return jsonify({"urls": urls})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
