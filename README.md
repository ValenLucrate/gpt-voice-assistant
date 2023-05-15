# GPT-3 Voice Assistant

## Description
The GPT-3 Voice Assistant is an application that allows users to interact with OpenAI's GPT-3 language model(text-davinci-003) using voice commands. Users can ask the application questions or provide prompts, and the model will generate responses in natural language.

## Requirements
To run the GPT-3 Voice Assistant, you will need to have the following dependencies installed on your system:
- Python 3.x
- Pyttsx3
- SpeechRecognition
- OpenAI API key

## Installation
To install the required packages, run the following command in your terminal:

pip install pyttsx3 SpeechRecognition openai

You will also need to set your OpenAI API key as an environment variable by putting your openai api key inside openai.api_key = "your-api-key"
You can get your openai api key from here:
https://platform.openai.com/account/api-keys

## Usage
To start the GPT-3 Voice Assistant, run the following command in your terminal:
The application will prompt you to say "Voxi" to start recording your question. Once you provide a prompt, the model will generate a response and speak it aloud. The assistant will then ask if there's anything else you need help with, and will continue to listen for additional prompts until you say "no" or "disconnect".(In state of fixing the code for that atm..)

## License
This project is licensed under the MIT License. See the LICENSE file for details.
