



import socket
from threading import Thread
from time import sleep, time
import code as pycode

import pyaudio
import keyboard

from _reads import *
from _cont_fl import *

from _client_send_recorded_audio import send_recorded_audio
from _client_play_recived_audio import play_recived_audio



def start_client(name, ip, port):
	Running = Bucket(1)

	hotkey_to_mute = read_str('client/hotkey-to-mute.txt')
	hotkey_to_unmute = read_str('client/hotkey-to-unmute.txt')

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


	keyboard.add_hotkey( hotkey_to_mute, lambda:on_mute(user_is_muted) )
	keyboard.add_hotkey( hotkey_to_unmute, lambda:on_unmute(user_is_muted) )

	try:
		while Running():
			sleep(1)
	except KeyboardInterrupt:
		pass

	keyboard.unhook_all_hotkeys()


	Running.new(0)
	s.close()

	wait_for_the_end(thread_counter)
	print('END')



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