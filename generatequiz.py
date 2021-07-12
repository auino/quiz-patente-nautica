import os
import json
import time
import random
import argparse
import datetime
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from termcolor import colored

### DATA BASED ON THE FOLLOWING EXAMINATION:
### LIGURIA - ENTRO LE 12 MIGLIA - 2018
### BEGIN

DEFAULT_QUIZ = 'quiz/genova2018.txt'

### END

CLEAR_SCREEN = False

def screen_clear():
	if os.name == 'posix': # for mac and linux(here, os.name is 'posix')
		_ = os.system('clear')
	else: # for windows platfrom
		_ = os.system('cls')

def alphabetasarray():
	m = []
	s = 'A'
	for i in range(0, 26): m.append(chr(ord(s)+i))
	return m

def numbertoa(n):
	m = alphabetasarray()
	return m[int(n)-1]

def atonumber(a):
	m = alphabetasarray()
	for i in range(0, len(m)):
		if a.upper() == m[i]: return i+1
	return 0

def removecommentedlines(s):
	r = []
	for s in s.split('\n'):
		if len(s) > 0 and s[0] == '#': continue
		r.append(s)
	return '\n'.join(r)

def loaddata(filename):
	r = []
	f = open(filename, 'r')
	d = f.read()
	f.close()
	d = removecommentedlines(d)
	basicdata = json.loads(d.split('\n')[0])
	d = d[d.index('\n')+1:]
	for slot in d.split('\n\n'):
		e = {}
		for row in slot.split('\n'):
			try:
				k = row[:row.index(':')].strip().lower()
				v = row[row.index(':')+1:].strip()
				e[str(k)] = str(v)
			except: pass
		r.append(e)
	return {'exam_info':basicdata, 'questions':r}

def filterquizbynumber(l, f):
	r = []
	for i in range(0, len(f)): f[i] = int(f[i])
	for e in l:
		if e.get('numero') is None: continue
		if int(e.get('numero')) in f: r.append(e)
	return r

def filterquizbyquestion(l, f):
	r = []
	for e in l:
		if f.lower() in e.get('domanda').lower(): r.append(e)
	return r

def filterquizbyanswer(l, f):
	r = []
	for e in l:
		shouldadd = False
		if f.lower() in e.get('risposta1').lower(): shouldadd = True
		if f.lower() in e.get('risposta2').lower(): shouldadd = True
		if f.lower() in e.get('risposta3').lower(): shouldadd = True
		if shouldadd: r.append(e)
	return r

def filterquizbyimage(l):
	r = []
	for e in l:
		if len(e.get('immagine')) > 0: r.append(e)
	return r

def generaterandomexam(l, exam_info, seed):
	r = []
	print("Identificativo utilizzato per la simulazione di esame: {}".format(seed))
	random.seed(seed)
	for e in exam_info:
		block_list = l[e.get('from')-1:e.get('to')]
		random.shuffle(block_list)
		r += block_list[:e.get('count')]
	return r

def shuffle_answers(d):
	a = [d.get('risposta1'), d.get('risposta2'), d.get('risposta3')]
	rispostacorretta_text = a[int(d.get('rispostacorretta'))-1]
	random.shuffle(a)
	d['rispostacorretta'] = 0
	for i in range(0, len(a)):
		if a[i] == rispostacorretta_text:
			d['rispostacorretta'] = i+1
			break
	d['risposta1'] = a[0]
	d['risposta2'] = a[1]
	d['risposta3'] = a[2]
	return d

