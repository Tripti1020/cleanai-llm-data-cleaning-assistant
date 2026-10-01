import json
import os
import re
import time

from dotenv import load_dotenv
from google import genai

# --------------------------------------------------
# Environment
# --------------------------------------------------

load_dotenv()

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
FALLBACK_MODEL = os.getenv(
    "GEMINI_FALLBACK_MODEL",
    "gemini-2.5-flash-lite"
)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# --------------------------------------------------
# Prompt Loader
# --------------------------------------------------

def load_prompt():

    with open(
        "prompts/cleaning_prompt.txt",
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()

# --------------------------------------------------
# JSON Extractor
# --------------------------------------------------

def extract_json(text):
    """
    Extract JSON even if Gemini wraps it
    in markdown.
    """

    text = text.strip()

    text = re.sub(
        r"^```json|^```|```$",
        "",
        text,
        flags=re.MULTILINE
    ).strip()

    return json.loads(text)

# --------------------------------------------------
# Gemini Request
# --------------------------------------------------

def ask_model(model_name, prompt):

    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )

    return extract_json(response.text)

# --------------------------------------------------
# Main Function
# --------------------------------------------------

def generate_cleaning_plan(profile, issues_df):

    prompt = load_prompt()

    dataset_summary = {
        "rows": profile["rows"],
        "columns": profile["columns"],
        "missing_cells": profile["missing_cells"],
        "duplicate_rows": profile["duplicate_rows"],
        "issues": issues_df.to_dict(orient="records")
    }

    final_prompt = f"""
{prompt}

Dataset Metadata:

{json.dumps(dataset_summary, indent=2)}
"""

    retries = 3

    for attempt in range(retries):

        try:

            result = ask_model(
                MODEL_NAME,
                final_prompt
            )

            return result, None

        except Exception as e:

            message = str(e)

            if "503" in message or "UNAVAILABLE" in message:

                wait = 2 ** attempt

                time.sleep(wait)

                continue

            if "404" in message:

                break

            last_error = message

    try:

        result = ask_model(
            FALLBACK_MODEL,
            final_prompt
        )

        return result, None

    except Exception as e:

        return None, (
            "Gemini is temporarily busy. "
            "Please try again in a minute.\n\n"
            f"Technical details: {str(e)}"
        )