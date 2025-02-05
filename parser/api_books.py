import google.generativeai as genai
import os
import json
import logging

logger = logging.getLogger(__name__)

def extract_info_from_resume(text_content):
    genai.configure(api_key=os.getenv('API_KEY'))

    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = """
    You are a Resume Parsing AI. Please extract the following details from the resume text and return them in a structured JSON format as shown below. Ensure that sections like Education, Experience, and Skills are correctly captured. If any section is missing or not available, return null or an empty array. Please do not include any additional information or explanations, just return the JSON object as shown below.

    {
        "personal_information": {
            "name": "<string: full name of the candidate>",
            "email": "<string: email>",
            "mobile": "<string: mobile number>",
            "city": "<string: city of the candidate>",
            "country": "<string: country of the candidate>",
            "linkedin": "<string: linkedin URL or null>",
            "github": "<string: github URL or null>"
        },
        "skills": {
            "languages": ["<string: language 1>", "<string: language 2>", ...],
            "frameworks": ["<string: framework 1>", "<string: framework 2>", ...],
            "technologies": ["<string: technology 1>", "<string: technology 2>", ...]
        },
        "education": [
            {
                "degree_name": "<string: degree name>",
                "institution_name": "<string: institution name>",
                "city": "<string: city>",
                "country": "<string: country>",
                "year_of_start": <int: start year>,
                "year_of_graduation": <int: graduation year>
            }
        ],
        "experience": [
            {
                "company_name": "<string: company name>",
                "position": "<string: position>",
                "duration": "<string: duration (e.g. 2019-2022)>",
                "responsibilities": "<string: job responsibilities>"
            }
        ],
        "projects": [
            {
                "project_name": "<string: project name>",
                "project_description": "<string: description>"
            }
        ],
        "achievements_awards": [
            "<string: achievement/award>"
        ],
    }

    """
    response = model.generate_content(prompt+ "\n\n" + text_content)
    try:
        
        response_content = response.text.strip()
        
        if response_content.startswith("```json"):
            response_content = response_content[7:].strip()  

        if response_content.endswith("```"):
            response_content = response_content[:-3].strip() 

        response_content = response_content.replace('null', '""')

        return json.loads(response_content)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
        return None