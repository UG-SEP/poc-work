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

### 1. **Install Docker**

Ensure Docker is installed and running on your system. You can follow the [official Docker installation guide](https://docs.docker.com/get-docker/) for your platform.

### 2. **Clone the Repository**

Clone the repository to your local machine:

```bash
git clone <repository-url>
cd <repository-directory>
```

### 3. **Create a .env File**

Create a `.env` file in the root directory of the project to store sensitive environment variables **API_KEY**.
Note: Use `gemini 1.5 flash` API KEY

### 4. **Build and Run the Docker Container**

Build and run the Docker container by executing the following commands:

```bash
# Build the Docker image
docker build -t resume-parse-api .

# Run the Docker container
docker run -d -p 8000:8000 --env-file .env resume-parse-api
```

### 5. **Testing the API with Postman**

1. Open **Postman** or any API testing tool.
2. Set the request type to `POST`.
3. Enter the URL `http://localhost:8000/` in the request URL.
4. Select the' form-data' option in the **Body** section.
5. Add a field named `resume` with the type `file`.
6. Upload the resume (PDF) file to test the API.
