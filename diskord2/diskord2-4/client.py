


from _reads import *

from _client import start_client



#ip = read_str('client-ip.txt')
#port = read_int('client-port.txt')


def main_menu():
	if read_bool('client/auto-connect-on-startup.txt'):
		server_addr = read_addr('client/auto-connect-to.txt')
		start_client(*server_addr)
		del server_addr

	last_err = ''
	while 1:
		print('==========')

		print('Choose a server')
		servers = load_servers()
		if len(servers) == 0:
			input('no servers found, press enter to refresh')
			continue

		for ind, (name, ip, port) in enumerate(servers):
			print(f'{ind}/ {name} -> {ip}#{port}')

		c = input('>')
		
		if c.lower() == 'quit':
			return
		try:
			c = int(c)
		except ValueError:
			print('choice must be an integer')
			continue

		if c < 0:
			print('choice too low')
			continue

		if c >= len(servers):
			print('choice too high')
			continue

		server_data = servers[c]
		start_client(*server_data)


def start_main_menu():
	try:
		main_menu()
	except KeyboardInterrupt:
		print('QUIT')



def load_servers():
	ser = read_str('client/servers.txt')
	ser = ser.split('\n')

	while '' in ser:
		ser.remove('')

	servers = []
	for ser in ser:
		if '#' in ser:
			ind =  ser.index('#')
			name = ser[ind+1:]
			ser = ser[:ind]

			if ':' in ser:
				ind = ser.index(':')
				port = int(ser[ind+1:])
				ip = ser[:ind]

				servers.append((name, ip, port))

	return servers



if __name__ == '__main__':
	start_main_menu()