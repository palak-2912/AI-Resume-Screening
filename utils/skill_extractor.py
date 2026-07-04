import os
import re
import pandas as pd

# Project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to skill.csv
SKILL_PATH = os.path.join(BASE_DIR, "skill.csv")


def extract_skills(text):

    df = pd.read_csv(SKILL_PATH)
    df.columns = df.columns.str.strip()

    skills = df["skill"].dropna().tolist()

    text = text.lower()

    detected = []

    for skill in skills:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            detected.append(skill)

    return sorted(list(set(detected)))