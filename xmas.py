from __future__ import print_function
import time
import numpy as np

SIMULATE = True

class BrokenLED:
	def __init__(self, pin):
		pass

	def on(self):
		pass

	def off(self):
		pass

if SIMULATE:
	LED = BrokenLED
else:
	from gpiozero import LED

channels = [LED(x) for x in [14, 15, 18, 23, 24, 25, 8, 7]]
channels[2] = BrokenLED(18)

def sweep_on():
	for c in channels:
		c.on()
		time.sleep(0.5)

def sweep_off():
	for c in reversed(channels):
		c.off()
		time.sleep(0.5)

def get_channel_energies(bucket):
	energies = [0.0] * 8
	energies[0] = sum(bucket[0:5])
	energies[1] = sum(bucket[5:10])
	energies[2] = sum(bucket[10:15])
	energies[3] = sum(bucket[15:20])
	energies[4] = sum(bucket[20:25])
	energies[5] = sum(bucket[25:30])
	energies[6] = sum(bucket[30:35])
	energies[7] = sum(bucket[35:40])
	return energies

class SimulatedPlayer:
	def __init__(self, audiofile):
		self.wav = audiofile + ".wav"
		pass

	def start(self):
		import subprocess, sys
		self.p = subprocess.Popen("mplayer {}".format(self.wav), shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

class ActualPlayer:
	def __init__(self, audiofile):
		self.wav = audiofile

	def start(self):
		r = requests.get("http://molybdenum.local:6543/tx?src={}.f32&freq=99500000&rate=1000000&gain=30")
		r.text

def draw_mel(stdscr, mel_data, player):
	# Average the mel data into buckets
	DT = 0.1
	tm = 0.0
	processed = []
	bucket = []
	for ts,spectra in mel_data:
		if ts > tm + DT:
			tm += DT
			processed.append(np.mean(np.array(bucket), axis=0))
			bucket = []
		bucket.append(spectra)

	# Channelize the data
	channel_energies = []
	for bucket in processed:
		channel_energies.append(get_channel_energies(bucket))

	player.start()
	start_tm = time.time()
	avgs = [0.0] * 8
	import itertools
	for i,bucket in enumerate(channel_energies):
		while i*DT > time.time() - start_tm:
			pass
		is_on = [False] * 8
		for j in range(8):
			is_on[j] = bucket[j] > avgs[j]
			avgs[j] = avgs[j] * 0.8 + bucket[j] * 0.2
			if is_on[j]:
				channels[j].on()
			else:
				channels[j].off()
		for chan,x in enumerate(is_on):
			for r,c in itertools.product(range(5, 10), range(chan*6, chan*6+5)):
				if x:
					stdscr.addstr(r, c, " ", curses.A_REVERSE)
				else:
					stdscr.addstr(r, c, " ")
		stdscr.refresh()
	pass

def parse_mel(fname):
	l = []
	for line in open(fname).readlines():
		parts = [float(s) for s in line.strip(" \r\n").split(" ")]
		l.append((parts[0], parts[1:]))
	return l

def playSong(stdscr, song):
	if SIMULATE:
		player = SimulatedPlayer(song)
	else:
		player = ActualPlayer(song)
	mel = parse_mel("{}.mel".format(song))
	draw_mel(stdscr, mel, player)

import curses

def main(stdscr):
	stdscr.clear()

	#import arrow
	#while True:
	#	h = arrow.now().to('US/Central').hour
	#	if (h >= 17 and h <= 23) or (h == 7):
	#		print "Turning all on"
	#		[x.on() for x in channels]
	#	else:
	#		print "Turning all off"
	#		[x.off() for x in channels]
	#	time.sleep(120)
	#	pass

	import sys
	if len(sys.argv) == 1:
		raise Exception("You must supply the prefix of the .wav and .mel files as a command line argument!")
	playSong(stdscr, sys.argv[1])

	stdscr.endwin()

curses.wrapper(main)
