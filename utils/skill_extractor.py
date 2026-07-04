import os
import re
import pandas as pd

# Project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to jobs.csv
JOBS_PATH = os.path.join(BASE_DIR, "jobs.csv")


def recommend_jobs(resume_skills):

    # Read jobs dataset
    jobs = pd.read_csv(JOBS_PATH)

    # Remove extra spaces from column names
    jobs.columns = jobs.columns.str.strip()

    # Convert resume skills to lowercase and remove duplicates
    resume_skill_set = {str(skill).strip().lower() for skill in resume_skills}

    recommendations = []

    # Loop through every job
    for _, row in jobs.iterrows():

        # Safely read columns
        required = str(row.get("Required Skills", ""))
        languages = str(row.get("Programming Languages Required", ""))

        # Combine skills
        all_skills = required + "," + languages

        # Split by comma or slash
        required_skills = []

        for item in re.split(r"[,/]", all_skills):
            item = item.strip().lower()

            if item:
                required_skills.append(item)

        # Remove duplicate required skills
        required_skills = list(set(required_skills))

        # Find matched skills
        matched = []

        for skill in required_skills:
            if skill in resume_skill_set:
                matched.append(skill)

        # Calculate score
        if required_skills:
            score = round(
                (len(matched) / len(required_skills)) * 100,
                2
            )
        else:
            score = 0

        recommendations.append({
            "Job Title": row.get("Job Title", "Unknown"),
            "Match Score": score,
            "Matched Skills": ", ".join(sorted(matched)),
            "Required Skills": ", ".join(sorted(required_skills))
        })

    # Convert to DataFrame
    result = pd.DataFrame(recommendations)

    # Sort by match score
    result = result.sort_values(
        by="Match Score",
        ascending=False
    )

    # Remove duplicate job titles
    result = result.drop_duplicates(
        subset=["Job Title"]
    )

    # Return top 10 recommendations
    return result.head(10)