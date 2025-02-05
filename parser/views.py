from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .controllers import ResumeProcessor

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def extract_resume(request):
    if 'resume' not in request.FILES:
        return Response({"error": "No resume file provided"}, status=400)

    resume_file = request.FILES['resume']

    extracted_data = ResumeProcessor.process_resume(resume_file)

    return Response(extracted_data, status=200)
