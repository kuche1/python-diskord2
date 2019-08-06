



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

