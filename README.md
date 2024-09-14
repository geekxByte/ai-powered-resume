# LinkedIn PDF to HTML Resume Converter

This Flask web application converts LinkedIn PDF resumes into well-formatted HTML resumes. It uses OpenAI's GPT-3.5-turbo model to generate a professional HTML layout if an API key is provided. If the API rate limit is exceeded or no API key is given, it falls back to a simpler HTML generation method.

## Features

- **PDF Parsing**: Extracts text from LinkedIn PDF resumes.
- **AI-Powered Resume Generation**: Utilizes OpenAI API to create a polished HTML resume.
- **Fallback HTML Generation**: Provides a basic but functional HTML resume layout if AI generation fails.
- **User Interface**: Simple and clean web form for uploading PDF files and entering the OpenAI API key.

## Prerequisites

- Python 3.8 or higher
- Flask
- `pdfminer.six`
- `openai` Python library

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/linkedin-pdf-to-html-resume.git
    cd linkedin-pdf-to-html-resume
    ```

2. **Create and Activate a Virtual Environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Required Packages**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` File**

    The application does not use a `.env` file directly, but it’s good practice to keep environment variables for OpenAI API key and other secrets. Create a `.env` file in the root directory with your API key:

    ```text
    OPENAI_API_KEY=your_openai_api_key_here
    ```

## Usage

1. **Run the Flask Application**

    ```bash
    python app.py
    ```

2. **Access the Web Interface**

    Open your browser and navigate to `http://127.0.0.1:5000/`.

3. **Upload a LinkedIn PDF**

    - Select the LinkedIn PDF file to upload.
    - Enter your OpenAI API key (optional).
    - Click "Generate HTML Resume."

4. **Download the HTML Resume**

    Once the processing is complete, the generated HTML resume will be available for download.

## Approach

1. **PDF Parsing**:
    - Uses `pdfminer.six` to extract text from the provided LinkedIn PDF.
    - Extracted text is then processed to identify and categorize different sections of the resume.

2. **AI-Powered Resume Generation**:
    - If an OpenAI API key is provided, the application sends a request to OpenAI's GPT-3.5-turbo model with instructions to generate a well-formatted HTML resume.
    - The AI generates HTML with semantic tags and styling based on the provided PDF content.

3. **Fallback HTML Generation**:
    - If no API key is provided or if the AI generation fails, the application uses a predefined fallback method to generate a basic HTML resume.
    - The fallback method parses the extracted text and organizes it into sections such as Experience, Education, and Skills.

4. **Error Handling**:
    - The application handles various errors such as missing files, API errors, and file processing issues.
    - Flash messages are used to inform users of errors or important information.
