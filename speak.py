import pygame
from os.path import exists, dirname,join
import os,sys
from gtts import gTTS
from pygame.locals import *
import requests

script_dir = dirname(__file__)
target_dir = join(script_dir, '../sounds')

class Speak:
    def __init__(self, phrase: list):
        self.phrase = phrase

        if not exists(target_dir):
            os.mkdir(target_dir)

        if exists(target_dir):        
            for word in self.phrase:
                mp3_path = join(target_dir, f'{self.phrase}.mp3')
                if not exists(mp3_path) and self.has_internet_connection():
                    try:
                        tts = gTTS(text=word, lang='en')
                        tts.save(mp3_path)
                    except Exception as e:
                        pass

    def has_internet_connection(self) -> bool:
        """
        Function to check internet connectivity.
        :return: True if internet is available, False otherwise
        """
        try:
            requests.get("http://www.google.com", timeout=5)
            return True
        except requests.ConnectionError as e:
            return False
        
    def play_mp3(self,word) -> None:
        """
        Function to play the saved mp3 file that matches the word
        :param word: the word that wants to be played
        """
        try:
            if word != "":
                pygame.mixer.pre_init(13000, -16, 2, 2048) # setup mixer to avoid sound lag
                pygame.init()
                pygame.mixer.init()
                script_dir = dirname(__file__)
                mp3_path = join(script_dir, '../sounds', f'{word}.mp3')
                pygame.mixer.music.load(mp3_path)
                pygame.mixer.music.play()
                return
        except Exception as e:  
            return
