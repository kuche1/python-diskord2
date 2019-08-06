



def read_lst(fd):
	f = open(fd)
	cont = f.read()
	f.close()

	cont = cont.split('\n')
	while '' in cont:
		cont.remove('')

	return cont


def read_int(fd):
	with open(fd, 'rb') as f:
		return int( f.read() )

def read_str(fd):
	f = open(fd, 'rb')
	cont = f.read()
	f.close()
	return cont.decode('utf-8')


def read_float(fd):
	with open(fd, 'rb') as f:
		return float(f.read())

def read_bool(fd):
	data = read_str(fd)
	if data == 'yes':
		return 1
	elif data == 'no':
		return 0
	else:
		raise Exception(f'Bool file corrupt: {fd}')


def read_dict_float(fd):
	dic = {}
	for item in read_str(fd).split('\n'):
		if '=' in item:
			ind = item.index('=')
			name = item[:ind]
			value = item[ind+1:]
			if '#' in value:
				ind = value.index('#')
				value = value[:ind]
			dic[name] = float(value)
	return dic


def read_addr(fd):
	cont = read_str(fd)
	if cont.count('\n') == 0:

		if '#' in cont:
			ind = cont.index('#')
			name = cont[ind+1:]
			cont = cont[:ind]
			print(f'name:{name}')

			if ':' in cont:
				ind = cont.index(':')
				
				ip = cont[:ind]
				port = cont[ind+1:]
				try:
					port = int(port)
				except ValueError:
					print(f'bad port (not a number)->{port}')
				else:
					return name, ip, port



			else:
				print('no port')

		else:
			print('no hashtag')

	else:
		print('no new lines')



	raise Exception(f'Addr file corrupt: {fd}')