from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None

    if request.method == 'POST':
        product_name = request.form['product_name']
        features = request.form['features']
        tone = request.form['tone']

        prompt = f"""
You are an expert e-commerce copywriter.

Write a {tone} product description.

Product Name: {product_name}
Features: {features}

Rules:
- Start with strong introduction
- No random words or broken sentences
- 100–150 words
- Make it engaging and persuasive
"""

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:5000",
                "X-Title": "AI Product Generator"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )

        data = response.json()

        if "choices" in data:
            result = data["choices"][0]["message"]["content"]
        else:
            result = data.get("error", {}).get("message", "API Error")

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)