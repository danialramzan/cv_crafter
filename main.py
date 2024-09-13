import os
import json
from jinja2 import Template
import subprocess
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

# Load OpenAI API key from the .env file
openai_api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_api_key

# Load the JSON data from a file
with open("resume_data.json", "r") as f:
    resume_data = json.load(f)


# Function to filter experiences and projects based on indices
def filter_items_by_indices(items, indices):
    return [item for item in items if item['index'] in indices]


# Function to generate LaTeX from filtered data
def generate_latex(resume_data, experiences, projects):
    # Define the LaTeX template
    latex_template = r"""
    \documentclass[letterpaper,11pt]{article}
    
    \usepackage{latexsym}
    \usepackage[empty]{fullpage}
    \usepackage{graphicx}
    \usepackage{titlesec}
    \usepackage{marvosym}
    \usepackage{xcolor}
    \usepackage[usenames,dvipsnames]{color}
    \usepackage{verbatim}
    \usepackage{enumitem}
    \usepackage[hidelinks]{hyperref}
    \usepackage{fancyhdr}
    \usepackage[english]{babel}
    \usepackage{tabularx}
    \usepackage{fontawesome5}
    \usepackage{multicol}
    \setlength{\multicolsep}{-3.0pt}
    \setlength{\columnsep}{-1pt}
    \input{glyphtounicode}
    \usepackage{caption}
    \usepackage[margin=1in,bottom=0.2in,marginparwidth=0.8in,marginparsep=0.1in]{geometry}

    


    \setlength{\parskip}{0pt} % Reduce space between paragraphs
    \setlength{\parindent}{0pt} % No paragraph indent

    \begin{document}

    %-----------HEADER-----------
    {\color{blue}\huge\scshape\textbf{{{ name}}}}

 %   \vspace{1pt}
 %   {{ location }} • \href{mailto:{{ email }}}{{ email }} ~ 
  %  \href{tel:+{{ phone }}}{{ phone }} ~ 
 %   \href{{ linkedin }}{{ linkedin }} ~ 
 %   \href{{ github }}{{ github }}

 %   %-----------EXPERIENCE-----------
   % \section{EXPERIENCE}
  %  \begin{itemize}
  %      {% for exp in experiences %}
  %      \item \textbf{{ exp.title }} at {{ exp.company }} | {{ exp.location }} ({{ exp.dates }})
   %     \begin{itemize}
   %         {% for desc in exp.description %}
   %         \item {{ desc | safe }}
  %          {% endfor %}
 %       \end{itemize}
 %       {% endfor %}
 %   \end{itemize}
%
  %  %-----------PROJECTS-----------
 %   \section{PROJECTS}
  %  \begin{itemize}
%        {% for proj in projects %}
  %      \item \textbf{{ proj.name }} | \href{{ proj.link }}{{ proj.name }} ({{ proj.dates }})
  %      \begin{itemize}
   %         {% for desc in proj.description %}
  %          \item {{ desc | safe }}
 %           {% endfor %}
 %       \end{itemize}
 %       {% endfor %}
  %  \end{itemize}
%
    \end{document}
    """

    # Create a Jinja2 template
    template = Template(latex_template)

    # Render the LaTeX template with the provided resume data
    rendered_latex = template.render(
        name=resume_data['name'],
        location=resume_data['location'],
        email=resume_data['email'],
        phone=resume_data['phone'],
        github=resume_data['github'],
        linkedin=resume_data['linkedin'],
        experiences=experiences,
        projects=projects
    )

    # Write the rendered LaTeX to a file
    with open("generated_resume.tex", "w") as f:
        f.write(rendered_latex)

    # Compile the LaTeX file to PDF using pdflatex
    subprocess.run(["pdflatex", "generated_resume.tex"])


# Function to extract keywords from a job description using OpenAI
def extract_keywords_openai(job_description):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Extract key skills and responsibilities from this job description: {job_description}",
        max_tokens=150,
    )
    return response.choices[0].text.strip()


# Example usage:

# Provide the indices for the experiences and projects you want to include
experience_indices = [0, 1]  # For example, include the first two experiences
project_indices = [0]  # Include only the first project

# Optionally, you can use the OpenAI function to extract keywords from a job description
# job_description = "Looking for a software engineer experienced in Python, Docker, and REST APIs."
# keywords = extract_keywords_openai(job_description)
# print("Extracted Keywords:", keywords)

# Filter the experiences and projects based on the indices
selected_experiences = filter_items_by_indices(resume_data['experience'], experience_indices)
selected_projects = filter_items_by_indices(resume_data['projects'], project_indices)

# Generate and compile the LaTeX resume
generate_latex(resume_data, selected_experiences, selected_projects)
