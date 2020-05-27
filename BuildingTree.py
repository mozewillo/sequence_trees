# -*- coding: utf-8 -*-

###############
###SEQUENCES###
###############

def EditDistance(seq1, seq2) :
	#determines biological distance of sequences(depending on number of mutations)
	S= [[0 for x in range(len(seq1) + 1)] for y in range(len(seq2) + 1)]
	for j in range(len(seq1) + 1):
		S[0][j] = j
	for i in range(len(seq2) + 1):
		S[i][0] = i
	for i in range(1, len(seq2) + 1):
		for j in range(1, len(seq1) + 1):
			s = (seq1[j - 1] != seq2[i - 1])
			S[i][j] = min ((S[i-1][j-1] + int(s)), S[i][j-1] + 1, S[i-1][j] + 1)
	return S[len(seq2)][len(seq1)]

def BuildTree(sequences, dist_function=EditDistance):
	#function spans a tree depending on editional distances
	#based on Prim's Algorithm for fiding minimum spanning tree
	cost=[]
	#initialize tree with single vertex
	root = sequences.pop()
	source = root
	leaf = 0 
	MST = {}
	MST[source]=[0]
	mkr=PhylNode(0, source)
	memory = []
	# finding minimum-weight edge
	for s in range(len(sequences)):
				if s==0:
					cost.append([dist_function(source, sequences[s])])
				else:
					cost[leaf].append(dist_function(source, sequences[s]))
	for leaf in range(len(sequences)):
		memory.append(source)
		mini = float("inf")
		leaf_initial = 0

 		for i in range(leaf + 1):
 			mloc = min(cost[i])
 			if mloc < mini:
 				mini = mloc #minimal editing distance
 				leaf_initial = cost[i].index(mini)
 				father = i
 		source = sequences[leaf_initial]
 		MST[source] = [mini]
 		for key in MST.keys():
 			if key == memory[father]:
 				MST[key].append(source)
 		#remove used vertex
 		for i in range(leaf + 1):
 			del cost[i][leaf_initial]
 		del sequences[leaf_initial]
 		#update costs
		for s in range(len(sequences)):
			if len(cost) < leaf + 2:
				cost.append([dist_function(source, sequences[s])])
			else:
				cost[leaf + 1].append(dist_function(source, sequences[s]))
	spanTree = PhylTree(grow(MST, root))
 	return spanTree

def grow(MST, root):
	#returns nodes from picked root
	values = MST[root]
	node = PhylNode(values[0], root)
	if len(values) != 1:
		for val in values[1:]:
			node.addChild(grow(MST, val))
	return node


class PhylNode:
	def __init__(self, distance=None, sequence=None, children=None):
		self.distance = distance
		self.sequence = sequence
		self.children = children

	def set_distance(self, distance):
		self.distance = distance

	def set_sequence(self, sequence):
		self.sequence = sequence

	def get_sequence(self):
		return self.sequence

	def get_sequencesNode(self, sequences):
		sequences.append(self.sequence)
		if self.children != None:
			for child in self.children:
				sequences = child.get_sequencesNode(sequences)
		return sequences

	def get_distance(self):
		return self.distance

	def get_children_str(self):
		ch_str = ""
		if self.children != None:
			for child in self.children:
				ch_str+=(child.__str__())
		return ch_str

	def get_children(self):
		if self.children != None:
			return self.children

	def __str__(self):
		return self.toString()

	def __call__(self):
		return self

	def toString(self, i=0):
		ch = ""
		if self.children != None:
			i+=1
			for child in self.children:
				ch += child.toString(i)
			i-=1
		return "\t"*i + "/_" + str(self.get_distance()) + "_" + str(self.get_sequence())+ "\n" + ch

	def sumdistNode(self, suma=0):
		suma+=self.distance
		if self.children != None:
			for child in self.children:
				suma = child.sumdistNode(suma)
		return suma

	def calculate_distancesNode(self, dist_function):
		if self.children != None:
			for child in self.children:
				child.set_distance(dist_function(self.sequence, child.sequence))
				child.calculate_distancesNode(dist_function)

	def addChild(self, child):
		if self.children != None:
			self.children.append(child)
		else:
			self.children = [child]


class PhylTree:
	def __init__(self, node):
		self.root = node

	def root(self):
		return self.root

	def get_sequences(self):
		sequences = []
		if self.root != None:
			sequences.append(self.root.get_sequence())
			for child in self.root.children:
				sequences = child.get_sequencesNode(sequences)
		return sequences

	def __str__(self):
		if self.root != None:
			return self.root.toString()

	def distance_sum(self):
		if self.root!=None:
			return self.root.sumdistNode()

	def calculate_distances(self, dist_function=EditDistance):
		if self.root != None:
			self.root.set_distance(0)
			self.root.calculate_distancesNode(dist_function)

sequences=[]

sequences.append('ACGTAAGCTT')

sequences.append('ATAAAGCCAT')

sequences.append('ATAAGGCCAT')

sequences.append('ACGTAAACCTT')

sequences.append('ATAAGCTT')

sequences.append('ACGTAAAGCGT')

sequences.append('ACGTAAAGCTT')


T = PhylTree(PhylNode(1,sequences[0],
	[PhylNode(1,sequences[1],
		[PhylNode(2,sequences[2]),
		PhylNode(1,sequences[3],[
			PhylNode(1,sequences[4]),]),
		PhylNode(5,sequences[5]),]),
	PhylNode(1,sequences[6]),]))


print T.root()