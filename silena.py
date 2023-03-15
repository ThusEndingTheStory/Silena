from sys import argv
from os import system

# /bin/bash -c "$(curl -fsSL https://exaloop.io/install.sh)"
# codon build -release -exe silena2/silena.py

class w:
	sh = ""

	def write(string):
		w.sh += string

funcNames = []
silnPath = "./silena2/"

def getFuncsFromFile(file):
	f = open(file, "r").readlines()
	for line in f:
		words = line.split()
		if not not words:
			if not len(words) == 1:
				if words[1] == "()":
					funcNames.append(words[0])
				elif words[0] == "function":
					funcNames.append(words[1])
	return funcNames

def info(msg):
	print(f"\x1b[34mSilena:\n  {msg}")

def err(msg):
  # system('clear')
  info(f"\x1b[31mError:\n    {msg}\x1b[0m")
  exit(1)

def openTargetFile():
	try:
		return open(argv[1], "r")
	except:
		err("Couldn't open target file")
		
def load(file):
	lineNum = 0
	
	for line in file:
		lineNum += 1
		words = line.split()
		if words == []:
			w.write("\n")
		elif words[0] == ">>":
			w.write("# ")
			i = 0
			while i < len(words)-1:
				w.write(words[i+1] + " ")
				i += 1
			w.write("\n")
		elif words[0] == "&using":
			if words[1] != "local":
				w.write(f"source \"{silnPath}extensions/" + words[1] + "\"\n")
				getFuncsFromFile(f"{silnPath}extensions/" + words[1])
			else:
				w.write("source \"" + words[2] + "\"\n")
				getFuncsFromFile(words[2])
		elif words[0] == "input":
			w.write("read " + words[1] + "\n")
		elif words[0] == "clear":
			w.write("clear\n")
		elif words[0] == "wait":
			w.write("sleep " + words[1] + "\n")
		# Loops
		elif words[0] == "while":
			w.write("while ")
			i = 0
			while i < len(words)-1:
				w.write(words[i+1] + " ")
				i += 1
			w.write("; do\n")
		elif words[0] == "for":
			w.write("for ")
			i = 0
			while i < len(words)-1:
				w.write(words[i+1] + " ")
				i += 1
			w.write("; do\n")
		elif words[0] == "endloop":
			w.write("done")
			i = 0
			while i < len(words)-1:
				w.write(words[i+1] + " ")
				i += 1
			w.write("\n")
		# End of loops
		# Math
		elif words[0] == "math(":
			w.write("((")
			added = ""
			for word in words:
				if not word == "math(":
					for char in word:
						if not char == ")":
							added += char
						else:
							break
			w.write(added + "))\n")
		# End of math
		# Functions
		elif words[0] == "func":
			funcNames.append(words[1])
			w.write(words[1] + " () {\n")
		elif words[0] == "endfunc":
			w.write("}\n")
		# End of functions
		# If statements
		elif words[0] == "if":
			w.write("if [ ")
			i = 0
			while i < len(words)-1:
				if words[i+1] == "&&":
					w.write("] && [ ")
				elif words[i+1] == "||":
					w.write("] || [ ")
				else:
					w.write(words[i+1] + " ")
				i += 1
			w.write("]; then\n")
		elif words[0] == "elif":
			w.write("elif [ ")
			i = 0
			while i < len(words)-1:
				if words[i+1] == "&&":
					w.write("] && [ ")
				elif words[i+1] == "||":
					w.write("] || [ ")
				else:
					w.write(words[i+1] + " ")
				i += 1
			w.write("]; then\n")
		elif words[0] == "else":
			w.write("else\n")
		elif words[0] == "end":
			w.write("fi\n")
		# End of if statements
		# Write
		elif words[0] == "write":
			w.write("printf ")
			i = 0
			while i < len(words)-1:
				w.write(words[i+1] + " ")
				i += 1
			w.write("\n")
		# End of write
		# Variables
		elif words[0] == "assign":
			w.write(words[1] + "=")
			i = 0
			while i < len(words)-2:
				w.write(words[i+2] + " ")
				i += 1
			w.write("\n")
		# End of variables
		else:
			error = True
			if words[0] in funcNames:
				error = False
				i = 0
				while i < len(words):
					w.write(words[i] + " ")
					i += 1
				w.write("\n")
			else:
				for word in words:
					if word in funcNames:
						error = False
				if error:
					if line[len(line)-1:] == "\n":
						err("Line " + str(lineNum) + ": Command '\x1b[34m" + line[:len(line)-1] + "\x1b[31m' not found")
					else:
						err("Line " + str(lineNum) + ": Command '\x1b[34m" + line + "\x1b[31m' not found")

target = openTargetFile()
load(target.readlines())
print(w.sh)
system(w.sh)
