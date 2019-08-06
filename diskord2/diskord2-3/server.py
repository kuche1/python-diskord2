


from time import sleep
import socket
from threading import Thread

from _reads import *



frame_delay = 0
frame_repeat = 1
reciving_no_more_than = 1024 * 10






def start_server():
	global Running
	Running = 1

	s_port = read_int('server-port.txt')
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

	participators = read_lst('server-participators.txt')

	thr(save_new_connections, (participators,))

	thr(redirect_recived_data)

	try:
		while 1:
			sleep(50)
	except KeyboardInterrupt:
		pass

	stop_server()



def send(con, data):
	try:
		con.sendall(data)
	except (ConnectionAbortedError, ConnectionResetError):
		pass


def redirect_recived_data():
	bad_cons = []
	while Running:
		for _ in range(frame_repeat):

			ind = 0
			while ind < len(cons):
				con = cons[ind]
				ip = ips[ind]
				try:
					data = con.recv(reciving_no_more_than)
				except BlockingIOError:
					pass
				except (ConnectionAbortedError, ConnectionResetError):
					print(f'deleting: {ip}')
					del cons[ind]
					del ips[ind]
					continue
				else:

					header = f'{ip},{ len(data) };'.encode('utf-8')
					data = header + data
					for reciver in cons:
						if reciver != con:#ne raboti???
							#thr(send, (reciver, data))
							send(reciver, data)
				ind += 1

		sleep(frame_delay)



def save_new_connections(participators):
	while Running:
		try:
			con, (ip, port) = s.accept()
		except OSError:
			break

		if ip in participators:
			print(f'new connection: {ip}')
			cons.append(con)
			ips.append(ip)
		else:
			print(f'uninvited user: {ip}')
			con.close()

		sleep(0.5)




def stop_server():
	global Running

	Running = 0
	s.close()


def thr(fnc, args=()):
	Thread(target=fnc, args=args).start()











cons = []
ips = []
start_server()