
# docs:
# https://docs.python.org/2/library/cmd.html
# https://hg.python.org/cpython/file/2.7/Lib/cmd.py
# http://pymotw.com/2/cmd/

import os, cmd, random, urllib2, shutil, platform
from colorama import Fore, Back, Style

# Colorama: https://pypi.python.org/pypi/colorama
# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL

import ontospy
from libs.util import *
from libs.quotes import QUOTES


class Shell(cmd.Cmd):
	"""Simple command processor example."""

	prompt = Fore.BLUE + Style.BRIGHT +'<OntoSPy>: ' + Style.RESET_ALL
	intro = "Type 'help' to get started. Use TAB to explore commands."

	doc_header = 'Commands'
	misc_header = 'Miscellaneous'
	undoc_header = 'Undocumented commands'
	
	ruler = '-'
	
	def emptyline(self):
		""" override default behaviour of running last command """
		pass
		
	def __init__(self):
		 """
		 self.current = {'file' : filename, 'fullpath' : fullpath, 'graph': g}
		 self.currentEntity = {'entity' : entity, 'type' : 'class' } [?]
		 """
		 # useful vars
		 self.LOCAL = ontospy.ONTOSPY_LOCAL
		 self.LOCAL_MODELS = ontospy.ONTOSPY_LOCAL_MODELS
		 self.ontologies = ontospy.get_localontologies()
		 self.current = None
		 self.currentEntity = None
		 
		 cmd.Cmd.__init__(self)


	# HELPER METHODS
	# --------	

	def _get_prompt(self, onto="", entity="", default_entity_color=Fore.BLUE):
		""" changes the prompt contextually """
		if entity:
			onto = self.current['file']
			temp1_1 = default_entity_color + Style.NORMAL + '%s: ' % truncate(onto, 20)
			temp1_2 = default_entity_color + Style.BRIGHT + '%s' % entity
			temp2 = '<OntoSPy: %s>: ' % (temp1_1 + temp1_2)
			return Fore.BLUE + Style.BRIGHT + temp2 + Style.RESET_ALL
		elif onto:
			temp1 = default_entity_color + '%s' % onto 
			temp2 = '<OntoSPy: %s>: ' % temp1
			return Fore.BLUE + Style.BRIGHT + temp2 + Style.RESET_ALL
		else:
			return Fore.BLUE + Style.BRIGHT +'<OntoSPy>: ' + Style.RESET_ALL

	def _clear_screen(self):
		""" http://stackoverflow.com/questions/18937058/python-clear-screen-in-shell """
		if platform.system() == "Windows":
			tmp = os.system('cls') #for window
		else:
			tmp = os.system('clear') #for Linux
		return True



	def _print_entity_intro(self, g=None, entity=None, first_time=True):
		"""after a selection, prints on screen basic info about onto or entity, plus change prompt """
		if entity:
			# self._clear_screen()
			print Fore.RED + Style.BRIGHT + entity.uri + Style.RESET_ALL
			print Style.DIM + entity.bestDescription() + Style.RESET_ALL
			entity.printStats()
			if first_time:
				self.prompt = self._get_prompt(entity=self.currentEntity['name'])
		elif g:
			if first_time:
				self._clear_screen()
				playSound(ontospy.ONTOSPY_SOUNDS)  # new..
				print "Loaded ", self.current['fullpath']
			g.printStats()
			for o in g.ontologies:
				print Fore.RED + Style.BRIGHT + o.uri + Style.RESET_ALL
				print Style.DIM + o.bestDescription() + Style.RESET_ALL
			if first_time:
				self.prompt = self._get_prompt(self.current['file'])



	def _selectFromList(self, _list):
		"""
		Generic method that lets users pick an item from a list via raw_input
		Note: the list items need to be OntoSPy entities.
		"""
		if len(_list) == 1: # if by any chance there's no need to select a choice
			return _list[0]
		print "%d matching results: " % len(_list)
		counter = 1
		for el in _list:
			if hasattr(el, 'uri'):
				print Fore.BLUE + Style.BRIGHT + "[%d] " % counter, Style.RESET_ALL, el.uri
			else:
				print Fore.BLUE + Style.BRIGHT + "[%d] " % counter, Style.RESET_ALL, el
			counter += 1
		print "--------------"
		var = raw_input(Fore.BLUE + Style.BRIGHT + "Please select one entity: " + Style.RESET_ALL)
		try:
			var = int(var)
			return _list[var-1]
		except:
			print "Selection not valid"
			return None



	# MAIN METHODS
	# --------


	def _list_ontologies(self):
		counter = 0
		for file in self.ontologies:
			counter += 1
			print Fore.BLUE + Style.BRIGHT + "[%d]" % counter,	Fore.RED, file, Style.RESET_ALL



	def _select_ontology(self, line):
		# if
		try:
			var = int(line)	 # it's a string
			if var in range(1, len(self.ontologies)+1):
				self._load_ontology(self.ontologies[var-1])
		except ValueError:
			out = []
			for each in self.ontologies:
				if line in each:
					out += [each]
			choice = self._selectFromList(out)
			if choice:
				self._load_ontology(choice)



	def _load_ontology(self, filename):
		""" loads an ontology from the local repository 
			note: if the ontology does not have a cached version, it is created
		"""
		fullpath = self.LOCAL_MODELS + "/" + filename
		g = ontospy.get_pickled_ontology(filename)
		if not g:
			g = ontospy.do_pickle_ontology(filename)
		self.current = {'file' : filename, 'fullpath' : fullpath, 'graph': g}
		self.currentEntity = None
		self._print_entity_intro(g)



	def _select_class(self, line):			
		# try to match a class and load it
		g = self.current['graph']
		if line.isdigit():
			line =	int(line)
		out = g.getClass(line)
		if out:
			if type(out) == type([]):
				choice = self._selectFromList(out)
				if choice:
					self.currentEntity = {'name' : choice.locale or choice.uri, 'object' : choice}				
			else:
				self.currentEntity = {'name' : out.locale or out.uri, 'object' : out}				
			# ..finally:
			if self.currentEntity:
				self._print_entity_intro(entity=self.currentEntity['object'])
				
				# self.prompt = self._get_prompt(entity=self.currentEntity['name'])
		else:
			print "not found"


	def _select_property(self, line):			
		# try to match a class and load it
		g = self.current['graph']
		if line.isdigit():
			line =	int(line)
		out = g.getProperty(line)
		if out:
			if type(out) == type([]):
				choice = self._selectFromList(out)
				if choice:
					self.currentEntity = {'name' : choice.locale or choice.uri, 'object' : choice}	

			else:
				self.currentEntity = {'name' : out.locale or out.uri, 'object' : out}	
			
			# ..finally:
			if self.currentEntity:
				self._print_entity_intro(entity=self.currentEntity['object'])	
		else:
			print "not found"
			

	def _select_concept(self, line):
		# try to match a class and load it
		g = self.current['graph']
		if line.isdigit():
			line =	int(line)
		out = g.getSkosConcept(line)
		if out:
			if type(out) == type([]):
				choice = self._selectFromList(out)
				if choice:
					self.currentEntity = {'name' : choice.locale or choice.uri, 'object' : choice}
			else:
				self.currentEntity = {'name' : out.locale or out.uri, 'object' : out}
			# ..finally:
			if self.currentEntity:
				self._print_entity_intro(entity=self.currentEntity['object'])

		else:
			print "not found"




	# COMMANDS
	# --------
	# NOTE: all commands should start with 'do_' and must pass 'line'

		
	def do_current(self, line):
		""" List the ontology currently loaded""" 
		 # {'file' : filename, 'fullpath' : fullpath, 'graph': g}
		if self.current:
			print self.current['file']
		else:
			print "No ontology loaded. Use the 'ontology' command"

	def do_currentEntity(self, line):
		""" List the entity currently loaded""" 
		 # {'file' : filename, 'fullpath' : fullpath, 'graph': g}
		if self.currentEntity:
			print self.currentEntity['name']
		else:
			print "No entity loaded. Use the 'class' or 'property' command"



	def do_triples(self, line):
		"""Print out the triples that have the current entity as subject""" 
		# print "If no ontology > no triples \n if ontology = show annotations \n if entity = show triples"
		if self.currentEntity:
			self.currentEntity['object'].printTriples()
		elif self.current:
			g = self.current['graph']		
			for o in g.ontologies:
				o.printTriples()		
		else:
			print "Please select an ontology first."
			
			
	def do_serialize(self, line):
		"""Serialize current entity into an RDF format.\nValid options: xml | n3 | turtle | nt | pretty-xml
		""" 
		# print "If no ontology > no triples \n if ontology = show annotations \n if entity = show triples"
		if line not in ['xml', 'n3', 'turtle', 'nt', 'pretty-xml']:
			line = "turtle"
		if self.currentEntity:
			self.currentEntity['object'].printSerialize(line)
		elif self.current:
			g = self.current['graph']		
			for o in g.ontologies:
				o.printSerialize(line)		
		else:
			print "Please select an ontology first."
	
				
	def do_tree(self, line):
		"""Shows the subsumtion tree of an ontology.\nOptions: [classes | properties]\nDefault: classes"""
		if not self.current:
			print "Please select an ontology first"
		elif line and line == "properties":
			g = self.current['graph']
			g.printPropertyTree(showids=True, labels=False)
		elif line and line == "concepts":
			g = self.current['graph']
			g.printSkosTree(showids=True, labels=False)
		else: # self.current exists
			g = self.current['graph']
			g.printClassTree(showids=True, labels=False)	
						
			
	def do_ontology(self, line):
		"""Select an ontology""" 
		
		if not self.ontologies:
			print "No ontologies in the local repository. Use the 'import' command. "
		else:
			if line:
				self._select_ontology(line)
			else:
				print "Please select an ontology"
				self._list_ontologies()
				
	def do_class(self, line):
		"""Select a class""" 
		if not self.current:	
			print "Please select an ontology first"
		elif line:
			self._select_class(line)
		else:
			print "Enter a class name or number, or type 'class <space><tab>' for suggestions"

	def do_property(self, line):
		"""Select a property""" 
		if not self.current:	
			print "Please select an ontology first"
		elif line:
			self._select_property(line)
		else:
			print "Enter a class name or number, or type 'property <space><tab>' for suggestions"

	def do_concept(self, line):
		"""Select a SKOS concept"""
		if not self.current:
			print "Please select an ontology first"
		elif line:
			self._select_concept(line)
		else:
			print "Enter a SKOS concept name or number, or type 'concept <space><tab>' for suggestions"

	def do_annotations(self, line):
		"Show annotations for current ontology"
		if not self.current:
			print "No ontology loaded"
		else:
			g = self.current['graph']
			for o in g.ontologies:
				o.printTriples()

	def do_summary(self, line):
		"Print a summary of the currently active entity"
		if self.currentEntity:
			self._print_entity_intro(entity=self.currentEntity['object'], first_time=False)
		elif self.current:
			self._print_entity_intro(g=self.current['graph'], first_time=False)
		else:
			print "Please select an ontology first"




	def do_delete(self, line):
		""" Delete an ontology from the local repository. """
		if not line:
			print "Please specify an ontology name"
		else:
			fullpath = self.LOCAL_MODELS + "/" + line
			if os.path.exists(fullpath):
				var = raw_input("Are you sure? (y/n)")
				if var == "y":
					os.remove(fullpath)
					# @todo: do this operation in /cache...
					if os.path.exists(fullpath + ".pickle"):
						os.remove(fullpath + ".pickle")
					self.ontologies = ontospy.get_localontologies()
					print "Deleted %s" % fullpath
			else:
				print "Not found"


	def do_top(self, line):
		"Unload any ontology and go back to top level"
		if self.currentEntity:
			self.currentEntity = None
			self.prompt = self._get_prompt(self.current['file'])
		else:
			self.current = None
			self.prompt = self._get_prompt()

	def do_quit(self, line):
		"Exit OntoSPy shell"
		return True


	def do_inspiration(self, line):
		_quote = random.choice(QUOTES)
		# print _quote['source']
		print Style.DIM + unicode(_quote['text'])
		print Style.BRIGHT + unicode(_quote['source']) + Style.RESET_ALL


	def default(self, line):
		"default message when a command is not recognized"
		foo = ["Wow first time I hear that", "That looks like the wrong command", "Are you sure you mean that? try 'help' for some suggestions"]
		print(random.choice(foo))



	# AUTOCOMPLETE METHODS
	# --------


	def complete_tree(self, text, line, begidx, endidx):
		"""completion for tree command"""
		
		options = ['classes', 'properties', 'concepts']

		if not text:
			completions = options
		else:
			completions = [ f
							for f in options
							if f.startswith(text)
							]
		return completions	


	def complete_serialize(self, text, line, begidx, endidx):
		"""completion for tree command"""
		
		options = ['xml', 'n3', 'turtle', 'nt', 'pretty-xml']

		if not text:
			completions = options
		else:
			completions = [ f
							for f in options
							if f.startswith(text)
							]
		return completions	
				
		
	def complete_ontology(self, text, line, begidx, endidx):
		"""completion for select command"""
		
		options = self.ontologies[:]

		if not text:
			completions = options
		else:
			completions = [ f
							for f in options
							if f.startswith(text)
							]
		return completions						
			
	
	def complete_class(self, text, line, begidx, endidx):
		"""completion for select command"""
		
		if self.current:
			g = self.current['graph']
			options = [x.locale for x in g.classes]
		else:
			options = []

		if not text:
			completions = options
		else:
			completions = [ f
							for f in options
							if f.startswith(text)
							]
		return completions		


	def complete_property(self, text, line, begidx, endidx):
		"""completion for select command"""
		
		if self.current:
			g = self.current['graph']
			options = [x.locale for x in g.properties]
		else:
			options = []

		if not text:
			completions = options
		else:
			completions = [ f
							for f in options
							if f.startswith(text)
							]
		return completions	



	def complete_concept(self, text, line, begidx, endidx):
		"""completion for select command"""

		if self.current:
			g = self.current['graph']
			options = [x.locale for x in g.skosConcepts]
		else:
			options = []

		if not text:
			completions = options
		else:
			completions = [ f
							for f in options
							if f.startswith(text)
							]
		return completions
				

	def complete_delete(self, text, line, begidx, endidx):
		if not text:
			completions = self.ontologies[:]
		else:
			completions = [ f
							for f in self.ontologies
							if f.startswith(text)
							]
		return completions
							


if __name__ == '__main__':
	Shell().cmdloop()