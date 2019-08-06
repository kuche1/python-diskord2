



def read_lst(fd, sep='\n'):
	f = open(fd)
	cont = f.read()
	f.close()

	cont = cont.split(sep)
	while '' in cont:
		cont.remove('')

	return cont


def read_int(fd):
	with open(fd, 'rb') as f:
		cont = f.readline()
		if b'#' in cont:
			cont = cont[:cont.index(b'#')]
		return int( cont )

def read_str(fd):
	with open(fd) as f:
		return f.read()


def read_float(fd):
	with open(fd, 'rb') as f:
		cont = f.readline()
		if b'#' in cont:
			cont = cont[:cont.index(b'#')]
		try:
			return float( cont )
		except ValueError:
			raise Exception(f'bad float: {fd}')

def read_bool(fd):
	f = open(fd)
	cont = f.read(2)

	if cont == 'no':
		f.close()
		return 0
	cont += f.read(1)
	f.close()

	if cont == 'yes':
		return 1

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
			try:
				dic[name] = float(value)
			except ValueError:
				raise Exception(f'bad float in dict file: {fd}')
	return dic


def read_addr(fd):
	cont = read_str(fd)
	if cont.count('\n') == 0:

		if '#' in cont:
			ind = cont.index('#')
			name = cont[ind+1:]
			cont = cont[:ind]

			if ':' in cont:
				ind = cont.index(':')
				
				ip = cont[:ind]
				port = cont[ind+1:]
				try:
					port = int(port)
				except ValueError:
					print(f'bad port (not a number) in file {fd}-> {port}')
				else:
					return name, ip, port



			else:
				print('no port')

		else:
			print('no hashtag')

	else:
		print('no new lines')



	raise Exception(f'Addr file corrupt: {fd}')


