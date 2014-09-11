import sys
import os
import main

if len(sys.argv) < 2:
    print "Usage: python tests.py <arithm | logic | expr | comp | coll | strings | all> "
else:
    for x in range(1, len(sys.argv)):
        if sys.argv[x] == "arithm":
            os.system("python main.py arytmetyczne.txt")
        elif sys.argv[x] == "logic":
            os.system("python main.py logiczne.txt")
        elif sys.argv[x] == "expr":
            os.system("python main.py wyrazenia.txt")
        elif sys.argv[x] == "comp":
            os.system("python main.py porownania.txt")
        elif sys.argv[x] == "coll":
            os.system("python main.py kolekcje.txt")
        elif sys.argv[x] == "strings":
            os.system("python main.py stringitxt")
        elif sys.argv[x] == "all":
            os.system("python main.py arytmetyczne.txt")
            os.system("python main.py logiczne.txt")
            os.system("python main.py porownania.txt")
            os.system("python main.py wyrazenia.txt")
            os.system("python main.py kolekcje.txt")
            os.system("python main.py stringi.txt")

