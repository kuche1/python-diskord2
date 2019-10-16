


def put(text):
	print(text,end='')


def INP(text=''):
	return input(f'{text}> ')

def inp(title='', *opts):
	print(title)
	for ind,opt in enumerate(opts):
		print(f'{ind+1}/ {opt}')

	while 1:
		c = INP()
		try:
			int_c = int(c)
		except ValueError:
			put(f'not a number')
		else:
			c = int_c
			if c < 1:
				put(f'too low')
			elif c > len(opts):
				put(f'too high')
			else:
				return c
		print(f": {c}")
		

def inp_fnc(title,*args):
	args = list(args)
	texts = []
	fncs = []
	while args:
		texts.append(args.pop(0))
		fncs.append(args.pop(0))
		
	c = inp(title, *texts)
	return fncs[c-1]
