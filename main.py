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

    with open('resume_template.tex', 'r') as template_file:
        latex_template = template_file.read()

    # Write the rendered LaTeX to a file
    with open("generated_resume.tex", "w") as f:
        f.write(latex_template)

    experiences_json_to_tex(selected_experiences, "generated_resume.tex")
    projects_json_to_tex(selected_projects, "generated_resume.tex")

    with open("generated_resume.tex", 'a') as file:
        file.write("\\end{document}\n")


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


def experiences_json_to_tex(experiences, filename):
    with open(filename, 'a') as file:  # Open the .tex file in append mode
        file.write("%-----------EXPERIENCE -----------\n\n")
        file.write("\\vspace{-15pt}\n")
        file.write("\\section{EXPERIENCE}\n")
        file.write("\\resumeSubHeadingListStart\n")
        for experience in experiences:
            file.write("\\resumeSubheading\n")
            file.write(f"    {{{experience['title']}}}{{{experience['dates']}}}\n")
            file.write(f"    {{{experience['company']}}}{{{experience['location']}}}\n")
            file.write("    \\resumeItemListStart\n")
            for item in experience['description']:
                file.write(f"        \\resumeItem{{{item}}}\n")
            file.write("    \\resumeItemListEnd\n\n")
        file.write("\\resumeSubHeadingListEnd\n\n")


def projects_json_to_tex(projects, filename):
    with open(filename, 'a') as file:  # Open the .tex file in append mode
        file.write("%-----------PROJECTS -----------\n\n")
        file.write("\\vspace{-15pt}\n")
        file.write("\\section{PROJECTS}\n")
        file.write("\\resumeSubHeadingListStart\n")

        for project in projects:
            file.write(rf"{{\textbf{{{project['name']}}} $|$" + '\n')  # Project name
            file.write(r"          {\faIcon{code}}\n" + '\n')  # FontAwesome icon with a new line

            # Add hyperlink if available
            file.write(rf"          \ifHYPERLINKON" + '\n')
            file.write(rf"          \underline{{\href{{{project['link']}}}{{\textcolor{{gray}}{{link}}}}}}" + '\n')
            file.write(rf"          \else" + '\n')
            file.write(rf"          \fi" + '\n')
            file.write(rf"" + '\n')

            file.write("    \\resumeItemListStart\n")



            # Always write the description
            for item in project['description']:
                file.write(f"        \\resumeItem{{{item}}}\n")
            file.write("    \\resumeItemListEnd\n\n")



# def projects_json_to_tex(projects, filename):
#     with open(filename, 'a') as file:  # Open the .tex file in append mode
#         file.write("%-----------PROJECTS -----------\n\n")
#         file.write("\\vspace{-14pt}\n")
#         file.write("\\section{PROJECTS}\n")
#         file.write("\\vspace{-5pt}\n")
#         file.write("\\resumeSubHeadingListStart\n")
#         for project in projects:
#             file.write("      \\resumeProjectHeading\n")
#             file.write(f"          {{\\textbf{{{project['name']}}} $|$ \n")
#             file.write(f"          {{\\faIcon{{code}}}} \n")
#             file.write("          \\ifHYPERLINKON\n")
#             file.write(f"    \\underline{{\\href{{{project['link']}}}{{\\textcolor{{gray}}{{link}}}}}}\n")
#             file.write("          \\else\n")
#             file.write("          \\fi\n")
#             file.write(f"          }}{{{project['dates']}}}\n")
#             file.write("          \\resumeItemListStart\n")
#
#             for item in project['description']:
#                 file.write(f"            \\resumeItem{{{item}}}\n")
#
#             file.write("          \\resumeItemListEnd\n")
#             file.write("          \\vspace{-15pt}\n")
#
#         file.write("    \\resumeSubHeadingListEnd\n\n")


# Example usage:

# Provide the indices for the experiences and projects you want to include

experience_indices = [0]  # For example, include the first two experiences
project_indices = [0]  # Include only the first project

# Optionally, you can use the OpenAI function to extract keywords from a job description
# job_description = "Looking for a software engineer experienced in Python, Docker, and REST APIs."
# keywords = extract_keywords_openai(job_description)
# print("Extracted Keywords:", keywords)

# Filter the experiences and projects based on the indices


# STUB
# selected_experiences = 0
# selected_projects = 0

selected_experiences = filter_items_by_indices(resume_data['experience'], experience_indices)
selected_projects = filter_items_by_indices(resume_data['projects'], project_indices)

# Generate and compile the LaTeX resume

generate_latex(resume_data, selected_experiences, selected_projects)
