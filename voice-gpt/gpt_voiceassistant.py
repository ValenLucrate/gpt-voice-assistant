import openai
import pyttsx3
import speech_recognition as sr
import threading

openai.api_key = "your-api-key"

def transcribe_audio_to_text(audio, recognizer):
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand the audio"
    except sr.RequestError as e:
        return "Could not request results from Google Speech Recognition service; {0}".format(e)

def generate_response(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    if response.choices:
        return response.choices[0].text
    else:
        return "Sorry, I don't know the answer to that."

def speak_text(text, engine):
    engine.setProperty('rate', 170)
    engine.setProperty('pitch', 50)  # adjust pitch
    engine.say(text)
    engine.runAndWait()

def speech_to_text(recognizer, engine):
    while True:
        print("Say 'Jarvis' to start recording your question...")
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            transcription = transcribe_audio_to_text(audio, recognizer)
            if "jarvis" in transcription.lower():
                #record audio
                print("Say your question...")
                audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                text = transcribe_audio_to_text(audio, recognizer)
                if text:
                    print(f"You: {text}")
                    #response
                    prompt = f"Q: {text}\nA:"
                    response = generate_response(prompt)
                    print(f"GPT-3: {response}")
                    speak_text(response, engine)
                    #ask user if there is anything else they need help with
                    print("Is there anything else I can help you with?")
                    audio = recognizer.listen(source, phrase_time_limit=15, timeout=15)
                    transcription = transcribe_audio_to_text(audio, recognizer)
                    if not transcription:
                        break
                    elif "no" in transcription.lower() or "disconnect" in transcription.lower():
                        speak_text("Goodbye!", engine)
                        return

def main():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 500
    engine = pyttsx3.init()
    speech_to_text(recognizer, engine)

if __name__ == "__main__":
    main()
