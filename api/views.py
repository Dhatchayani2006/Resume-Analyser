from django.shortcuts import render
from django.http import JsonResponse
import re
import fitz
import google.generativeai as genai
from .constant import API_KEY

def index(request):
    return render(request, 'index.html')

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        resume_text = "".join(page.get_text() for page in fitz.open(stream=file.read(), filetype="pdf"))
        user_prompt = request.POST.get('user_prompt', '')

        genai.configure(api_key=API_KEY)
        response = genai.GenerativeModel('gemini-pro').generate_content(f"{resume_text}\n{user_prompt}")
        
        parsed_data = parse_resume_text(resume_text)
        name = list(parsed_data.keys())[0] if parsed_data else "N/A"
        experience = parsed_data[name][0] if parsed_data else "N/A"
        education = parsed_data[name][1] if parsed_data else "N/A"
        
        return JsonResponse({
            'generated_text': response.text,
            'name': name,
            'experience': experience,
            'education': education
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

def parse_resume_text(text):
    resumes = {}
    patterns = {
        "name": re.compile(r"Name:\s*(.*)"),
        "experience": re.compile(r"Experience:\s*(.*)", re.IGNORECASE),
        "education": re.compile(r"Education:\s*(.*)", re.IGNORECASE)
    }
    for individual in text.split("\n\n"):
        name = patterns["name"].search(individual)
        if name:
            resumes[name.group(1).strip()] = [
                patterns["experience"].search(individual).group(1).strip() if patterns["experience"].search(individual) else "",
                patterns["education"].search(individual).group(1).strip() if patterns["education"].search(individual) else ""
            ]
    return resumes
