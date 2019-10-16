



import socket
from threading import Thread
from time import sleep, time
import code as pycode
import audioop

import pyaudio
import keyboard

from _reads import *
from _cont_fl import *



pyaud = pyaudio.PyAudio()

audio_format = pyaudio.paInt16
audio_quality = 44100
frames_per_buffer = 2048



def start_client(name, ip, port):
	Running = Bucket(1)

	hotkey_to_mute = read_str('client-hotkey-to-mute.txt')
	hotkey_to_unmute = read_str('client-hotkey-to-unmute.txt')

	s = socket.socket()
	print(f'connecting to: {name}@{ip}#{port}')
	try:
		s.connect((ip, port))
	except TimeoutError:
		print('computer is on, but doesnt respond')
		return
	except KeyboardInterrupt:
		return
	except socket.gaierror:
		print('invalid ip')
		return

	thread_counter = Bucket(0)
	user_is_muted = Bucket(0)

	args = (Running, s)
	thr(play_recived_audio, args, thread_counter)
	thr(send_recorded_audio, args+(user_is_muted,), thread_counter)
	print('connected')


	def on_mute(muted):
		muted.new(1)
		print('muted')
	def on_unmute(muted):
		muted.new(0)
		print('unmuted')

	#hotkeys = []
	#hotkeys.append (keyboard.add_hotkey( hotkey_to_mute, lambda:on_mute(user_is_muted) ))
	#hotkeys.append (keyboard.add_hotkey( hotkey_to_unmute, lambda:on_unmute(user_is_muted) ))
	keyboard.add_hotkey( hotkey_to_mute, lambda:on_mute(user_is_muted) )
	keyboard.add_hotkey( hotkey_to_unmute, lambda:on_unmute(user_is_muted) )

	try:
		while Running:
			sleep(50)
	except KeyboardInterrupt:
		pass
	
	#for hotkey in hotkeys:
	#	keyboard.remove_hotkey(hotkey)
	keyboard.unhook_all_hotkeys()
	print('hotkeys fixed')


	stop_client(Running, s)

	wait_for_the_end(thread_counter)
	print('END')

	



def play_recived_audio(Running, s):
	stdouts = {}
	example_stdout = lambda:pyaud.open(
    format=audio_format,
    channels=1,
    rate=audio_quality,
    input=False,
    output=True,
    frames_per_buffer=frames_per_buffer
	)
	audio_samples_width_in_bytes = read_int('client-audio-samples-width-in-bytes.txt')

	play_volume = read_float('client-play-volume.txt')
	user_volumes = read_dict_float('client-user-volumes.txt')

	data = b''
	while Running:
		try:
			frame = s.recv(20)
		except ConnectionResetError:
			print('connection error')
			break
		except (ConnectionAbortedError,):
			print('aborted by user')
			break
		except OSError:
			print('aborted by user?')
			break

		data += frame

		if b';' in data:
			ind = data.index(b';')
			head = data[:ind].decode('utf-8')
			data = data[ind+1:]

			source, to_recv = head.split(',')
			to_recv = int(to_recv)

			if source in user_volumes:
				volume = play_volume * user_volumes[source]
			else:
				volume = play_volume
				print(f'unknown guy: {source}')
				user_volumes[source] = 1

			left = to_recv - len(data)
			while left > 0:
				try:
					frame = s.recv(left)
				except (ConnectionResetError, ConnectionAbortedError):
					if Running:
						print('connection error')
					break
				left -= len(frame)
				data += frame

			audio = data[:to_recv]
			
			audio = audioop.mul(audio, audio_samples_width_in_bytes, volume)
			if source in stdouts:
				stdout = stdouts[source]
			else:
				print(f'new audio channel for: {source}')
				stdout = example_stdout()
				stdouts[source] = stdout
				
			stdout.write(audio)

			data = data[to_recv:]

	stdout.stop_stream()
	stdout.close()

	stop_client(Running, s)

def send_recorded_audio(Running, s, muted):
	stdin = pyaud.open(
    format=audio_format,
    channels=1,
    rate=audio_quality,
    input=True,
    output=False,
    frames_per_buffer=frames_per_buffer
	)
	audio_samples_width_in_bytes = read_int('client-audio-samples-width-in-bytes.txt')
	record_volume = read_float('client-record-volume.txt')

	while Running:
		data = stdin.read(frames_per_buffer)
		if muted():
			data = audioop.mul(data, audio_samples_width_in_bytes, 0)
		else:
			data = audioop.mul(data, audio_samples_width_in_bytes, record_volume)

		try:
			s.sendall(data)
		except ConnectionResetError:
			print('server has shut down / is restarting')
			break
		except OSError:#manual shutdown
			break
	stdin.stop_stream()
	stdin.close()

	stop_client(Running, s)



def stop_client(Running, s):
	Running.new(0)
	s.close()





def thr(fnc, args=(), thread_counter=0):
	if thread_counter:
		thread_counter.increase()
		Thread( target=thread_wrapper, args=(fnc, args, thread_counter) ).start()
	else:
		Thread(target=fnc, args=args).start()

def thread_wrapper(fnc, args, thread_counter):
	try:
		fnc(*args)
	finally:
		thread_counter.decrease()




def wait_for_the_end(counter, delay=0.1):
	while counter():
		sleep(delay)