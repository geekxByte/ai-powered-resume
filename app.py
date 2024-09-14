import os
from flask import Flask, render_template, request, send_file, flash
import openai
from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for flashing messages

def parse_pdf(pdf_file):
    """
    Extract text from a PDF file using pdfminer.six.
    """
    output_string = StringIO()
    extract_text_to_fp(pdf_file, output_string, laparams=LAParams(), output_type='text', codec='utf-8')
    return output_string.getvalue()

def generate_ai_resume(api_key, pdf_text):
    """
    Generate an HTML resume using the OpenAI API.
    """
    openai.api_key = api_key
    
    system_message = """
    You are an AI assistant specialized in creating well-structured, visually appealing HTML resumes. 
    Your task is to analyze the given text from a LinkedIn PDF and generate a 
    professional HTML resume. The HTML should include appropriate semantic tags, 
    classes for styling, and embedded CSS for a clean, modern, and visually attractive look.
    """

    user_message = f"""
    Please create an HTML resume based on the following LinkedIn PDF content:

    {pdf_text}

    Ensure the HTML includes:
    1. A header with the person's name and contact information
    2. Sections for Summary, Experience, Education, and Skills
    3. Proper semantic HTML5 tags (header, main, section, etc.)
    4. Classes for styling
    5. Embedded CSS for a clean, professional, and visually appealing look
    6. Any other relevant sections found in the PDF content
    7. Use of appropriate icons (you can use Font Awesome or similar icon libraries)
    8. A two-column layout for better use of space
    9. Subtle use of colors to enhance readability and visual appeal

    Return only the HTML code, nothing else.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"AI resume generation failed: {str(e)}")
        return None

def generate_fallback_resume(pdf_text):
    """
    Generate a fallback HTML resume based on simple parsing of the PDF text.
    """
    lines = pdf_text.split('\n')
    
    name = lines[0].strip()
    contact_info = ' | '.join(line.strip() for line in lines[1:5] if line.strip())
    
    sections = {
        "Technical Skills": [],
        "Education": [],
        "Experience": [],
        "Projects": [],
        "Achievements": [],
        "Profile Links": []
    }
    
    current_section = ""
    
    for line in lines[5:]:
        line = line.strip()
        if line in sections:
            current_section = line
        elif line and current_section:
            sections[current_section].append(line)
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{name} - Resume</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f0f2f5;
            }}
            .resume-container {{
                background-color: #ffffff;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 40px;
                display: grid;
                grid-template-columns: 2fr 1fr;
                gap: 40px;
            }}
            h1 {{
                color: #2c3e50;
                margin-bottom: 10px;
                grid-column: 1 / -1;
            }}
            h2 {{
                color: #34495e;
                border-bottom: 2px solid #ecf0f1;
                padding-bottom: 10px;
                margin-top: 30px;
            }}
            .contact-info {{
                grid-column: 1 / -1;
                color: #7f8c8d;
                margin-bottom: 20px;
            }}
            .main-column {{
                grid-column: 1 / 2;
            }}
            .side-column {{
                grid-column: 2 / 3;
            }}
            .section {{
                margin-bottom: 30px;
            }}
            ul {{
                padding-left: 20px;
            }}
            li {{
                margin-bottom: 10px;
            }}
            .icon {{
                margin-right: 10px;
                color: #3498db;
            }}
        </style>
    </head>
    <body>
        <div class="resume-container">
            <h1>{name}</h1>
            <div class="contact-info">{contact_info}</div>
            
            <div class="main-column">
                <div class="section">
                    <h2><i class="fas fa-user-tie icon"></i>Summary</h2>
                    <p>{sections['Technical Skills'][0] if sections['Technical Skills'] else 'Professional summary not available.'}</p>
                </div>
                
                <div class="section">
                    <h2><i class="fas fa-briefcase icon"></i>Experience</h2>
                    <ul>
                        {"".join(f"<li>{item}</li>" for item in sections['Experience'])}
                    </ul>
                </div>
                
                <div class="section">
                    <h2><i class="fas fa-project-diagram icon"></i>Projects</h2>
                    <ul>
                        {"".join(f"<li>{item}</li>" for item in sections['Projects'])}
                    </ul>
                </div>
            </div>
            
            <div class="side-column">
                <div class="section">
                    <h2><i class="fas fa-graduation-cap icon"></i>Education</h2>
                    <ul>
                        {"".join(f"<li>{item}</li>" for item in sections['Education'])}
                    </ul>
                </div>
                
                <div class="section">
                    <h2><i class="fas fa-cogs icon"></i>Technical Skills</h2>
                    <ul>
                        {"".join(f"<li>{item}</li>" for item in sections['Technical Skills'][1:] if sections['Technical Skills'])}
                    </ul>
                </div>
                
                <div class="section">
                    <h2><i class="fas fa-trophy icon"></i>Achievements</h2>
                    <ul>
                        {"".join(f"<li>{item}</li>" for item in sections['Achievements'])}
                    </ul>
                </div>
                
                <div class="section">
                    <h2><i class="fas fa-link icon"></i>Profile Links</h2>
                    <ul>
                        {"".join(f"<li>{item}</li>" for item in sections['Profile Links'])}
                    </ul>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            flash('No file part in the request. Please try again.', 'error')
            return render_template('index.html')
        
        file = request.files['pdf_file']
        api_key = request.form.get('api_key', '')
        
        if file.filename == '':
            flash('No file selected. Please choose a file and try again.', 'error')
            return render_template('index.html')

        if file:
            try:
                pdf_text = parse_pdf(file)
                
                if api_key:
                    html_resume = generate_ai_resume(api_key, pdf_text)
                    if html_resume is None:
                        flash('AI-powered resume generation failed. Falling back to simple HTML generation.', 'warning')
                        html_resume = generate_fallback_resume(pdf_text)
                else:
                    flash('No API key provided. Using simple HTML generation.', 'info')
                    html_resume = generate_fallback_resume(pdf_text)

                # Save the HTML resume
                with open('resume.html', 'w', encoding='utf-8') as f:
                    f.write(html_resume)

                return send_file('resume.html', as_attachment=True)
            except Exception as e:
                flash(f'An error occurred while processing your file: {str(e)}', 'error')
                return render_template('index.html')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
