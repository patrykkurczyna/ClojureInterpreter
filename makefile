arithm: 
	python main.py arytmetyczne.txt

expr: 
	python main.py wyrazenia.txt

logic: 
	python main.py logiczne.txt
	
comp: 
	python main.py porownania.txt
	
coll: 
	python main.py kolekcje.txt
	
strings: 
	python main.py stringi.txt

run:
	tests clean
	
tests:
	python main.py arytmetyczne.txt
	python main.py wyrazenia.txt
	python main.py logiczne.txt
	python main.py porownania.txt
	python main.py kolekcje.txt
	python main.py stringi.txt

clean:
	rm -f *.pyc parser.out parsetab.py *~
