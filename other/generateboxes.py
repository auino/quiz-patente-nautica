import os
import requests

try: os.mkdir('img')
except: pass
try: os.mkdir('img/liguria')
except: pass

def removetags(a):
	r = []
	for e in a:
		if len(e) == 0: continue
		if e[0] == '<': e = e[e.index('>')+1:]
		e = e[:e.index('<')]
		r.append(e)
	return r

def removeresults(a):
	r = []
	for e in a:
		if len(e) <= 2: continue
		r.append(e[e.index('|')+2:])
	return r

def getimage(s):
	s = s.replace('\\\'', '"')
	s = s.replace('\'', '"')
	s = s[s.index('src'):]
	s = s[s.index('"')+1:]
	s = s[:s.index('"')]
	url = 'https://www.quizpatentenautica.net/Liguria/{}'.format(s)
	s = s.replace('img', 'img/liguria')
	response = requests.get(url)
	f = open(s, "wb")
	f.write(response.content)
	f.close()
	return s

def getcorrectanswer(a):
	c = 1
	for i in range(0, len(a)):
		if len(a[i]) == 0: continue
		if a[i][0].upper() == 'V': return c
		c += 1
	return 0

enc = 'iso-8859-15'
f = open('/tmp/out.html', 'r', encoding=enc)
t = f.read()
f.close()

quiz = []
for qanda in t.split('<div class="domanda">'):
	if len(qanda) == 0: continue
	d = qanda.split('\n')
	image = ''
	if '<img ' in d[1]:
		image = getimage(d[1])
		d = [d[0]] + d[2:]
	d = removetags(d)
	correctanswer = getcorrectanswer(d[1:])
	q = d[0]
	count = q[:q.index(' ')]
	d = removeresults(d[1:])
	q = q[q.index(' ')+1:]
	print('Numero: {}\nDomanda: {}\nImmagine: {}\nRisposta1: {}\nRisposta2: {}\nRisposta3: {}\nRispostaCorretta: {}\n'.format(count, q, image, d[0], d[1], d[2], correctanswer))