def showquiz(l, shouldshuffle, nodirectanswers, seed, success_percentage):
	screen_clear()
	correctnumbers = []
	wrongnumbers = []
	ignorednumbers = []
	i = 1
	for q in l:
		if shouldshuffle: q = shuffle_answers(q)
		print('Domanda #{} ({}/{}): {}\n A. {}\n B. {}\n C. {}'.format(q.get('numero'), i, len(l), q.get('domanda'), q.get('risposta1'), q.get('risposta2'), q.get('risposta3')))
		if len(q.get('immagine')) > 0:
			img = mpimg.imread(q.get('immagine'))
			imgplot = plt.imshow(img)
			plt.show()
		r = input('Opzione scelta: ')
		if len(r) == 0:
			if not nodirectanswers: print(colored('Risposta ignorata. La risposta corretta è la {}.'.format(numbertoa(q.get('rispostacorretta'))), 'grey'))
			ignorednumbers.append(q.get('numero'))
		else:
			if atonumber(r[0]) == int(q.get('rispostacorretta')):
				if not nodirectanswers: print(colored('Corretto!', 'green'))
				correctnumbers.append(q.get('numero'))
			else:
				if not nodirectanswers: print(colored('Errato. La risposta corretta è la {}.'.format(numbertoa(q.get('rispostacorretta'))), 'red'))
				wrongnumbers.append(q.get('numero'))
		print('')
		if CLEAR_SCREEN:
			time.sleep(2)
			screen_clear()
		i += 1
	if (len(l) - len(ignorednumbers)) > 0: print('Risultato del quiz: {} ({}/{})'.format((colored('superato', 'green') if (len(correctnumbers)/(len(l) - len(ignorednumbers)) >= float(success_percentage)) else colored('non superato', 'red')), len(correctnumbers), len(l)-len(ignorednumbers)))
	if len(correctnumbers) > 0: print('Numero di quiz delle risposte corrette: {}'.format(','.join(correctnumbers)))
	if len(ignorednumbers) > 0: print('Numero di quiz delle risposte ignorate: {}'.format(','.join(ignorednumbers)))
	if len(wrongnumbers) > 0: print('Numero di quiz delle risposte errate: {}'.format(','.join(wrongnumbers)))

# Main program

# arguments configuration
parser = argparse.ArgumentParser(description='Quiz patente nautica - Liguria - Entro le 12 miglia')
parser.add_argument('--file', type=str, default=DEFAULT_QUIZ,
	help='il file da utilizzare (default "{}")'.format(DEFAULT_QUIZ))
parser.add_argument('--range', type=str,
	help='i numeri iniziale e finale dei quiz da selezionare, separati da trattino, (es. "1-135", considerando sia il quiz numero 1 che il quiz numero 135)')
parser.add_argument('--select', type=str,
	help='la lista di quiz da selezionare, in base al loro numero, separati da virgola (es. "1,10,100,1000"')
parser.add_argument('--search', type=str,
	help='inserendo una stringa di testo, verranno considerati solamente i quiz che contengono tale stringa nella domanda (es. "bandiera")')
parser.add_argument('--searchanswer', type=str,
	help='inserendo una stringa di testo, verranno considerati solamente i quiz che contengono tale stringa nella risposta (es. "chiglia")')
parser.add_argument('--onlyimages', action='store_true', default=False,
	help='per selezionare solo i quiz contenenti immagini')
parser.add_argument('--shuffle', action='store_true', default=False,
	help='per mischiare casualmente le risposte')
parser.add_argument('--nodirectanswers', action='store_true', default=False,
	help='per evitare di ottenere immediatatamente la risposta corretta')
parser.add_argument('--exam', action='store_true', default=False,
	help='per generare un possibile testo di esame')
parser.add_argument('--repeatexam', type=str,
	help='inserendo l\'identificativo utilizzato per una simulazione di esame precedentemente fatta, sarà possibile ripeterla (es. "12345")')

args = parser.parse_args()

# loading data
data = loaddata(args.file)
exam_info = data.get('exam_info')
quiz = data.get('questions')

# parsing arguments and acting accordingly
if args.range != None:
	f = []
	for i in range(int(args.range.split('-')[0]), int(args.range.split('-')[1])+1): f.append(i)
	quiz = filterquizbynumber(quiz, f)
if args.select != None: quiz = filterquizbynumber(quiz, args.select.split(','))
if args.search != None: quiz = filterquizbyquestion(quiz, args.search)
if args.searchanswer != None: quiz = filterquizbyanswer(quiz, args.searchanswer)
if args.onlyimages: quiz = filterquizbyimage(quiz)
seed = None
if args.exam:
	seed = int(time.time())
	quiz = generaterandomexam(quiz, exam_info.get('exam_details'), seed)
if args.repeatexam != None:
	seed = int(args.repeatexam)
	quiz = generaterandomexam(quiz, exam_info.get('exam_details'), seed)

# sorting the list
quiz = sorted(quiz, key=lambda x: int(x.get('numero')))

# saving start time
starttime = time.time()

# showing the list of quiz
try: showquiz(quiz, args.shuffle, args.nodirectanswers, seed, exam_info.get('exam_success_percentage'))
except KeyboardInterrupt as e: print('')

if seed != None:
	print('Identificativo della simulazione di esame: {}'.format(seed))
	# showing elapsed time
	endtime = time.time()
	elapsedtime = int(endtime - starttime)
	elapsedtime = str(datetime.timedelta(seconds=elapsedtime))
	print('Durata della simulazione: {}'.format(elapsedtime))
