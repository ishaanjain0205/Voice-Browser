# voiceBrowser

## Voice-Controlled Chrome Browser

This project enables you to control your chrome browser with your voice. Using Python, Hugging Face Sentence-Transformers, Vosk, Selenium, and PyAudio, the application takes in your spoken commands and executes them on a chrome browser. It leverages NLP-driven command recognition to extract and execute user voice commands, using real-time speech-to-text conversion and web automation. More specifically, this project uses a zero-shot-classification trained on the facebook/bart-large-mnli model and paraphrase-MiniLM-L6-v2.


## Features

- **Natural Language Processing (NLP):** Implemented command recognition and target extraction using Hugging Face's Sentence-Transformers (models: `paraphrase-MiniLM-L6-v2`, `all-MiniLM-L6-v2`).
- **Zero-Shot Classification:** Utilizes a zero-shot classification model to accurately recognize and execute user commands without predefined categories.
- **Speech-to-Text Conversion:** Integrated **Vosk** and **PyAudio** to handle real-time voice commands and convert them to text.
- **Browser Automation:** Uses **Selenium** to automate dynamic web commands, enabling voice-driven control over a Chrome browser.

## Best Way to Operate
It is a tool to control your browser just as your clicks would. You cannot say things such as open Netflix. 
Try using commands like:
- search up how to code or look up how to code
- go back a tab
- go to the next tab
- scroll down a little
- scroll up more
- open a brand new tab
- close this tab
- go back a page
- go to the next page
- click on wikipedia (if your link clink does not work on the first try, say the clickable link part and the small title above the link as well)
<img width="620" alt="Screenshot 2024-09-08 at 1 20 27 PM" src="https://github.com/user-attachments/assets/844aa934-b937-4440-b632-90ecc98eb66a">

For this example, say "click on YouTube apps on Google Play" and "google play".


Keep an eye on the terminal to see when to speak and what the application understood. 

## Installation

Follow the steps below to set up the project and install the necessary dependencies.

### 1. Clone the repository

```bash
git clone https://github.com/your-username/voiceBrowser.git
cd voiceBrowser
```
### 2. Create a virtual enviornment

#### For Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### For Windows
###### Full functionality may not be supported on windows
``` bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install neccessary dependencies
#### Once your virtual environment is activated, install the project dependencies from the requirements.txt file:
```bash
pip install -r requirements.txt
```

### 4. Run the project
#### First attempt to run the project may take a few minutes
```bash
python main.py
```


## Requirements
This project requires Python and the following libraries (installed automatically via requirements.txt):

Hugging Face Transformers
Vosk
PyAudio
Selenium
Scikit-learn
Torch
See the full list of dependencies in the requirements.txt file.

## License
This project is licensed under the MIT License.

