import os
import requests

try: os.mkdir('img')
except: pass
try: os.mkdir('img/genova2018')
except: pass

def removetags(a):
	r = []
	for e in a:
		if len(e) == 0: continue
		if e[0] == '<': e = e[e.index('>')+1:]
		r.append(e)
	return r

def removeindexes(l):
	for i in range(0, len(l)):
		l[i] = l[i][l[i].index(')')+2:]
	return l

def getimage(s):
	s = s.replace('\\\'', '"')
	s = s.replace('\'', '"')
	s = s[s.index('src'):]
	s = s[s.index('"')+1:]
	s = s[:s.index('"')]
	url = 'https://www.nauticando.net/{}'.format(s)
	s = s.replace('img/quiz-patente-nautica', 'img/genova2018')
	if s[0] == '/': s = s[1:]
	response = requests.get(url)
	f = open(s, "wb")
	f.write(response.content)
	f.close()
	return s

def getcorrectanswer(a):
	for i in range(0, len(a)):
		if 'data-correct="1"' in a[i].lower(): return i + 1
	return 0

#enc = 'iso-8859-15'
f = open('/tmp/output.txt', 'r') #	, encoding=enc)
t = f.read()
f.close()

quiz = []
quiznumber = 1
for qanda in t.split('<div class="col-12 '):
	if len(qanda) == 0: continue
	d = qanda.split('\n')
	image = ''
	if '<img ' in d[1]:
		image = getimage(d[1])
		d = [d[0]] + d[2:]
	correctanswer = getcorrectanswer(d[1:])
	d = removetags(d)
	q = d[0]
	if 'pb-10">' in q: q = q[q.index('>')+1:]
	d = removeindexes(d[1:])
	print('Numero: {}\nDomanda: {}\nImmagine: {}\nRisposta1: {}\nRisposta2: {}\nRisposta3: {}\nRispostaCorretta: {}\n'.format(quiznumber, q, image, d[0], d[1], d[2], correctanswer))
	quiznumber += 1
