


from time import sleep
import socket
from threading import Thread
from code import interact as pyinteract

from _cont_fl import *
from _reads import *



recive_delay = 0.001
reciving_no_more_than = 1024 * 10

send_delay = 0.001






def start_server():
	Running = Bucket(1)

	s_port = read_int('server/port.txt')
	print(f'starting on port: {s_port}')

	global s
	s = socket.socket()
	try:
		s.bind(('', s_port))
	except OSError:
		print('port taken')
		return
	s.listen(1)
	print('ready')


	unsent_messages = {}

	thr(save_new_connections, (Running, unsent_messages,) )
	thr(send_recived_data, (Running, unsent_messages,) )

	try:
		while Running():
			sleep(1)
	except KeyboardInterrupt:
		pass

	stop_server(Running)


def send_recived_data(Running, send_stack):
	while Running():
		bad_cons = []
		for con in send_stack:

			to_send_list = send_stack[con]	
				
			if to_send_list:
				to_send = to_send_list.pop(0)

				for reciver in send_stack:
					if reciver != con:
						try:
							reciver.sendall(to_send)
						except OSError:
							bad_cons.append(reciver)
						except ConnectionResetError:
							pass#wait for the oserror

				if bad_cons:
					while bad_cons:
						bad_con = bad_cons.pop()
						del send_stack[bad_con]
						#print('deleting 2')
					break

		sleep(send_delay)




def save_recived_data(Running, con, ip, send_stack):
	try:

		#pyinteract(local=locals())

		data = b''
		while Running():
			try:
				frame = con.recv(5)
			except (ConnectionAbortedError, ConnectionResetError):
				print(f'deleting: {ip}')
				return
			data += frame

			while b';' in data:
				ind = data.index(b';')
				try:
					to_recive = int(data[:ind])
				except ValueError:
					print('hackerman: {ip}')
					return
				data = data[ind+1:]

				while len(data) < to_recive:
					try:
						frame = con.recv(reciving_no_more_than)
					except (ConnectionAbortedError, ConnectionResetError):
						print(f'deleting: {ip}')
						return
					data += frame

				header = f'{ip},{to_recive};'.encode('utf-8')
				send_stack[con].append( header+data[:to_recive] )

				data = data[to_recive:]



	finally:
		con.close()



def save_new_connections(Running, send_stack):
	participators = read_lst('server/participators.txt')
	while Running():
		try:
			con, (ip, port) = s.accept()
		except OSError:
			break

		if ip in participators:
			print(f'new connection: {ip}')
			send_stack[con] = []
			thr(save_recived_data, (Running, con, ip, send_stack) )
		else:
			print(f'uninvited user: {ip}')
			con.close()

		sleep(0.5)




def stop_server(Running):
	Running.new(0)
	s.close()

def thr(fnc, args=()):
	Thread(target=fnc, args=args).start()








if __name__ == '__main__':
	start_server()