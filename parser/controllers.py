import pdfplumber
import PyPDF2
import re
import logging
from .api_books import extract_info_from_resume
import fitz


logger = logging.getLogger(__name__)

class ResumeProcessor:

    @staticmethod
    def extract_text_from_pdf(pdf_file):
        try:

            text = ResumeProcessor.extract_text_with_pdfplumber(pdf_file)
            text=""
            if not text.strip():
                
                logger.warning("No text extracted with pdfplumber, attempting PyPDF2.")
                text = ResumeProcessor.extract_text_with_pypdf2(pdf_file)

            return text.strip()

        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}", exc_info=True)
            raise Exception(f"Failed to extract text from the resume: {e}")

    @staticmethod
    def extract_text_with_pdfplumber(pdf_file):
        text = ""
        try:
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            return text
        except Exception as e:
            logger.error(f"pdfplumber extraction failed: {e}", exc_info=True)
            return ""

    @staticmethod
    def extract_text_with_pypdf2(pdf_file):
        text = ""
        try:

            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() or ""
            
            return text
        except Exception as e:
            logger.error(f"PyPDF2 extraction failed: {e}", exc_info=True)
            return ""

    @staticmethod
    def extract_email(resume_text):
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        email_match = re.findall(email_pattern, resume_text)
        return email_match[0] if email_match else None

    @staticmethod
    def extract_mobile(resume_text):
        mobile_pattern = r'(\+91[-.\s]?)?([6-9]\d{4}[\s]?\d{5})\b'
        mobile_match = re.search(mobile_pattern, resume_text)
        return mobile_match.group(2) if mobile_match else None


    @staticmethod
    def extract_urls_from_pdf(pdf_file):
        try:
            doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            urls = []
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                links = page.get_links()
                
                for link in links:
                    uri = link.get('uri')
                    if uri:
                        urls.append(uri)
            return urls
        except Exception as e:
            logger.error(f"An error occurred while extracting URLs from the PDF: {e}")
            raise Exception(f"Failed to extract URLs from the PDF: {e}")


    @staticmethod
    def extract_linkedin_and_github(urls):
        linkedin_url = None
        github_url = None
        mailto_url = None

        linkedin_pattern = r"(https?:\/\/)?(www\.)?linkedin\.com\/in\/[a-zA-Z0-9\-]+\/?"
        github_pattern = r"(https?:\/\/)?(www\.)?github\.com\/[a-zA-Z0-9\-]+\/?$"
        mailto_pattern = r"mailto:([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"

        for url in urls:
            if re.search(linkedin_pattern, url):
                linkedin_url = url
            if re.search(github_pattern, url):
                github_url = url
            mailto_match = re.search(mailto_pattern, url)
            if mailto_match:
                mailto_url = mailto_match.group(1)

        return linkedin_url, github_url, mailto_url

    @staticmethod
    def fix_mobile_number(mobile):
        correct_mobile_no = ""
        
        if "+91" in mobile:
            correct_mobile_no += "+91 "
            mobile = mobile.replace("+91", "")

        digits = re.findall(r'\d', mobile)  

        if len(digits) < 10:
            return None 

        if digits[0] not in ['6', '7', '8', '9']:
            return None 
        
        correct_mobile_no += ''.join(digits[:10]) 
        
        return correct_mobile_no

    @staticmethod
    def process_resume(pdf_file):
        try:
            resume_text = ResumeProcessor.extract_text_from_pdf(pdf_file)
            if not resume_text:
                raise Exception("Failed to extract text from resume.")
            resume_text = resume_text.lower()

            parsed_data = extract_info_from_resume(resume_text)

            if not parsed_data:
                raise Exception("Failed to parse resume.")

            email = ResumeProcessor.extract_email(resume_text)
            mobile = ResumeProcessor.extract_mobile(resume_text)
            pdf_file.seek(0)
            urls = ResumeProcessor.extract_urls_from_pdf(pdf_file)

            linkedin_url, github_url, mailto_url = ResumeProcessor.extract_linkedin_and_github(urls)

            if linkedin_url is not None:
                parsed_data['personal_information']['linkedin'] = linkedin_url

            if github_url is not None:
                parsed_data['personal_information']['github'] = github_url

            if email is not None:
                parsed_data['personal_information']['email'] = email

            if mobile is not None:
                parsed_data['personal_information']['mobile'] = mobile
            else:
                parsed_data['personal_information']['mobile'] = ResumeProcessor.fix_mobile_number(parsed_data['personal_information']['mobile'])
            
            if mailto_url is not None:
                parsed_data['personal_information']['email'] = mailto_url

            return {
                "message": "Success",
                "data": parsed_data
            }

        except Exception as e:
            logger.error(f"Error processing resume: {e}", exc_info=True)
            return {
                "message": "Error",
                "error": str(e)
            }