import os
import json
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


def filter_skills_by_indices(skills, skill_type, indices):
    """Filters skills from a specific skill type based on given indices."""
    return [skills[skill_type][i] for i in indices]


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
    skills_json_to_tex("generated_resume.tex")

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
        file.write("\\vspace{-5pt}\n")
        file.write("\\resumeSubHeadingListStart\n")
        file.write("\\resumeProjectHeading\n")

        for project in projects:
            file.write(rf"{{\textbf{{{project['name']}}} $|$")  # Project name
            file.write(r"{\faIcon{code}}" + '\n')  # FontAwesome icon with a new line

            # Add hyperlink if available
            file.write(rf"          \ifHYPERLINKON" + '\n')
            file.write(rf"    \underline{{\href{{{project['link']}}}{{\textcolor{{gray}}{{link}}}}}}" + '\n')
            file.write(rf"          \else" + '\n')
            file.write(rf"          \fi" + '\n')
            file.write("    }" + f"{{{project['dates']}}}\n")

            file.write("    \\resumeItemListStart\n")

            # Always write the description
            for item in project['description']:
                file.write(f"        \\resumeItem{{{item}}}\n")
            file.write("    \\resumeItemListEnd\n\n")
            file.write("    \\resumeItemListEnd\n")


def skills_json_to_tex(filename):
    with open(filename, 'a') as file:  # Open the .tex file in append mode
        file.write("\\vspace{-14pt}\n")
        file.write("\\section{TECHNICAL SKILLS}\n")
        file.write(" \\begin{itemize}[leftmargin=0.15in, label={}]\n")
        file.write("    \\small{\\item{\n")

        # Add the filtered languages
        if selected_languages:
            file.write("     \\textbf{Languages}{: " + ", ".join(selected_languages) + "} \\\\\n")

        # Add the filtered frameworks
        if selected_frameworks:
            file.write("     \\textbf{Frameworks}{: " + ", ".join(selected_frameworks) + "} \\\\\n")

        # Add the filtered developer tools
        if selected_tools:
            file.write("     \\textbf{Developer Tools}{: " + ", ".join(selected_tools) + "} \\\\\n")

        # Add the filtered data science skills
        if selected_data_science:
            file.write("     \\textbf{Data Science/Machine Learning:}{ " + ", ".join(selected_data_science) + "}\n")

        file.write("    }}\n")
        file.write(" \\end{itemize}\n")


# Example usage:

# Provide the indices for the experiences and projects you want to include

experience_indices = [0]  # For example, include the first two experiences
project_indices = [0]  # Include only the first project


############# DEV #####################

# Select all indices for a given skill type
def select_all_indices(skills, skill_type):
    return list(range(len(skills[skill_type])))


languages_indices = select_all_indices(resume_data['technical_skills'], 'languages')
frameworks_indices = select_all_indices(resume_data['technical_skills'], 'frameworks')
tools_indices = select_all_indices(resume_data['technical_skills'], 'developer_tools')
data_science_indices = select_all_indices(resume_data['technical_skills'], 'data_science_machine_learning')

# # skills indices
# languages_indices = [1, 2, 3]  # Select specific languages
# frameworks_indices = [0, 1]  # Select specific frameworks
# tools_indices = [2, 3]  # Select specific developer tools
# data_science_indices = [0, 2, 4]  # Select specific data science/machine learning skills


selected_experiences = filter_items_by_indices(resume_data['experience'], experience_indices)
selected_projects = filter_items_by_indices(resume_data['projects'], project_indices)

# Filtered skills by indices
selected_languages = filter_skills_by_indices(resume_data['technical_skills'], 'languages', languages_indices)
selected_frameworks = filter_skills_by_indices(resume_data['technical_skills'], 'frameworks', frameworks_indices)
selected_tools = filter_skills_by_indices(resume_data['technical_skills'], 'developer_tools', tools_indices)
selected_data_science = (
    filter_skills_by_indices(resume_data['technical_skills'],
                             'data_science_machine_learning', data_science_indices))

# Generate and compile the LaTeX resume

generate_latex(resume_data, selected_experiences, selected_projects)
print(selected_experiences)
print(selected_data_science)
