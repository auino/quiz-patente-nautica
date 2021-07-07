#!/bin/bash
SLOTS_COUNT=7
MIN_VALUES=(1 136 221 300 563 628 1041)
MAX_VALUES=(135 220 299 562 627 1040 1152)
#COUNT_VALUES=(135 85 79 263 65 413 112)
rm /tmp/out.html 2> /dev/null
for CAP in $(seq 1 $SLOTS_COUNT); do
	for DA in $(seq ${MIN_VALUES[`expr $CAP - 1`]} 5 ${MAX_VALUES[`expr $CAP - 1`]}); do
		A=`expr $DA + 4`
		if [ $A -gt ${MAX_VALUES[`expr $CAP - 1`]} ]; then A=${MAX_VALUES[`expr $CAP - 1`]}; fi
		G=`expr $A - $DA + 1`
		URL="https://www.quizpatentenautica.net/Liguria/raggruppamentoBASE_correttore.asp?CAP=${CAP}&VIS=${DA}-${A}&DA=${DA}&A=${A}&G=${G}&GT=${G}"

		DATA=""
		C=0
		Ci=1
		for i in $(seq $DA $A); do
			C=`expr $C + 1`
			Ci=`expr $C \* 3 - 2`
			CiStart=`expr $i \* 3 - 2`
			ORDINE1=`expr $i \* 3`
			ORDINE2=`expr $ORDINE1 + 1`
			ORDINE3=`expr $ORDINE1 + 2`
			DATA="${DATA}DOMANDA${C}=${i}&ORDINE${C}${Ci}=${CiStart}&ORDINE${C}`expr $Ci + 1`=`expr $CiStart + 1`&ORDINE${C}`expr $Ci + 2`=`expr $CiStart + 2`&"
		done
		DATA="${DATA}B1=VERIFICA"

		curl -s $URL \
			-X 'POST' \
			-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
			-H 'Content-Type: application/x-www-form-urlencoded' \
			-H 'Origin: https://www.quizpatentenautica.net' \
			-H 'Cookie: displayCookieConsent=y; ASPSESSIONIDSUTABDTA=PHNOMJIBPGGJNHLMJDMANCJI' \
			-H 'Accept-Language: it-it' \
			-H 'Host: www.quizpatentenautica.net' \
			-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15' \
			-H 'Referer: https://www.quizpatentenautica.net/Liguria/raggruppamentoBASE_genera.asp?CAP=1&VIS=1-5&DA=1&A=5&G=5&GT=5' \
			-H 'Accept-Encoding: gzip, deflate, br' \
			-H 'Connection: keep-alive' \
			-H "Content-Length: ${#DATA}" \
			--data "$DATA"|grep -e "domanda\|RISPOSTA\|img\ alt=\"\"\ src="|grep -v 'id="pub"'|sed 's/\t*//' >> /tmp/out.html
		echo "$CAP > $DA $A"
	done
done

