import getpass
import os
import ast
import sys
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import GoogleGenerativeAI 
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

# This code creates a REDME file for a project
# The code uses the GoogleGenerativeAI model=gemini-pro to create the README file
# This code uses LangChain as the underlying library to interact with the model

# To use the code please place the file in the same directory as the file you want to create a README for
# run the code using the following command from the terminal: python README_creator.py <file_name>
# You will ne asked to provide your Google API Key
# The README file will be created in the same directory as the file you want to create a README for

# Funcions:
# model_creator: This function creates a model
def model_creator():
    # Setting the GOOGLE_API_KEY API key
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API Key")

    # Creating a model
    model = GoogleGenerativeAI (model="gemini-pro")
    return model

# message_creator: This function creates a list of messages that will be used to invoke the model
def message_creator(human_message):
    # Invoking the model
    messages = [
        SystemMessage(content="Create a README text for the project that will be represented by the code in the document provided."),
        SystemMessage(content="The README text should iclude: Project's Title, Project Description, Table of Contents, How to run the Project (only if stated in the project), Badges, Conclution ."),
        SystemMessage(content="The Badges should include things from imports, Conclution should describe things that the user learned from this project preperations."),
        SystemMessage(content="The format of the README text should be in markdown format."),
        HumanMessage(content=human_message)
    ]
    return messages
    loader = DirectoryLoader(directory, glob="**/*.py", loader_cls=PythonLoader)
    PYTHON_CODE = loader.load()
    python_splitter = RecursiveCharacterTextSplitter.from_language(language=Language.PYTHON, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    if len(PYTHON_CODE[0].page_content) > 4000:
        python_docs = python_splitter.create_documents([PYTHON_CODE[0].page_content])
    else:
        python_docs = PYTHON_CODE
    return python_docs

# Extracts function headers and their docstrings (or preceding comments if no docstring) from a Python file.
def extract_functions_with_docstrings(file_content):

    # Parse the file content into an AST
    tree = ast.parse(file_content)
    
    # Initialize a list to store current comments
    current_comments = []

    # List to hold function definitions and their docstrings
    functions_info = []

    # Split the file content into lines to match line numbers with comments
    lines = file_content.splitlines()

    # Traverse the AST to find function definitions
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            docstring = ast.get_docstring(node) or None
            function_header = get_function_header(node)
            
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

            # Store the function header and docstring
            functions_info.append({
                "header": function_header,
                "docstring": docstring
            })
            
            # Clear the current comments for the next function
            current_comments = []

    return functions_info

# Reconstructs the function header from an AST node.
def get_function_header(node):
    header = f"def {node.name}("
    args = [arg.arg for arg in node.args.args]
    header += ", ".join(args) + "):"
    return header

# Formats the extracted function information into a single string.
def format_functions_info(functions_info):
    formatted_string = ""
    for func in functions_info:
        formatted_string += f"{func['header']}\n"
        formatted_string += f"{func['docstring']}\n\n"
    return formatted_string

def generate_readme(file_path):
    """
    Generates a README.md file by extracting function headers and their descriptions from a given Python file,
    and using a model to create the README content.
    If the mdel can handle the entire content of the file, it will use the entire content of the file.

    Args:
    - file_path (str): Path to the Python file from which to extract function information.

    Example usage:
    generate_readme("README creator.py")
    """
    with open(file_path, "r") as file:
        file_content = file.read()
    if len(file_content) > 4000:
        functions_info = extract_functions_with_docstrings(file_content)
        formatted_string = format_functions_info(functions_info)
    else:
        formatted_string = file_content

    message = message_creator(formatted_string)
    model = model_creator()
    result = model.invoke(message)

    # Define the path to save the README.md file
    readme_path = "README.md"

    # Write the content to the file
    with open(readme_path, "w") as file:
        file.write(result)

#Generatess the README file using the provided file
generate_readme(sys.argv[1])