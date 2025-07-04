# NeuroScribe PDF Copilot

NeuroScribe PDF Copilot is a smart PDF application designed to enhance your PDF editing experience by integrating advanced text detection, editing capabilities, and AI-powered assistance through OpenAI's GPT. This application allows users to upload PDF documents, detect and edit text blocks, and utilize AI commands for improved text manipulation.

## Features

- **PDF Upload**: Easily upload PDF documents for editing.
- **Text Block Detection**: Automatically detect text blocks within the PDF, preserving formatting details.
- **Text Editing**: Edit detected text blocks directly within the application, with options to erase or modify text.
- **GPT Copilot Commands**: Leverage OpenAI's GPT for text rewriting, summarization, and other AI-driven text manipulations.
- **Secure API Key Management**: Store your OpenAI API key securely using environment variables.

## Project Structure

```
neuroscribe-pdf-copilot
├── src
│   ├── app.py                # Main entry point for the Streamlit application
│   ├── components
│   │   ├── pdf_upload.py     # Functions for handling PDF uploads
│   │   ├── text_detection.py  # Functions for detecting text blocks
│   │   ├── text_editing.py    # Functions for editing text blocks
│   │   └── gpt_copilot.py     # Functions for interacting with OpenAI API
│   ├── utils
│   │   ├── pdf_utils.py      # Utility functions for PDF manipulation
│   │   └── openai_utils.py    # Utility functions for OpenAI API interactions
│   └── __init__.py           # Marks the directory as a Python package
├── .env                       # Environment variables for secure API key management
├── .gitignore                 # Files and directories to ignore by Git
├── requirements.txt           # Project dependencies
└── README.md                  # Documentation for the project
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd neuroscribe-pdf-copilot
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key:
   - Create a `.env` file in the root directory and add your API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

## Usage

To run the application, execute the following command:
```
streamlit run src/app.py
```

Open your web browser and navigate to `http://localhost:8501` to access the NeuroScribe PDF Copilot application.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.