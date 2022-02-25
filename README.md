# quiz-patente-nautica

*This project is supposed to be used for Italian users. Therefore, the whole content of the generated documents, including the README file, is in Italian language.*

### Introduzione ###

Questo software permette di prepararsi all'esame teorico per il conseguimento dell'abilitazione alla navigazione entro le 12 miglia, considerando i [quiz del Ministero delle Infrastrutture de della Mobilità Sostenibili (MIMS), Decreto Direttoriale n. 10 del 25 gennaio 2022 (d.m. 323 del 10/08/2021)](https://www.mit.gov.it/nfsmitgov/files/media/normativa/2022-02/ALLEGATO%20A%20DD%2010%20DEL%2025GEN2022.pdf) (anno 2022).

### Caratteristiche ###

* Dettagli sugli errori fatti, con output colorato
* Supporto a quiz contenenti immagini
* Possibilità di simulare un possibile esame, eventualmente ripetendo una simulazione specifica
* Possibilità di filtrare i quiz (in base alla numerazione; in base ad una query di ricerca, sia sulla domanda che sulle risposte; solo quiz contenenti immagini)
* Possibilità di ignorare un quiz (premendo il tasto invio)
* Riassunto dettagliato sull'andamento dei quiz, per ogni esecuzione, in termini di risposte corrette, ignorate ed errate, per eventuali raffinamenti della propria preparazione

### Installazione ###

* Per prima cosa, clonare il repository:
```
git clone https://github.com/auino/quiz-patente-nautica.git
```
* Accedere alla directory appena creata:
```
cd quiz-patente-nautica
```
* Installare le dipendenze (per dispositivi dotati di processore Apple M1, procedere con una [installazione manuale di matplotlib](https://stackoverflow.com/questions/66122146/pip-install-matplotlib-fails-on-m1-mac), dunque installare manualmente le altre dipendenze dal file `requirements.txt`):
```
pip3 install -r requirements.txt
```

### Esecuzione ###

Vengono riportati a seguire alcuni comandi di esempio.

* Mostrare l'help
```
python3 generatequiz.py --help
```
* Fare tutti i quiz registrati (funzionalità utile per poter studiare tutti i quiz in modo sequenziale)
```
python3 generatequiz.py
```
* Fare solo i quiz `1`, `10`, `100` e `1000` (funzionalità utile per poter ripetere quiz considerati particolarmente difficili)
```
python3 generatequiz.py --select 1,10,100,1000
```
* Fare solo i quiz che contengono la parola `bandiera` (case insensitive) nella domanda (funzionalità utile per poter affrontare solo un insieme di quiz specifici)
```
python3 generatequiz.py --search bandiera
```
* Fare solo i quiz che contengono la parola `chiglia` (case insensitive) in almeno una delle risposte (funzionalità utile per poter riprendere evenquali quiz dei quali non si ricorda la domanda)
```
python3 generatequiz.py --searchanswer chiglia
```
* Fare solo i quiz che contengono immagini (funzionalità utile per poter affrontare solo quiz visivi come quelli sui fanali previsi)
```
python3 generatequiz.py --onlyimages
```
* Mischiare le risposte (funzionalità utile per ricordare al meglio la risposta corretta)
```
python3 generatequiz.py --shuffle
```
* Fare una simulazione di esame (funzionalità utile per una preparazione a ridosso dell'esame finale; è eventualmente possibile ottenere l'identificativo dell'esame scorrendo la schermata sopra la prima domanda)
```
python3 generatequiz.py --exam
```
* Fare una simulazione di esame, senza mostrare la risposta corretta per ogni domanda
```
python3 generatequiz.py --exam --nodirectanswers
```
* Ripetere una simulazione di esame (sulla base di un identificativo di esame specifico)
```
python3 generatequiz.py --repeatexam 12345
```
* Caricare un file differente da quello di default, ad esempio, quello di vela
```
python3 generatequiz.py --file quiz/mims2022-vela.txt
```

Al termine dell'esecuzione, i numeri delle eventuali risposte errate verranno mostrati in output.

### Suggerimenti per l'utilizzo ###

Una volta studiata in modo approfondito la parte teorica, si suggerisce di procedere come segue:
1. Rispondere tutti i quiz
```
python3 generatequiz.py
```
eventualmente, un poco per volta, come nell'esempio a seguire (solo i primi `100` quiz):
```
python3 generatequiz.py --range 1-100
```
salvando tutte le risposte errate fornite dal programma.

2. Ripetere eventuali errori:
```
python3 generatequiz.py --select 1,10,100,1000
```
inserendo la lista delle risposte errate.

3. Ripetere eventualmente il punto precedente finché non si sostengano più errori.

4. Fare molte simulazioni di esame:
```
python3 generatequiz.py --exam
```

5. Eventualmente, ripetere una simulazione specifica:
```
python3 generatequiz.py --repeatexam 12345
```

### Estensioni ###

Sebbene il software riporti solamente specifici casi di utilizzo, è possibile estenderlo con qualsiasi tipo di esame ministeriale basato su test a risposta multipla, con tre opzioni disponibili, utilizzando il formato riportato nei quiz di esempio.

In riferimento a ciò, consultare i file all'interno della directory `quiz`, considerando che:
* le righe che iniziano con il carattere `#` identificano commenti
* la prima riga utile deve contenere dettagli utili per l'esame, rispettando il formato presente nei file all'interno della directory `quiz`
* la struttura ed i nomi delle proprietà deve restare invariata

### Osservazioni sui quiz ###

I [quiz del Ministero delle Infrastrutture de della Mobilità Sostenibili (MIMS), Decreto Direttoriale n. 10 del 25 gennaio 2022 (d.m. 323 del 10/08/2021)](https://www.mit.gov.it/nfsmitgov/files/media/normativa/2022-02/ALLEGATO%20A%20DD%2010%20DEL%2025GEN2022.pdf) disponibili non riportano la domanda numero 1.4.2.38.
Per questo motivo, i quiz presenti in questo documento sono stati adattati, specialmente per quanto riguarda la numerazione, per escludere questo test.

### Contatti ###

E' possibile trovarmi su [Twitter](https://twitter.com) come [@auino](https://twitter.com/auino).
