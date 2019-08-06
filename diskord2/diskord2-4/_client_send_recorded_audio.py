import audioop
import zlib
from uuid import getnode as get_mac

import pyaudio

from _reads import *



audio_format = pyaudio.paInt16
audio_quality = 44100
#frames_per_buffer = 2048


header_mac = (hex(get_mac())[2:]+';').encode('utf_8')

pyaud = pyaudio.PyAudio()
#da napravq recordinga na separate thread
def send_recorded_audio(Running, s, muted):
	frames_per_buffer = read_int('client/recorded-frames-per-buffer.txt')
	stdin = pyaud.open(
    format=audio_format,
    channels=1,
    rate=audio_quality,
    input=True,
    output=False,
    frames_per_buffer=frames_per_buffer
	)
	audio_samples_width_in_bytes = read_int('client/audio-samples-width-in-bytes.txt')
	record_volume = read_float('client/record-volume.txt')

	compression_level = read_int('client/audio-compression.txt')

	while Running:
		data = stdin.read(frames_per_buffer)
		if muted():
			data = audioop.mul(data, audio_samples_width_in_bytes, 0)
		else:
			data = audioop.mul(data, audio_samples_width_in_bytes, record_volume)

		data = zlib.compress(data, compression_level)
		header = f'{ len(data) };'.encode('utf-8')
		try:
			s.sendall(header + data)
		except ConnectionResetError:
			print('server has shut down / is restarting')
			break
		except OSError:#manual shutdown
			break
	stdin.stop_stream()
	stdin.close()
	#pyaud.terminate()

	Running.new(0)
	s.close()
