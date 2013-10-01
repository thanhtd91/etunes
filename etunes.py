'''
to convert to mp3
timidity -Or -o - first_succesful_tune.mid | lame -r - first_succesful_tune.mp3

'''
# importing all the necessary modules
from pyknon.genmidi import Midi
from pyknon.music import NoteSeq

import random


import os


import subprocess as sub
import re
import time

# sample notes pool // Q = Quarter notes // E = One Eigth Notes
notesPoolQuarter = ['C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'Bb4', 'B4']
notesPoolEighth = ['C8', 'C#8', 'D8', 'D#8', 'E8', 'F8', 'F#8', 'G8', 'G#8', 'A8', 'Bb8', 'B8']
notesPoolSixteenth = ['C16', 'C#16', 'D16', 'D#16', 'E16', 'F16', 'F#16', 'G16', 'G#16', 'A16', 'Bb16', 'B16']
notesPoolThirtySecond = ['C32', 'C#32', 'D32', 'D#32', 'E32', 'F32', 'F#32', 'G32', 'G#32', 'A32', 'Bb32', 'B32']

notesPoolRest = ['R16', 'R32']

notesPoolA = notesPoolSixteenth + notesPoolThirtySecond + notesPoolRest

NUMBER_OF_NOTES = 8
NUMBER_OF_TUNES = 6

# tunes contains NoteSeq objects
tunes = []

# defining a class tune which represents an individual in the population
class Tune:

	# constructor
	def __init__(self):
		self.notes = randomTune()
		self.score = 1

	def crossover(self, b):
		child = Tune()
		midpoint = random.randrange(len(self.notes))
		child.notes = self.notes[:midpoint] + b.notes[midpoint:]
		return child

	def mutate(self, mutationRate = 0.01):
		for i in range(len(self.notes)):
			if random.random() < mutationRate:
				self.notes = self.notes[:i] + NoteSeq(random.choice(notesPoolA)) + self.notes[i + 1:]

	def displayNotes(self):
		print "\t%s%s" % (str(self.notes).ljust(int(NUMBER_OF_NOTES * 8)), self.score)


def randomTune():
	# creating a string of random notes from the pool
	noteString = ''
	for _ in range(NUMBER_OF_NOTES):
		noteString += random.choice(notesPoolA) + " "

	return NoteSeq(noteString)
cd 
# takes a NoteSeq object as parameter
def generateMid(tune):
	midi = Midi()
	midi.seq_notes(tune.notes)
	midi.write("midi/tune.mid")

def playMid():
	sub.Popen(['timidity', 'midi/tune.mid'], stdout=sub.PIPE, stderr=sub.PIPE)

def showAllTunes():
	print '\n\tNOTES'.ljust(int(NUMBER_OF_NOTES * 8)) + 'SCORE'
	for i in tunes:
			i.displayNotes()
	print

def input():

		

		showAllTunes()

		while True:
			print '~~>>',
			command = raw_input()

			match = re.search(r'(\w*) ?(\d*) ?(\d*)', command)
			if match.group(1) == 'play':
				tuneNumber = int(match.group(2)) - 1
				generateMid(tunes[tuneNumber])
				playMid()
				showAllTunes()

			if match.group(1) == 'score':
				print 'scoring...'
				time.sleep(0.5)
				tuneNumber, score = int(match.group(2)) - 1, int(match.group(3))
				tunes[tuneNumber].score = score
				showAllTunes()

			if match.group(1) == 'done':
				return True	

			if match.group(1) == 'choose':
				tuneNumber = int(match.group(2)) - 1
				generateMid(tunes[tuneNumber])
				playMid()
				print 'Well, Okay then. Enjoy your eTune.'
				time.sleep(0.5)
				return False

def main():
	
	for i in range(NUMBER_OF_TUNES):
		tunes.append(Tune())

	os.system('clear')
	print '~~~eTunes~~~'
	time.sleep(0.5)
	print 'Hi! Welcome to eTunes.'
	time.sleep(0.5)
	print 'We will be using', NUMBER_OF_TUNES, 'tunes',
	print 'with each having', NUMBER_OF_NOTES, 'notes.'
	time.sleep(0.5)
	print '\nThe contents of the music pool is shown below.'


	flag = input()

	while flag:

		print 'mating tunes...'
		time.sleep(0.5)
		print 'mutating tunelings...'
		time.sleep(0.5)
		print 'done...'
		time.sleep(1)

		matingPool = []
		for i in range(NUMBER_OF_TUNES):
			for j in range(tunes[i].score):
				matingPool.append(tunes[i])

		for i in range(NUMBER_OF_TUNES):
			a, b = random.sample(matingPool, 2)

			# todo: receive two children from crossover
			child = a.crossover(b)
			child.mutate()
			tunes[i] = child

		while True:
			try:
				flag = input()
				break
			except IndexError:
				print
			except:
				print 'Oops! You must\'ve typed something wrong. Why don\'t you try again.'

main()
