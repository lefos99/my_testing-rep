#Author:Eleftherios Mylonakis
#!/usr/bin/env python

import alsaaudio, wave, numpy
import speech_recognition as sr
import time
import pyttsx
import os

flag2=1
while True:
	inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, 'default')
	inp.setchannels(1)
	inp.setrate(44100)
	inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
	inp.setperiodsize(1024)
	
	w = wave.open('test.wav', 'wb')
	w.setnchannels(1)
	w.setsampwidth(2)
	w.setframerate(44100)
	
	desired_time=input("Give the time of your phrase in seconds! ")
	#~ desired_time=4
	starter=time.time()
	flag1=1
	while flag1:
		l, data = inp.read()
		a = numpy.fromstring(data, dtype='int16')
		if flag2==1:
			threshold=numpy.abs(a).mean()
			print "The threshold is"
			print threshold
			flag2=0
		print numpy.abs(a).mean()
		w.writeframes(data)
		if time.time()-starter>desired_time:
			flag1=0
	r = sr.Recognizer()
	r.energy_threshold = threshold
	engine = pyttsx.init()
	with sr.WavFile('test.wav') as source:              # use "test.wav" as the audio source
		audio = r.record(source)                        # extract audio data from the file
	try:
		#~ engine.say("I think you said " +r.recognize(audio))
		print r.recognize(audio)
		engine.runAndWait()
		print("Transcription: " + r.recognize(audio))   # recognize speech using Google Speech Recognition
	except LookupError:
		#~ engine.say("Sorry, i couldn't underastand what you said")
		engine.runAndWait()                                 # speech is unintelligible
		print("Could not understand audio")
	time.sleep(desired_time+2)

