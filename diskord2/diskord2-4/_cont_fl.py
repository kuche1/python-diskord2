


class Bucket:
	def __init__(s, val=0):
		s.new(val)
	def __call__(s):
		return s.value
	def new(s, val):
		s.value = val

	def increase(s, val=1):
		s.value += val
	def decrease(s, val=1):
		s.value -= val


