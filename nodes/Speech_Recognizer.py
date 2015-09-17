# -*- coding: utf-8 -*- 
#Author:Eleftherios Mylonakis
#!/usr/bin/env python


import alsaaudio, wave, numpy
import speech_recognition as sr
import time
import pyttsx
import os

	
def recorder(desired_time):
	inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, 'default')
	inp.setchannels(1)
	inp.setrate(44100)
	inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
	inp.setperiodsize(1024)
	
	w = wave.open('test.wav', 'wb')
	w.setnchannels(1)
	w.setsampwidth(2)
	w.setframerate(44100)
	
	starter=time.time()
	flag1=1
	flag_threshold=1
	while flag1:
		l, data = inp.read()
		a = numpy.fromstring(data, dtype='int16')
		if flag_threshold==1: #for background_noise
			threshold=numpy.abs(a).mean()
			print "The threshold is"
			print threshold
			flag_threshold=0
		print numpy.abs(a).mean()
		w.writeframes(data)
		if time.time()-starter>desired_time:
			flag1=0
	return threshold

def talking_machine(feedback):
	engine = pyttsx.init()
	engine.say(feedback)
	engine.runAndWait()                                 # speech is unintelligible
	
def recognizer_Eng_Us(threshold):
	r = sr.Recognizer()
	r.energy_threshold = threshold
	with sr.WavFile('test.wav') as source:              # use "test.wav" as the audio source
		audio = r.record(source)                        # extract audio data from the file
	try:
		phrase=r.recognize_google(audio, key = None, language = "en-US", show_all = False)
	except sr.UnknownValueError:
		phrase=("Google Speech Recognition could not understand audio")
		pass
	except sr.RequestError:
		phrase=("Could not request results from Google Speech Recognition service")
	except LookupError:
		phrase=("Could not understand audio")
		pass
	print("Transcription: " +phrase)   # recognize speech using Google Speech Recognition
	return phrase
	
def recognizer_Greek(threshold):
	r = sr.Recognizer()
	r.energy_threshold = threshold
	with sr.WavFile('test.wav') as source:              # use "test.wav" as the audio source
		audio = r.record(source)                        # extract audio data from the file
	try:
		phrase=r.recognize_google(audio, key = None, language = "el", show_all = False)
	except sr.UnknownValueError:
		phrase=("Google Speech Recognition could not understand audio")
		pass
	except sr.RequestError:
		phrase=("Could not request results from Google Speech Recognition service")
	except LookupError:
		phrase=("Could not understand audio")
		pass
	print("Transcription: " +phrase)   # recognize speech using Google Speech Recognition
	return phrase





i=0
while True:
	#~ desired_time=input("Give the time of your phrase in seconds! ")
	desired_time=6
	threshold=recorder(desired_time)
	phrase=recognizer_Eng_Us(threshold)
	if phrase=="Okay Google":
		talking_machine("Hello, boss")
		threshold=recorder(desired_time)
		phrase=recognizer_Greek(threshold)
		if phrase==(u'άναψε το θερμοσίφωνα'):
			i=1
		elif phrase==(u'κλείσε το θερμοσίφωνα'):
			i=0			
	print i
	#~ time.sleep(desired_time+2)
	


