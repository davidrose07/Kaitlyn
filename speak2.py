import pyttsx3

def list_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for index, voice in enumerate(voices):
        all_voices.append(index)
        print(f"Voice {index}: ID: {voice.id} | Name: {voice.name} | Languages: {voice.languages}")

def set_voice(index):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if index < len(voices):
        engine.setProperty('voice', voices[index].id)
        print(f"Selected voice: {voices[index].name}")
    else:
        print("Voice index out of range.")

def speak_text(text, num):
    # Initialize the TTS engine
    engine = pyttsx3.init()
    voices =engine.getProperty('voices')

    # Optional: Set properties like voice, speech rate, and volume
    engine.setProperty('rate', 190)  # Speed percent (can be adjusted to suit your preferences)
    engine.setProperty('volume', 0.9)  # Volume 0-1
    engine.setProperty('voice', voices[num].id)

    # Speaking the text
    engine.say(text)

    # Block while processing all the currently queued commands
    engine.runAndWait()

# List available voices
list_voices()

# Example: Set to the first voice in the list
for voices in all_voices:
    print(f'voices in all_voices: {voices}')
    #set_voice(voices)
    speak_text("Hello, is this working?", voices)
