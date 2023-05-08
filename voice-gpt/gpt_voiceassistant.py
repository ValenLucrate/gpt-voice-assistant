import openai 
import pyttsx3
import speech_recognition as sr
import threading
import time

openai.api_key = "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"
engine = pyttsx3.init()

recognizer = sr.Recognizer()
recognizer.energy_threshold = 500

def transcribe_audio_to_text(audio):
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand the audio"
    except sr.RequestError as e:
        return "Could not request results from Google Speech Recognition service; {0}".format(e)

def generate_response(prompt):
    response = openai.Completion.create(
        engine = 'text-davinci-003',
        prompt = prompt,
        max_tokens = 4000,
        n = 1,
        stop = None,
        temperature = 0.5,
    )
    if response.choices:
        return response.choices[0].text
    else:
        return "Sorry, I don't know the answer to that."

def speak_text(text):
    engine.setProperty('rate', 170)
    engine.setProperty('pitch', 50)  # adjust pitch
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    while True:
        print("Say 'Voxi' to start recording your question...")
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            transcription = transcribe_audio_to_text(audio)
            if "voxi" in transcription.lower():
                #record audio
                print("Say your question...")
                audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                text = transcribe_audio_to_text(audio)
                if text:
                    print(f"You: {text}")
                    #response
                    prompt = f"Q: {text}\nA:"
                    response = generate_response(prompt)
                    print(f"GPT-3: {response}")
                    speak_text(response)
                    #ask user if there is anything else they need help with
                    while True:
                        print("Is there anything else I can help you with?")
                        audio = recognizer.listen(source, phrase_time_limit=15, timeout=15)
                        transcription = transcribe_audio_to_text(audio)
                        if not transcription:
                            print("Sorry, I didn't catch that. Please try again.")
                            continue
                        elif "no" in transcription.lower() or "disconnect" in transcription.lower():
                            print("Thank you for using. Goodbye!")
                            return
                        elif "genius" in transcription.lower():
                            print("Please wait for the current question to finish.")
                            continue
                        else:
                            break

def main():
    try:
        stt_thread = threading.Thread(target=speech_to_text)
        stt_thread.start()
        stt_thread.join()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        recognizer.stop_listening()

if __name__ == "__main__":
    main()
