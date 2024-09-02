import ast
import logging
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import Http404, HttpResponse, JsonResponse
import fitz
from django.http import HttpResponse
import os

from home.prompts import *
from home.utilities import ResumePDF, create_resume, formatedResponse, get_response, get_sample_data, save_resume
from home.constants import pdf_path
from home.models import Submit
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request,'index.html')

def submit(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('pwd')
        sub=Submit(email=email,password=password)
        sub.save()
        messages.success(request,"Data updated successfully")

    return HttpResponse(Submit.objects.all())

class Home(APIView):
    def post(self, request):
        try:
            jobRole = request.data.get('jobRole')
            fields = {
            "name": "John Doe",
            "contact information": "Email: john.doe@example.com | Phone: 555-555-5555 | LinkedIn: linkedin.com/in/johndoe",
            "sections": {
                "Summary": [
                    "Motivated software engineer with 5+ years of experience in developing scalable applications."
                ],
                "Experience": [
                    "Led Implementation of Anaplan TPM solution for Pepsi Bottling Ventures. Managed project lifecycle from requirements gathering to post-deployment optimization. Streamlined Funding, Claims (Payment), and Accruals processes, improving operational efficiency and reducing processing time by 63%",
                    "Pioneered an innovative GPT-based AI solution for revenue growth management, integrating labeled RGM data to deliver actionable insights through charts and queries",
                    "Supported Functional Testing, UAT and Hypercare of Salesforce TPM solution implementation for Duracell Co.",
                    "Developed comprehensive Anaplan TPM product for PwC, featuring modules for Annual Operating Plans, Promotion Management, Fund Management, Payments, Accruals, and Reporting",
                    "Implemented SAP BTP iFlow for Anaplan-SAP S/4HANA integration. Achieved 98% data transfer accuracy and 75% reduction in manual entry",
                    "Supported data-driven market scan for AT&T Inc., analyzed customer data & competitor offerings to identify market opportunities & enhance competitive benchmarking. Provided analysis of results through reports, narratives, and presentations",
                    "Supported financial planning and analysis for Google LLC, aiding in budget management and financial forecasting to optimize operational efficiency",
                    "Developed and implemented Microsoft Power Platform solution of dynamic resource management, enhancing efficiency, visibility, and data-driven decision-making for Customer Transformation Team leadership"
                ],
                "Education": [
                    "B.S. in Computer Science, XYZ University, 2017"
                ],
                "Skills": [
                    "Python, Java, C++",
                    "Django, Flask, Spring Boot",
                    "SQL, MongoDB",
                    "Version Control: Git"
                ],
                "Projects": [
                    "Project hashedIn: Developed a web application for ABC Corp, which improved their internal processes by 20%."
                ],
                "Certifications": [
                    "Certified Kubernetes Administrator (CKA)",
                    "AWS Certified Solutions Architect"
                ]
            }
        }
            experience_prompt=pre_experience.format(experience=fields["sections"]["Experience"],job_role=jobRole)
            et=get_response(user_prompt=experience_prompt)
            f = ast.literal_eval(et)
            fields["sections"]["Experience"]=f
            document=create_resume(fields)
            save_resume(document)
            return HttpResponse("success")
        
        except Exception as err:
            logging.error(f"Exception occurred ->{err}")
            return HttpResponse(f"Error -> {err}", status=500)
        
class Resume2(APIView):
    def post(self, request):
        try:
            jobRole = request.data.get('jobRole')
            personal_details, academic_details, chapters, professional_summary, skills, positions_of_responsibility, projects, research_papers = get_sample_data()
            print(research_papers)
            # Chapter Prompt Changes
            chapter_prompt=resumePrompt.format(preData='chapters',data=chapters[0].body,job_role=jobRole)
            response=formatedResponse(chapter_prompt)
            chapters[0].body=response

            # Professional Summary Prompt Changes
            Prompt=resumePrompt.format(preData='professionalSummary',data=professional_summary,job_role=jobRole)
            summary_response=formatedResponse(Prompt)
            professional_summary=summary_response

            for i in range(len(projects)):
                prompt=resumePrompt.format(preData='project description',data=projects[i].description,job_role=jobRole)
                project_response=formatedResponse(prompt)
                projects[i].description=project_response

            # Generate PDF
            pdf = ResumePDF(personal_details, chapters, academic_details, professional_summary, skills, positions_of_responsibility, projects, research_papers)
            pdf.add_page()

            # Add light grey background for the entire page
            pdf.set_fill_color(250, 250, 250)  # Even lighter grey background
            pdf.rect(0, 48, 210, 297-40, 'F')  # 297 is A4 height, 40 is header height

            pdf.add_professional_summary()
            for chapter in chapters:
                pdf.add_chapter(chapter)
            pdf.add_academic_details()
            pdf.add_skills()
            pdf.add_position_of_responsibility()
            pdf.add_projects()
            pdf.add_research_papers()

            output_dir = r"C:/Users/rahulsingh594/Documents/Rahul"
            os.makedirs(output_dir, exist_ok=True)
            pdf.output(os.path.join(output_dir, 'resume14.pdf'))
            return HttpResponse("success")
        
        except Exception as err:
            logging.error(f"Exception occurred ->{err}")
            return HttpResponse(f"Error -> {err}", status=500)
        