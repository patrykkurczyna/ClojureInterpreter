
import sys
import ply.yacc as yacc
from ClojureParser import ClojureParser
from Interpreter import Interpreter


if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            filename = sys.argv[1]
            file = open(filename, "r")
        except IOError:
            print("Error while trying to open {0} file".format(filename))
            sys.exit(0)

        ClojureParser = ClojureParser()
        parser = yacc.yacc(module=ClojureParser)

        text = file.read()
        ast = parser.parse(text, lexer=ClojureParser.scanner)
        ast.accept2(Interpreter())
    else:
        ClojureParser = ClojureParser()
        parser = yacc.yacc(module=ClojureParser)
        print "Welcome to Clojure Interpreter "
        print " "
        print "Type 'exit' to quit."
        print " "
        print ">>>",
        line = sys.stdin.readline()

        while line:
            if line.rstrip("\n") == "exit":
                break
            ast = parser.parse(line, lexer=ClojureParser.scanner)
            ast.accept2(Interpreter())
            print ">>>",
            line = sys.stdin.readline()
