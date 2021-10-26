
dot:
	python3 cicgraph.py ${OPT} ${FNAME}.yaml && dot -Tsvg ${FNAME}.dot -o${FNAME}.svg && dot -Tpdf ${FNAME}.dot -o${FNAME}.pdf

neato:
	python3 cicgraph.py ${OPT} ${FNAME}.yaml && neato -Tsvg ${FNAME}.dot -o${FNAME}.svg && neato -Tpdf ${FNAME}.dot -o${FNAME}.pdf


clean:
	rm *.svg *.dot *.ps *.pdf
