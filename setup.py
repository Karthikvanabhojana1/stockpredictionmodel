"""
Setup script for Soros Chatbot
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="soros-chatbot",
    version="1.0.0",
    author="AI Assistant",
    author_email="assistant@example.com",
    description="A chatbot that speaks like George Soros with PDF processing capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/soros-chatbot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.3.0",
        "langchain>=0.0.350",
        "langchain-openai>=0.0.2",
        "langchain-community>=0.0.10",
        "transformers>=4.35.2",
        "torch>=2.1.1",
        "accelerate>=0.24.1",
        "PyPDF2>=3.0.1",
        "pdfplumber>=0.10.2",
        "pymupdf>=1.23.8",
        "nltk>=3.8.1",
        "spacy>=3.7.2",
        "textract>=1.6.5",
        "streamlit>=1.28.1",
        "gradio>=4.0.2",
        "pandas>=2.1.3",
        "numpy>=1.24.3",
        "scikit-learn>=1.3.2",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.2",
        "tiktoken>=0.5.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "black>=23.11.0",
            "flake8>=6.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "soros-chatbot=cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.txt", "*.md"],
    },
) 