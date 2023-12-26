import speech_recognition as sr
from language import LANGUAGES_TRANSLATE, LANGUAGES_GTTS
from googletrans import Translator
from gtts import gTTS
import pygame
import os


class TextOperation():

    def __init__(self, lang: str | None) -> None:
        self.lang = lang.lower()

    def translate(self, text: str) -> str:
        translator = Translator()
        translation = translator.translate(
            text=text, dest=LANGUAGES_TRANSLATE[self.lang])
        return translation.text

    def text2speech(self, text: str) -> None:
        myobj = gTTS(text=text, lang=LANGUAGES_GTTS[self.lang], slow=False)
        myobj.save('result.mp3')

    def playAudio(self, file: str) -> None:
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
        os.remove(os.path.join('./result.mp3'))


class SpeechOperation(TextOperation):

    def __init__(self, lang: str | None) -> None:
        super().__init__(lang)
        self.lang = lang.lower()

    def spech2text(self) -> str:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('listening......')
            r.pause_threshold = 1
            audio = r.listen(source=source)
            try:
                print('recognizing......')
                query = r.recognize_google(audio, language='en-in')
                return query
            except Exception as e:
                print(e)
                return 'sorry we cannot understand'
            
    def audio2text(self,file:str)->str:
        r=sr.Recognizer()
        source=sr.AudioFile(file)
        with source as s:
            audio=r.record(source=s)
            try:
                print('recognizing......')
                query = r.recognize_google(audio, language='en-in')
                return query
            except Exception as e:
                print(e)
                return 'sorry we cannot understand'


class Operation():

    def __init__(self) -> None:
        self.txt = ''
        self.lang = ''

    def startOperation(self) -> None:
        choice = int(input('ENTER EITHER YOU WANT TO WRITE(0) OR SPEAK(1): '))
        self.lang = input('ENTER THE LANGUAGE TO OPERATE: ')
        if (choice):
            s2t = SpeechOperation(lang=self.lang)
            self.txt = s2t.spech2text()
        else:
            self.txt = input('ENTER YOUR TEXT: ')

    def operation(self) -> None:
        t2s = TextOperation(lang=self.lang)
        txt = t2s.translate(text=self.txt)
        t2s.text2speech(text=txt)
        t2s.playAudio(file=os.path.join('./result.mp3'))




# if __name__ == '__main__':
    
#     opt = Operation()
#     while True:
#         opt.startOperation()
#         opt.operation()
#         choice = int(input('ENTER 1 FOR CONTINUE OR 0 FOR END: '))
#         if (not choice):
#             break