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
    
    
    %%%%%%%%%%%%%%%%%%%%%%%HYPERLINKS%%%%%%%%%%%%%%%%%%%%%%%%

    % Define the HYPERLINKON variable
    \newif\ifHYPERLINKON
    \HYPERLINKONtrue  % Change to \HYPERLINKONfalse to disable hyperlinks


    %----------FONT OPTIONS----------
    % sans-serif
    % \usepackage[sfdefault]{FiraSans}
    % \usepackage[sfdefault]{roboto}
    % \usepackage[sfdefault]{noto-sans}
    % \usepackage[default]{sourcesanspro}
    
    % serif
    % \usepackage{CormorantGaramond}
    % \usepackage{charter}
    
    \usepackage{helvet}
    \renewcommand{\familydefault}{\sfdefault}
    \usepackage[T1]{fontenc}
    
    \pagestyle{fancy}
    \fancyhf{} % clear all header and footer fields
    \fancyfoot{}
    \renewcommand{\headrulewidth}{0pt}
    \renewcommand{\footrulewidth}{0pt}
    
    % Adjust margins
    \addtolength{\oddsidemargin}{-0.6in}
    \addtolength{\evensidemargin}{-0.5in}
    \addtolength{\textwidth}{1.19in}
    \addtolength{\topmargin}{-.7in}
    \addtolength{\textheight}{1.4in}
    
    \urlstyle{same}
    
    \raggedbottom
    \raggedright
    \setlength{\tabcolsep}{0in}
    
    % Sections formatting
    \titleformat{\section}{
    \vspace{-4pt}\scshape\raggedright\large\bfseries\color{UBCblue}
    }{}{0em}{}[\color{UBCblue}\titlerule \vspace{-5pt}]
    % Ensure that generate pdf is machine readable/ATS parsable
    \pdfgentounicode=1
    
    %-------------------------
    % Custom commands
    
    {% raw %}
    
    \newcommand{\resumeItem}[1]{
      \item\small{
        {#1 \vspace{-2pt}}
      }
    }
    
    \newcommand{\classesList}[4]{
        \item\small{
            {#1 #2 #3 #4 \vspace{-2pt}}
      }
    }
    
    \newcommand{\resumeSubheading}[4]{
      \vspace{-2pt}\item
        \begin{tabular*}{1.0\textwidth}[t]{l@{\extracolsep{\fill}}r}
          \textbf{#1} & \textbf{\small \textcolor{gray}{#2}} \\
          \textit{\small#3} & \textit{\small {\textcolor{gray}{#4}}} \\
        \end{tabular*}\vspace{-7pt}
    }
    
    
    \newcommand{\resumeSubSubheading}[2]{
        \item
        \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
          \textit{\small#1} & \textit{\small #2} \\
        \end{tabular*}\vspace{-7pt}
    }
    
    \newcommand{\resumeProjectHeading}[2]{
        \item
        \begin{tabular*}{1.001\textwidth}{l@{\extracolsep{\fill}}r}
          \textbf{\small #1} & \textbf{\small \textcolor{gray}{#2}}\\
        \end{tabular*}\vspace{-7pt}
    }
    
    
    \newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}
    
    {% endraw %}
    
    %%%%%%%%%%%%%%%%%%%% ADDING RAW AND ENDRAW MAKES JINJA NOT INTERPRET THE ABOVE AS COMMANDS %%%%%
    
    \renewcommand\labelitemi{$\vcenter{\hbox{\tiny$\bullet$}}$}
    \renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}
    
    \newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.0in, label={}]}
    \newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
    \newcommand{\resumeItemListStart}{\begin{itemize}}
    \newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}
    
    \definecolor{UBCblue}{HTML}{0b133c}
    
    %-------------------------------------------
    %%%%%%  RESUME STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    % Other packages and configurations
    \usepackage{graphicx}
    \usepackage[empty]{fullpage}
    \usepackage{fancyhdr}
    % ... all other packages and custom commands
    
    \pagestyle{fancy}
    \fancyhf{} % clear all header and footer fields
    \fancyfoot{}
    \renewcommand{\headrulewidth}{0pt}
    \renewcommand{\footrulewidth}{0pt}
    % Adjust margins
    % ... margin adjustments and other configurations
    
    
    % Other packages and configurations
    \usepackage{graphicx}
    \usepackage[empty]{fullpage}
    \usepackage{fancyhdr}
    % ... all other packages and custom commands
    
    \pagestyle{fancy}
    \fancyhf{} % clear all header and footer fields
    \fancyfoot{}
    \renewcommand{\headrulewidth}{0pt}
    \renewcommand{\footrulewidth}{0pt}
    % Adjust margins
    % ... margin adjustments and other configurations
    
    \begin{document}
    
    % Trying to eliminate all margins for the image
    \noindent
    \begin{minipage}{\textwidth}
    
      
      \vspace*{-40pt} % Adjust as needed to reduce space before the heading
    \end{minipage}
    
    % Your heading and rest of the resume content
    
    \vspace{-13pt}
    {\color{UBCblue}\huge \scshape 
    \textbf{Danial Zoraiz Ramzan}} \\ \vspace{1pt}
    {\color{UBCblue}Vancouver, BC • Canadian Citizen • \faGlobe \hspace{0.in} 
    \underline{\ifHYPERLINKON\href{https://danialramzan.github.io/}{danialramzan.github.io/}\else 
    danialramzan.github.io/\fi}} \\ \vspace{1pt}
    {\color{UBCblue}\small 
    \raisebox{-0.1\height}{\faIcon{phone-square-alt}} 
    \underline{\ifHYPERLINKON\href{tel:+12369962015}{1-236-996-2015}\else 1-236-996-2015\fi} ~ 
    \raisebox{-0.2\height}{\faIcon{envelope-square}} 
    \underline{\ifHYPERLINKON\href{mailto:danrmzn@student.ubc.ca}{danrmzn@student.ubc.ca}\else danrmzn@student.ubc.ca\fi}  ~ 
    \raisebox{-0.2\height}{\faLinkedin\ \underline{\ifHYPERLINKON\href{https://linkedin.com/in/danialramzan}{linkedin.com/in/danialramzan}\else linkedin.com/in/danialramzan\fi}}  ~
    \raisebox{-0.2\height}{\faGithubSquare\ \underline{\ifHYPERLINKON\href{https://github.com/danialramzan}{github.com/danialramzan}\else github.com/danialramzan\fi}}}
    \vspace{-8pt}
    
    % The rest of your document content follows...
    
    % The rest of your document starts here


    \setlength{\parskip}{0pt} % Reduce space between paragraphs
    \setlength{\parindent}{0pt} % No paragraph indent


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
        # experiences=experiences,
        # projects=projects
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


# STUB
selected_experiences = 0
selected_projects = 0

#selected_experiences = filter_items_by_indices(resume_data['experience'], experience_indices)
#selected_projects = filter_items_by_indices(resume_data['projects'], project_indices)

# Generate and compile the LaTeX resume
generate_latex(resume_data, selected_experiences, selected_projects)