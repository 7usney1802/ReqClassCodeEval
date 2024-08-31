# ReqClassCodeEval
Code Generation and Assessment with CodeT5
This project is a Flask web application that generates Python code based on natural language requirements using the CodeT5 model. It also includes a code assessment feature that evaluates the quality of the generated code.
This project integrates the CodeT5 model to automatically generate Python code from user-provided natural language requirements. The generated code is then evaluated based on predefined metrics to ensure quality. This application is intended to streamline the process of code generation, especially for scenarios where quick prototyping or automation is necessary.
Code Generation: Automatically generate Python code based on natural language requirements using the CodeT5 model.
Code Assessment: Evaluate the quality of the generated code using specific metrics.
RESTful API: Expose a REST API endpoint for generating and assessing code.
Cross-Origin Resource Sharing (CORS): Enabled to allow cross-origin requests, making it easier to integrate with front-end applications.
Installation
Python 3.8 or later
Anaconda (recommended for managing dependencies and environments)
Setting Up the Environment
Clone the repository:

git clone https://github.com/yourusername/ReqClassCodeEval.git
Create a new conda environment and activate it:

bash
Copy code
conda create --name modelsetenv python=3.8
conda activate modelsetenv
Install the required packages:

bash
Copy code
pip install flask flask-cors openai==0.28.0 transformers pytest pylint bandit torch safetensors
Running the Application
Navigate to the project directory:

bash
Copy code
cd path/to/your/project
Start the Flask server:

bash
Copy code
python main.py
Open your web browser and go to http://127.0.0.1:5000 to access the application.

Usage
Once the server is running, you can interact with the application via its REST API.

Example Request
To generate code from a requirement, send a POST request to the /generate endpoint with a JSON body containing the requirement:

json
Copy code
{
  "requirement": "Sort a list of numbers in ascending order."
}
The API will return the generated code along with an assessment of the code's quality.

API Endpoints
POST /generate: Generates Python code based on the provided requirement.

Request Body:

requirement: A string containing the natural language description of the task.
Response:

code: The generated Python code.
assessment: The quality assessment of the generated code.
Project Structure
bash
Copy code
├── main.py                # Main application file
├── requirements.txt       # List of required packages
├── README.md              # Project documentation
└── .gitignore             # Files and directories to be ignored by Git
Contributing
Contributions are welcome! Please fork this repository and submit a pull request with your changes. Make sure to update the README and include tests for any new features.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Hugging Face for providing the CodeT5 model.
The open-source community for providing useful tools and libraries.
