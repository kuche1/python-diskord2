



import socket
from threading import Thread
from time import sleep, time
import code as pycode
import audioop

import pyaudio
import keyboard

from _reads import *


ip = read_str('client-ip.txt')
port = read_int('client-port.txt')

audio_format = pyaudio.paInt16
audio_quality = 44100
frames_per_buffer = 2048

audio_samples_width_in_bytes = read_int('client-audio-samples-width-in-bytes.txt')

play_volume = read_float('client-play-volume.txt')
record_volume = read_float('client-record-volume.txt')

hotkey_to_mute = read_str('client-hotkey-to-mute.txt')
hotkey_to_unmute = read_str('client-hotkey-to-unmute.txt')





def start_client():
	global s
	global Running
	global muted

	Running = 1


	s = socket.socket()
	print('connecting')
	try:
		s.connect((ip, port))
	except TimeoutError:
		print('computer is on, but doesnt respond')
		return
	except KeyboardInterrupt:
		return
	
	thr(play_recived_audio)
	muted = 0
	thr(send_recorded_audio)
	print('connected')


	def on_mute():
		global muted
		muted = 1
		print('muted')
	def on_unmute():
		global muted
		muted = 0
		print('unmuted')

	
	keyboard.add_hotkey(hotkey_to_mute, on_mute)
	keyboard.add_hotkey(hotkey_to_unmute, on_unmute)

	try:
		while 1:
			sleep(50)
	except KeyboardInterrupt:
		stop_client()

	



def play_recived_audio():
	stdout = pyaud.open(
    format=audio_format,
    channels=1,
    rate=audio_quality,
    input=False,
    output=True,
    frames_per_buffer=frames_per_buffer
	)
	#pycode.interact(local=locals())
	while Running:
		try:
			data = s.recv(10240)
		except (ConnectionResetError, ConnectionAbortedError):
			if Running:
				print('connection error')
			break
		if ';' in data:
			ind = data.index(';')
			source = data[:ind]
			data = data[ind+1:]

			#data = audioop.bias(data, audio_samples_width_in_bytes, 1)
			data = audioop.mul(data, audio_samples_width_in_bytes, play_volume) #data, ?, volume
			stdout.write(data)
		else:
			print(f'; not in data')
	stdout.stop_stream()
	stdout.close()

def send_recorded_audio():
	stdin = pyaud.open(
    format=audio_format,
    channels=1,
    rate=audio_quality,
    input=True,
    output=False,
    frames_per_buffer=frames_per_buffer
	)
	while Running:
		data = stdin.read(frames_per_buffer)
		if muted:
			data = audioop.mul(data, audio_samples_width_in_bytes, 0)
		else:
			data = audioop.mul(data, audio_samples_width_in_bytes, record_volume)

		try:
			s.sendall(data)
		except ConnectionResetError:
			print('server has shut down / is restarting')
			break
		except OSError:
			pass
	stdin.stop_stream()
	stdin.close()




def stop_client():
	global Running

	Running = 0
	s.close()

def thr(fnc, args=()):
	Thread(target=fnc, args=args).start()



pyaud = pyaudio.PyAudio()
start_client()




