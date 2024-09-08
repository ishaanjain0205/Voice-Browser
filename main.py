# integration.py
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

# audio handling
from vosk import Model, KaldiRecognizer
import pyaudio
import json

# selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By  

# files
from back_end_functions import compute_action, proccess_command


#start web driver 
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-popup-blocking")  # Disable popup blocking
driver = webdriver.Chrome(options = options)
driver.get("https://www.google.com")

# declare models
#valhalla/distilbart-mnli-12-3 
#facebook/bart-large-mnli
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
click_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

actions = ["scroll up", "up", "scroll down", "down", "search", "search up", "look", "click", "click on", "open tab", "close tab", "next tab", "forward tab", "previous tab", "last tab", "pause video", "play video", "go back", "last page", "next page", "next", "refresh"]

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=0)
text_based_actions = ["search", "click", "other"]

# initialize vosk speech recognition model and recognizer
voskModel = Model("vosk-model-small-en-us-0.15")
voskRecognizer = KaldiRecognizer(voskModel, 16000)

# initialize device mic
mic = pyaudio.PyAudio() 

# start stream
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()
print("Stream started")

# loop to feed audio and recognize data 
while True: 

    # read the stream
    try:
        voiceData = stream.read(8192)
        print("reading stream")
    except:
        print("ERROR READING STREAM")
        continue
    else:
        if voskRecognizer.AcceptWaveform(voiceData):
            recognizedText = voskRecognizer.Result()

            # exctract acutal text from json file
            json_string = json.loads(recognizedText)
            recognizedText = json_string['text']

            
            # output recognized
            print("RECOGNIZED: " + recognizedText)

            stream.stop_stream()

            # stop listening command
            if recognizedText == "stop listening":
                driver.quit()
                break

            # calculating and 
            if recognizedText != "":
                command = compute_action(recognizedText, actions, text_based_actions, model, classifier)
                print("CALCUALTED: " + command)
                proccess_command(command, recognizedText, driver, model, classifier, click_model)
            else:
                command = "error"
                print("NO AUDIO DETECTED")


            stream.start_stream()

            
            
    
