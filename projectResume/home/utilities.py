import tempfile
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import openai
import ast
from home.constants import pdf_path
import os
from home.prompts import sy

def get_response(user_prompt,system_prompt=sy):
    response = openai.chat.completions.create(
    # model="gpt-4", 
    model="gpt-4o",                    
    messages=[{"role": "system", "content": system_prompt,},
              {"role": "user", "content": user_prompt}],
    temperature=0,
    top_p=1
    )
    # print(response)
    result=response.choices[0].message.content
    return result

def create_resume(fields):
    document = Document()

    # Title and Subtitle Formatting
    title_style = document.styles['Heading 1']
    title_font = title_style.font
    title_font.name = 'Arial'
    title_font.size = Pt(24)
    title_font.color.rgb = RGBColor(0, 0, 139)  # Dark Blue

    subtitle_style = document.styles['Heading 2']
    subtitle_font = subtitle_style.font
    subtitle_font.name = 'Arial'
    subtitle_font.size = Pt(14)
    subtitle_font.color.rgb = RGBColor(0, 128, 128)  # Teal

    body_style = document.styles['Normal']
    body_font = body_style.font
    body_font.name = 'Calibri'
    body_font.size = Pt(11)
    body_font.color.rgb = RGBColor(0, 0, 0)  # Black

    # Add Title
    document.add_heading(fields['name'], level=1).alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_heading(fields['contact information'], level=2).alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Add Sections
    for section, content in fields['sections'].items():
        document.add_heading(section, level=2)
        for item in content:
            p = document.add_paragraph(item)
    return document

def save_resume(document, file_name=pdf_path):
    # Check if file exists and if so, that we can write to it
    if os.path.exists(file_name):
        if not os.access(file_name, os.W_OK):
            raise PermissionError(f"No write permission for file: {file_name}")

    try:
        # Save to a temporary file first
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file_name = temp_file.name
        temp_file.close()

        # Saving document to a temporary file
        document.save(temp_file_name)

        # Replace the original file with the temporary file
        os.replace(temp_file_name, file_name)
        print(f"Document successfully saved to {file_name}")

    except PermissionError as e:
        print(f"PermissionError: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # Clean up temporary file, if it exists
        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)