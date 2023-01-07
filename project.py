import speech_recognition  # распознавание речи
import pyttsx3  # речевой синтезатор
import wikipediaapi  # гугл в вики
import webbrowser  # работа с использованием браузера 
import os  # работа с файловой системой

class VoiceAssistant:
    name = ""
    sex = ""
    speech_language = ""
    recognition_language = ""

def setup_assistant_voice():
    voices = ttsEngine.getProperty("voices")
    assistant.speech_language == "en"
    assistant.recognition_language = "en-US"
    assistant.sex == "female"
    ttsEngine.setProperty("voice", voices[1].id)
        
def record_and_recognize_audio(*args: tuple):
   
    with microphone:
        recognized_data = ""
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            print("Listening...")
            audio = recognizer.listen(microphone, 5, 5)

            with open("microphone-results.wav", "wb") as file:
                file.write(audio.get_wav_data())

        except speech_recognition.WaitTimeoutError:
            play_voice_assistant_speech("Can you check if your microphone is on, please?")
            return
        try:
            print("One moment...")
            recognized_data = recognizer.recognize_google(audio, language=assistant.recognition_language).lower()

        except speech_recognition.UnknownValueError:
            pass  

        return recognized_data

def play_voice_assistant_speech(text_to_speech):
    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()

def play_greetings(*args: tuple):
    greetings = [
        ("Hello, {}! "),
    ]
    play_voice_assistant_speech(greetings)

def play_farewell_and_quit(*args: tuple):
    farewells = [
        ("See you soon, {}!")
    ]
    play_voice_assistant_speech(farewells)
    ttsEngine.stop()
    quit()

def search_for_term_on_google(*args: tuple):
    if not args[0]: return
    search_term = " ".join(args[0])

    url = "https://google.com/search?q=" + search_term
    webbrowser.get().open(url)

    search_results = []
    try:
        for _ in search(search_term,  # что мы ищем
                        tld="com",  # домен
                        lang=assistant.speech_language,  # язык
                        num=1,  # сколько результатов на странице
                        start=0,  # индекс первого результата
                        stop=1,  # индекс последнего результата
                        pause=1.0,  # задержка между запросами
                        ):
            search_results.append(_)
            webbrowser.get().open(_)

    except:
        play_voice_assistant_speech("Seems like we have a trouble")
        return

    print(search_results)
    play_voice_assistant_speech(("Here is what I found for {}").format(search_term))

def search_for_video_on_youtube(*args: tuple):
    if not args[0]: return
    search_term = " ".join(args[0])
    url = "https://www.youtube.com/results?search_query=" + search_term
    webbrowser.get().open(url)
    play_voice_assistant_speech(("Here is what I found for {}").format(search_term))

def search_for_definition_on_wikipedia(*args: tuple):
    if not args[0]: return
    search_term = " ".join(args[0])
    wiki = wikipediaapi.Wikipedia(assistant.speech_language) #установка языка

    wiki_page = wiki.page(search_term)
    try:
        if wiki_page.exists():
            play_voice_assistant_speech(("Here is what I found for {} ").format(search_term))
            webbrowser.get().open(wiki_page.fullurl)
        else:
            play_voice_assistant_speech(("Sorry? but I'm sorry but I didn't find anything for {} ").format(search_term))
    except:
        play_voice_assistant_speech("Seems like we have a trouble")
        return

def execute_command_with_name(command_name: str, *args: list): #Выполнение заданной пользователем команды
    for key in commands.keys():
        if command_name in key:
            commands[key](*args)
        else:
            pass  

commands = {
    ("hello", "hi"): play_greetings,
    ("goodbye", "exit", "stop"): play_farewell_and_quit,
    ("search", "google"): search_for_term_on_google,
    ("video", "youtube"): search_for_video_on_youtube,
    ("wikipedia"): search_for_definition_on_wikipedia,
}

if __name__ == "__main__":

    #инструменты распознавания, ввода речи
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    #инструменты синтеза речи
    ttsEngine = pyttsx3.init()

   # указание на помощника помощника
    assistant = VoiceAssistant()

    # установка голоса по умолчанию
    setup_assistant_voice()


    while True:
        # старт записи речи с последующим выводом удалением записанного с микрофона
        voice_input = record_and_recognize_audio()
        os.remove("microphone-results.wav")
        print(voice_input)

        # отделение комманд от дополнительной информаци
        voice_input = voice_input.split(" ")
        command = voice_input[0]
        command_options = [str(input_part) for input_part in voice_input[1:len(voice_input)]]
        execute_command_with_name(command, command_options)