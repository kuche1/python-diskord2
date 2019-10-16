


from _reads import *

from _client import start_client



#ip = read_str('client-ip.txt')
#port = read_int('client-port.txt')


def main_menu():
	if read_bool('client-auto-connect-on-startup.txt'):
		server_addr = read_addr('client-auto-connect-to.txt')
		start_client(*server_addr)



	last_err = ''
	while 1:
		print('==========')
		if last_err:
			print(last_err)

		print('Choose a server')
		servers = load_servers()
		if len(servers) == 0:
			last_err = 'refreshing servers'
			input('no servers found, press enter to refresh')
			continue

		for ind, (name, ip, port) in enumerate(servers):
			print(f'{ind}/ {name} -> {ip}#{port}')

		if len(servers) == 1:
			print('Only one server found, connecting')
			start_client(*servers[0])
			continue

		c = input('>')
		
		if c.lower() == 'quit':
			return
		try:
			c = int(c)
		except ValueError:
			last_err = 'choice must be an integer'
			continue

		if c < 0:
			last_err = 'choice too low'
			continue

		if c >= len(servers):
			last_err = 'choice too high'
			continue

		server_data = servers[c]
		start_client(*server_data)


def start_main_menu():
	try:
		main_menu()
	except KeyboardInterrupt:
		print('QUIT')



def load_servers():
	ser = read_str('client_servers.txt')
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