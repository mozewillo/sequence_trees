# -*- coding: utf-8 -*-
########################
#  Phylogenetic Trees  #
########################


class PhylNode:

    def __init__(self, distance = None, ch=[]):
    	self.children = ch
        self.distance = distance

    def get_children(self):
        ch=[]
        for i in self.children:
            ch.append(str(i))
        return ch

    def get_distance(self):
    	return self.distance

    def set_distance(self, distance):
    	self.distance = distance

    def __call__(self):
        ch="["
        if len(self.children) != 0:
            for c in self.children:
                ch += c.__str__() + ", "
        	ch= ch[: len(ch)-2]
        ch+="]"
        return "PhylNode = (" + str(self.distance) + ", " + ch +")"

    def __str__(self):
        ch="["
        if len(self.get_children())!= 0:
            for c in self.children:
                ch += c.__str__() + ", "
            ch= ch[: len(ch)-2]
        ch+="]"
        return "PhylNode = (" + str(self.distance) + ", " + ch +")"

    def max_leaf(self, maxi = 0, a = 0):
    	a += self.distance
    	if len(self.children) != 0:
    		for i in self.children:
    			maxi = i.max_leaf(maxi, a)
    		a -= self.distance
    		return maxi
    	else:
    		if a > maxi:
    			maxi= a
    		a -= self.distance
    		return maxi

    def min_leaf(self, mini=float("inf") , a=0):
    	a += self.distance
    	if len(self.children) != 0:
    		for i in self.children:
    			mini = i.min_leaf(mini, a)
    		a-=self.distance
    		return mini
    	else:
    		if mini > a:
    			mini = a
    		a -= self.distance
    		return mini

    def truncate(self, mini):
        if len(self.children) != 0:
        	h= mini - min( self.sum_path(self.distance, paths = []))
        	if h<0: h=0
        	self.set_distance(h)
        	for ch in self.children:
        		ch.truncate(mini)
        else:
        	self.set_distance(mini)

    def elongate( self, maxi ):
    	if len(self.children) != 0:
    		print maxi
    		h = maxi - max( self.sum_path(self.distance, paths = []))
    		if h > self.distance:
    			self.set_distance(h)
    		maxi -= self.distance
    		if maxi != 0:
    			for ch in self.children:
    				ch.elongate(maxi)
    		maxi+= self.distance
    	else:
    		self.set_distance(maxi)

    def unify(self, avrg):
        if len(self.children) != 0:
            x = self.sum_path(0, 0, paths=[])
            a = self.distance + avrg - float(sum(x)) / len(x)
            a= max(a, 0)
            self.set_distance(a)
            avrg -= self.get_distance()
            for ch in self.children:
                ch.unify(avrg)
            avrg+=self.distance
        else:
            self.set_distance(avrg)

    def sum_path(self, info= 0, dist = 0, paths = []):
    	dist += self.distance
        if len(self.children) != 0:
            for ch in self.children:
                paths=ch.sum_path(info, dist, paths)
            dist-=self.distance
        else:
            paths.append(dist - info)
        return paths



class PhylTree:
    def __init__(self, node=None):
        self.root = node

    def get_children(self):
    	ch=[]
    	if self.root!=None:
    		ch=self.root.get_children()
    	return ch
    
    def root(self):
        return self.root

    def max_leaf_distance(self):
        if self.root!=None:
            return self.root.max_leaf() - self.root.distance

    def __str__(self):
        tree = "PhylTree= ("
        if self.root != None:
            tree += str(self.root())
        tree += ")"
        return tree

    def __call__(self):
        tree = "PhylTree= ("
        if self.root != None:
            tree += self.root()
        tree += ")"
        return tree

    def min_leaf_distance(self):
		if self.root!=None:
			return self.root.min_leaf() - self.root.distance

    def elongate_distances(self):
    	if self.root != None:
    		if self.root.children != None:
    			for child in self.root.children:
    				child.elongate(self.max_leaf_distance())

    def truncate_distances(self):
    	ro=self.root.distance
        if self.root != None:
           self.root.truncate(self.min_leaf_distance())
        self.root.set_distance(ro)

    def unify_distances(self):
    	avrg= self.average_leaf_distance()
        if self.root != None:
        	if self.root.children != None:
        		for ch in self.root.children:
        			ch.unify(avrg)

    def average_leaf_distance(self):
        leaf_dist = self.root.sum_path(self.root.distance, paths = [])
        return float(sum(leaf_dist))/ len(leaf_dist)
