
import socket
from threading import Thread
from time import time, sleep

from cont_fl import *


def thr(fnc, args=()):
	Thread(target=fnc, args=args).start()



class Phone:
	def __init__(s, ip, port, listen):
		s.ip = ip
		s.port = port
		s.listen = listen

	def turn_on(s, ):
		s.on = 1

		s.sock = socket.socket()
		s.sock.bind((s.ip, s.port))
		s.sock.listen(s.listen)

		s.new_connections = []
		thr( s.save_new_connections_data )


	def main_menu(s):
		while s.on:

			s.display_new_calls()

			print(1)
			s.make_a_call()
			print(2)


















	



	def make_a_call(s):
		try:
			c = inp('============\nMake a call; BREAK', 
				'someone who is calling', 
				'someone who is not calling',
				'exit')
		except KeyboardInterrupt:
			return

		if c == 1:
			choices = []
			for time, (con, addr) in enumerate(s.new_connections):
				choices.append(f'{time}: {addr}')

			try:
				c = inp('Choose a caller', *choices)
			except KeyboardInterrupt:
				return
			s.answer_requested_call(s.new_connections[c-1])

		elif c == 2:
			s.speak_with_someone()

		elif c == 3:
			s.turn_off()





	def answer_requested_call(s, con_data):
		time, (con,addr) = con_data
		temp = con.recv(1)
		if temp != b'0':
			print('')
			raise




	refresh_new_connections_delay = 0.5
	def display_new_calls(s):
		try:
			print('displaying call requests; BREAK to skip')
			last_len = 0
			while s.on:
				le = len(s.new_connections)
				if le != last_len:
					print('===========')
					print('call requests:')
					for time, (con, addr) in enumerate(s.new_connections):
						print(f'{time}: {addr}')
					last_len = le
				sleep(s.refresh_new_connections_delay)
		except KeyboardInterrupt:
			pass


	def turn_off(s):
		s.on = 0
		s.sock.close()





	def save_new_connections_data(s):
		while s.on:
			try:
				data = s.sock.accept()
			except OSError:
				break

			s.new_connections.append( time(), data)

