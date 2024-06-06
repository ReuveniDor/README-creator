import getpass
import os
import ast
import sys
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import GoogleGenerativeAI 
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

class READMEGenerator:
    '''
    # This code creates a REDME file for a project
    # The code uses the GoogleGenerativeAI model=gemini-pro to create the README file
    # This code uses LangChain as the underlying library to interact with the model

    # To use the code please place the file in the same directory as the file you want to create a README for
    # run the code using the following command from the terminal: python README_creator_modified.py <directory path>
    # You will ne asked to provide your Google API Key
    # The README file will be created in the same directory as the file you want to create a README for

    A class that generates a README file for a project based on the code provided.

    Attributes:
        directory (str): The directory path where the project files are located.
        model (GoogleGenerativeAI): The GoogleGenerativeAI model used for generating the README text.

    Methods:
        __init__(self, directory): Initializes the READMEGenerator object.
        model_creator(self): Creates and returns the GoogleGenerativeAI model.
        message_creator(self, human_message): Creates a list of messages to invoke the model.
        extract_info(self, file_content): Extracts class and function information from the file content.
        extract_function_info(self, node, lines): Extracts function information from the AST node.
        get_function_header(self, node): Generates the function header string.
        format_info(self, classes_info, functions_info): Formats the class and function information into a string.
        process_directory(self, directory): Processes the directory to get all file contents.
        generate_readme(self): Generates the README file based on the project code.
    '''
    def __init__(self, directory):
        self.directory = directory
        self.model = self.model_creator()

    def model_creator(self):
        # Setting the GOOGLE_API_KEY API key
        if "GOOGLE_API_KEY" not in os.environ:
            os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API Key")
        
        # Creating a model
        model = GoogleGenerativeAI(model="gemini-pro")
        return model

    def message_creator(self, human_message):
        # Creating the list of messages to invoke the model
        messages = [
            SystemMessage(content="Create a README text for the project that will be represented by the code in the document provided."),
            SystemMessage(content="The README text should include: Project's Title, Project Description, Table of Contents, How to run the Project (only if stated in the project), Badges, Conclusion."),
            SystemMessage(content="The Badges should include things from imports, Conclusion should describe things that the user learned from this project preparations."),
            SystemMessage(content="The format of the README text should be in markdown format."),
            HumanMessage(content=human_message)
        ]
        return messages

    def extract_info(self, file_content):
        # Parse the file content into an AST
        tree = ast.parse(file_content)

        # Initialize lists to hold class and function definitions and their docstrings
        classes_info = []
        functions_info = []

        # Split the file content into lines to match line numbers with comments
        lines = file_content.splitlines()

        # Traverse the AST to find class and function definitions
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                class_docstring = ast.get_docstring(node) or "No docstring provided."
                classes_info.append({
                    "type": "class",
                    "name": class_name,
                    "docstring": class_docstring
                })
                for child in node.body:
                    if isinstance(child, ast.FunctionDef):
                        functions_info.append(self.extract_function_info(child, lines))
            elif isinstance(node, ast.FunctionDef):
                functions_info.append(self.extract_function_info(node, lines))

        return classes_info, functions_info

    def extract_function_info(self, node, lines):
        function_name = node.name
        docstring = ast.get_docstring(node) or None
        function_header = self.get_function_header(node)
        current_comments = []

        # Capture comments before the function definition if no docstring is provided
        if docstring is None:
            lineno = node.lineno
            for i in range(lineno - 2, -1, -1):
                line = lines[i].strip()
                if line.startswith("#"):
                    current_comments.insert(0, line.lstrip("#").strip())
                else:
                    break
            docstring = "\n".join(current_comments) if current_comments else "No docstring provided."

        return {
            "header": function_header,
            "docstring": docstring
        }

    def get_function_header(self, node):
        header = f"def {node.name}("
        args = [arg.arg for arg in node.args.args]
        header += ", ".join(args) + "):"
        return header

    def format_info(self, classes_info, functions_info):
        formatted_string = ""
        for cls in classes_info:
            formatted_string += f"class {cls['name']}:\n"
            formatted_string += f"    {cls['docstring']}\n\n"

        for func in functions_info:
            formatted_string += f"{func['header']}\n"
            formatted_string += f"{func['docstring']}\n\n"

        return formatted_string

    def process_directory(self, directory):
        all_contents = ""
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py") or file.endswith(".ipynb"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        all_contents += f.read() + "\n\n"
        return all_contents

    def generate_readme(self):
        # Process the directory to get all file contents
        all_contents = self.process_directory(self.directory)
        if len(all_contents) > 4000:
            classes_info, functions_info = self.extract_info(all_contents)
            formatted_string = self.format_info(classes_info, functions_info)
        else:
            formatted_string = all_contents

        message = self.message_creator(formatted_string)
        result = self.model.invoke(message)

        # Define the path to save the README.md file
        readme_path = os.path.join(self.directory, "README.md")

        # Write the content to the file
        with open(readme_path, "w", encoding="utf-8") as file:
            file.write(result)

# The directory of the project to create the README for
project_directory = sys.argv[1]

# Generate the README file
readme_generator = READMEGenerator(project_directory)
readme_generator.generate_readme()