import audioop
import zlib

import pyaudio

from _reads import *


audio_format = pyaudio.paInt16
audio_quality = 44100
frames_per_buffer = 2048


pyaud = pyaudio.PyAudio()
def play_recived_audio(Running, s):
	stdouts = {}
	example_stdout = lambda:pyaud.open(
    format=audio_format,
    channels=1,
    rate=audio_quality,
    input=False,
    output=True,
    frames_per_buffer=frames_per_buffer
	)
	audio_samples_width_in_bytes = read_int('client/audio-samples-width-in-bytes.txt')

	play_volume = read_float('client/play-volume.txt')
	user_volumes = read_dict_float('client/user-volumes.txt')

	data = b''
	while Running():
		try:
			frame = s.recv(20)
		except ConnectionResetError:
			print('server closed 1')
			break
		except (ConnectionAbortedError,):
			print('recv conenction error')
			break
		except OSError:
			print('aborted by user?')
			break

		data += frame

		if b';' in data:
			ind = data.index(b';')
			head = data[:ind].decode('utf-8')
			data = data[ind+1:]

			source, to_recv = head.split(',')
			to_recv = int(to_recv)

			if source in user_volumes:
				volume = play_volume * user_volumes[source]
			else:
				volume = play_volume
				print(f'unknown guy: {source}')
				user_volumes[source] = 1

			left = to_recv - len(data)
			while left > 0:
				try:
					frame = s.recv(left)
				except (ConnectionResetError, ConnectionAbortedError):
					if Running:
						print('connection error')
					break
				left -= len(frame)
				data += frame

			audio = data[:to_recv]
			audio = zlib.decompress(audio)
			
			audio = audioop.mul(audio, audio_samples_width_in_bytes, volume)
			if source in stdouts:
				stdout = stdouts[source]
			else:
				print(f'new audio channel for: {source}')
				stdout = example_stdout()
				stdouts[source] = stdout
				
			stdout.write(audio)

			data = data[to_recv:]

	for name in stdouts:
		stdout = stdouts[name]

		stdout.stop_stream()
		stdout.close()
	#pyaud.terminate()

	Running.new(0)
	s.close()


