
import os 
from gtts import gtts


def iTTS(string):


	language = 'pt-br'

	mytext = string


	myobj = gTTS(text = mytext, lang = language, slow = False)



	myobj.save("welcome.mp3")
	os.system("mpg321 welcome.mp3")