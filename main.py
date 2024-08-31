from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import subprocess
import tempfile
from transformers import pipeline
import re

app = Flask(__name__)
CORS(app, resources={r"/generate": {"origins": "*"}})

# Set your OpenAI API key here
openai.api_key = "sk-I3NrmWMuRSiWHsLVroj93NE6uIQe-1vkq-dzaasHWwT3BlbkFJVZhz3gngj0dUlib_AKA-gV0ev6CsK1h_XdxewT39sA"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    data = request.get_json()
    requirement = data.get('requirement', '').strip()

    if not requirement:
        return jsonify({'classification': None}), 400

    try:
        # Use BART pipeline for zero-shot classification
        classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        labels = ["Functional Requirement", "Non-Functional Requirement", "Security Requirement", "Performance Requirement", "Usability Requirement"]
        result = classifier(requirement, candidate_labels=labels)
        classification = result['labels'][0]

        return jsonify({'classification': classification})

    except Exception as e:
        return jsonify({'classification': f"An error occurred: {str(e)}"}), 500

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    requirement = data.get('requirement', '').strip()

    if not requirement:
        return jsonify({'code': "Requirement is empty. Please provide a valid requirement."}), 400

    try:
        # Use the `gpt-3.5-turbo` model to generate code
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who generates only code without any explanations."},
                {"role": "user", "content": f"Write a Python function to meet the following requirement: {requirement}"}
            ],
            max_tokens=700,
            temperature=0.2,
        )

        # Extract the generated code and clean it
        generated_code = response['choices'][0]['message']['content'].strip()
        cleaned_code = clean_generated_code(generated_code)

        return jsonify({'code': cleaned_code})

    except Exception as e:
        return jsonify({'code': f"An error occurred: {str(e)}"}), 500

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.get_json()
    code = data.get('code', '').strip()

    if not code:
        return jsonify({'evaluation': "No code provided for evaluation."}), 400

    try:
        # Clean the code of any markdown formatting or invalid syntax
        cleaned_code = clean_generated_code(code)

        # AI-Based Evaluation with ChatGPT, including generating and running unit tests
        ai_evaluation = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert software developer. Please evaluate the following code for efficiency, maintainability, and security. Then, write 5 unit tests and run them on the code, providing the result of every test. Please provide detailed feedback and suggestions for improvement. Make it clear and professional. then give the code rating out of 10."},
                {"role": "user", "content": f"Evaluate this code: {cleaned_code}"}
            ],
            max_tokens=1000,
            temperature=0.2,
        )

        ai_feedback = ai_evaluation['choices'][0]['message']['content'].strip()

        # Unit Testing
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(cleaned_code.encode())
            temp_file.close()

            # Running unit tests using pytest (this assumes your generated code has test cases)
            try:
                pytest_result = subprocess.run(['pytest', temp_file.name], capture_output=True, text=True)
                unit_test_feedback = pytest_result.stdout
            except Exception as e:
                unit_test_feedback = f"Unit test execution failed: {str(e)}"

            # Static Analysis using pylint
            pylint_result = subprocess.run(['pylint', temp_file.name], capture_output=True, text=True)
            pylint_feedback = pylint_result.stdout

        # Security Analysis using bandit
        bandit_result = subprocess.run(['bandit', '-r', temp_file.name], capture_output=True, text=True)
        security_feedback = bandit_result.stdout

        evaluation = {
            "ai_feedback": ai_feedback,
            "unit_test_feedback": unit_test_feedback,
            "pylint_feedback": pylint_feedback,
            "security_feedback": security_feedback
        }

        return jsonify({'evaluation': evaluation})

    except Exception as e:
        return jsonify({'evaluation': f"An error occurred: {str(e)}"}), 500

    data = request.get_json()
    code = data.get('code', '').strip()

    if not code:
        return jsonify({'evaluation': "No code provided for evaluation."}), 400

    try:
        # Clean the code of any markdown formatting or invalid syntax
        cleaned_code = clean_generated_code(code)

        # AI-Based Evaluation with ChatGPT
        ai_evaluation = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert software developer. Please evaluate the following code for efficiency, maintainability, and security.then write 5 unittest and run them on the code,Provide the results of every unittest.Please provide detailed feedback and suggestions for improvement. make it clear and professional "},
                {"role": "user", "content": f"Evaluate this code: {cleaned_code}"}
            ],
            max_tokens=800,
            temperature=0.2,
        )

        ai_feedback = ai_evaluation['choices'][0]['message']['content'].strip()

        # Unit Testing
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(cleaned_code.encode())
            temp_file.close()

            # Running unit tests using pytest (this assumes your generated code has test cases)
            try:
                pytest_result = subprocess.run(['pytest', temp_file.name], capture_output=True, text=True)
                unit_test_feedback = pytest_result.stdout
            except Exception as e:
                unit_test_feedback = f"Unit test execution failed: {str(e)}"

            # Static Analysis using pylint
            pylint_result = subprocess.run(['pylint', temp_file.name], capture_output=True, text=True)
            pylint_feedback = pylint_result.stdout

        # Security Analysis using bandit
        bandit_result = subprocess.run(['bandit', '-r', temp_file.name], capture_output=True, text=True)
        security_feedback = bandit_result.stdout

        evaluation = {
            "ai_feedback": ai_feedback,
            "unit_test_feedback": unit_test_feedback,
            "pylint_feedback": pylint_feedback,
            "security_feedback": security_feedback
        }

        return jsonify({'evaluation': evaluation})

    except Exception as e:
        return jsonify({'evaluation': f"An error occurred: {str(e)}"}), 500
import re

import re

def clean_generated_code(code):
    """Extract only the valid Python code, removing markdown, example usage, and placeholder comments."""
    # Remove markdown syntax
    code = re.sub(r'```python', '', code)  # Remove markdown
    code = re.sub(r'```', '', code)  # Remove closing markdown
    
    # Remove example usage and placeholder comments
    lines = code.splitlines()
    cleaned_lines = []
    
    for line in lines:
        # Skip lines that appear to be example usage or placeholders
        if re.search(r'schedule_task\(', line) or "Example usage" in line or "Code to send SMS notification" in line:
            continue
        if line.strip().startswith("schedule_task"):
            continue
        cleaned_lines.append(line)

    # Join lines back into a single string
    cleaned_code = "\n".join(cleaned_lines).strip()
    
    return cleaned_code


if __name__ == "__main__":
    app.run(debug=True)


# Set your OpenAI API key here
#openai.api_key = "sk-I3NrmWMuRSiWHsLVroj93NE6uIQe-1vkq-dzaasHWwT3BlbkFJVZhz3gngj0dUlib_AKA-gV0ev6CsK1h_XdxewT39sA"


