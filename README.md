# README Creator

This file was made with README creator

## Table of Contents

- [Project Description](#project-description)
- [How to Run the Project](#how-to-run-the-project)
- [Badges](#badges)
- [Conclusion](#conclusion)

## Project Description

This project provides a tool to automatically generate README.md files for Python projects.
The tool extracts function headers and their docstrings (or preceding comments if no docstring) from a given Python file, and uses a model to create the README content.

## How to Run the Project

To run the project, you can use the following steps:

1. Install the required dependencies.
2. Clone the project repository.
3. Run the following command:

```
python README_creator.py path/to/python_file.py
```

## Badges

- [![Python](https://img.shields.io/badge/Python-3.8-blue.svg)](https://www.python.org/)
- [![PyPI - License](https://img.shields.io/pypi/l/langchain-core?style=flat-square)](https://opensource.org/licenses/MIT)


## Conclusion

This project has been a great learning experience for me. I have learned a lot about Python, markdown, and machine learning. I am excited to see how this project can be used to help other developers create better README files for their projects.

## Functions

### `model_creator`

This function creates a model.

### `message_creator`

This function creates a list of messages that will be used to invoke the model.

### `extract_functions_with_docstrings`

Extracts function headers and their docstrings (or preceding comments if no docstring) from a Python file.

### `get_function_header`

Reconstructs the function header from an AST node.

### `format_functions_info`

Formats the extracted function information into a single string.

### `generate_readme`

Generates a README.md file by extracting function headers and their descriptions from a given Python file,
and using a model to create the README content.
If the mdel can handle the entire content of the file, it will use the entire content of the file.

Args:
- file_path (str): Path to the Python file from which to extract function information.

