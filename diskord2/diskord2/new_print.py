






class New_print:
	def __init__(s):
		s.waitlist = []
	def __call__(s, *args):
		s.waitlist.append(args)

	def flush(s):
		while s.waitlist:
			args = s.waitlist.pop(0)
			print(*args)
