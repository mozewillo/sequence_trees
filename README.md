# sequence_trees
Both scripts written within the Algorithms and Data Structures course 

SEQUENCE TREES 
SeqTrees implementing the phylogenetic trees object, that allows operations of modyfing the sequence distances.
By distance between any two vertices we mean the sum of the weights of the edges from the path between connecting these vertices.
Avaliable operations on tree:
- find the longes branch
- find the shortes brach
- truncate the branches so all the branches are in equal distance from the root, but none of those distances is elongated in process *
- elongate the branches so all the branches are in equal distance from the root, but none of those distances is shortened in process *

*In some phylogenetic models we expect the leaves to be in the same distance from the root.


BUILDING TREE
The editing distance between two texts is the minimum number of elementary editing operations(substitution, deletion, insertion) needed to transform one text into another. It is used in biology as a measure of evolutionary distance between homologous sequences. In this project we build the phylogenetic tree using the editing distances as a measure. We implemented Prims algorithm to build tree so that the sum of all distances is as small as possible (minimum spanning tree).
