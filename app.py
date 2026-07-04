from flask import Flask, render_template, request
import os
import tempfile

from utils.parser import extract_text
from utils.preprocess import clean_text
from utils.skill_extractor import extract_skills
from utils.recommender import recommend_jobs

# Create Flask app
app = Flask(__name__)

# Use temporary directory for uploads (Vercel compatible)
UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    # Check if file exists
    if "resume" not in request.files:
        return "No file uploaded."

    file = request.files["resume"]

    if file.filename == "":
        return "Please select a resume."

    # Save uploaded file
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    try:
        # Extract resume text
        resume_text = extract_text(filepath)

        # Clean text
        clean_resume = clean_text(resume_text)

        # Extract skills
        skills = extract_skills(clean_resume)

        # Recommend jobs
        jobs = recommend_jobs(skills)

        return render_template(
            "result.html",
            skills=skills,
            jobs=jobs.to_dict(orient="records")
        )

    except Exception as e:
        return f"Error: {str(e)}"

    finally:
        # Delete uploaded file after processing
        if os.path.exists(filepath):
            os.remove(filepath)


# This is only used when running locally
if __name__ == "__main__":
    app.run(debug=True)