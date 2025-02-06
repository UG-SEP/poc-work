# Resume Parser API

## About the Project

This project is a **Resume Parser API** that extracts key information from a resume (PDF file) uploaded by the user. The backend is built using **Django** and **Django Rest Framework (DRF)**, with the ability to process and extract text from resumes using various libraries such as **PyMuPDF**, **pdfplumber**, and **PyPDF2**. The extracted data is then parsed and structured into a JSON response.

## Features

- Extract text from resumes in PDF format.
- Parse the text to extract important details like personal information, skills, education, and work experience.
- Return the extracted data as a structured JSON response.
- pdfplumber and PyPDF2 are used for resume text extraction, while PyMuPDF extracts the links from the pdf files.

## Setup Instructions

Follow the steps below to set up and run the project on your local machine.

### 1. **Create a Virtual Environment**

First, navigate to the project directory and create a Python virtual environment to manage dependencies:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 2. **Install Dependencies**

Install the required dependencies by using the `requirements.txt` file

```bash
# Install dependencies from the requirements file
pip install -r requirements.txt
```
### 3. **Create a .env File**

Create a `.env` file in the root directory of the project to store sensitive environment variables **API_KEY**.
Note: Use `gemini 1.5 flash` API KEY

### 4. **Run Migrations**

Run Django migrations to set up the database:
```bash
# Apply migrations to create the necessary tables in the database
python manage.py migrate
```
### 5. **Run the Development Server**

Start the Django development server
```bash
# Start the development server
python manage.py runserver
```
### 6\. **Testing the API with Postman**

1. Open **Postman** or any API testing tool.
2. Set the request type to `POST`.
3. Enter the URL `http://localhost:8000/` in the request URL.
4. Select the' form-data' option in the **Body** section.
5. Add a field named `resume` with the type `file`.
6. Upload the resume (PDF) file to test the API.
