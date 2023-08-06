from itertools import product, takewhile, combinations
import pandas as pd
import numpy as np
from collections.abc import Iterable
import networkx as nx
from Bio import Phylo
from io import StringIO

__forbidden_attributes_phylo= ['_color', 'clades']


#> Define some functions
########################

# Para árboles

def get_dad(tree, n):
    in_edgs= list(tree.in_edges(n))
    if len(in_edgs)==0:
        if n in tree:
            raise ValueError('Node "{}" has no dad'.format(n))
        else:
            raise ValueError('Node "{}" not in tree'.format(n))
    return in_edgs[0][0]

def get_path(tree, x0, x1):
    P= [x1]
    while( x1 != x0 ):
        x1= get_dad(tree, x1)
        P+= [x1]
    return P[::-1]

def are_the_same(X):
    x0= X[0]
    F= lambda x: x==x0
    return all(map(F, X))

def LCA(tree, nodes):
    P= [get_path(tree, tree.root, n) for n in nodes]
    L= min(map(len, P))
    P= [X[:L] for X in P]
    M= len(nodes)
    #X= list( takewhile(lambda x: are_the_same(P[:,x]) , range(L)) )[-1]    
    X= list( takewhile(lambda x: are_the_same( [P[i][x] for i in range(M)] ) , range(L)) )[-1]    
    return P[0][X]

def LCA_color(tree, colors, color_attr= 'color'):
    nodes= {x for x in tree if tree.nodes[x][color_attr] in colors}
    return LCA(tree, nodes)

def induced_leafs(tree, n):
    Q= [n]
    L= []
    while len(Q) > 0:
        n= Q.pop()
        sons= list(tree[n])
        if len(sons) == 0:
            L+= [n]
        else:
            Q+= sons
    return L

def get_inner_nodes(tree):
    return set(tree) - set(induced_leafs(tree, tree.root))

def is_leaf(tree, node):
    return len(tree[node]) == 0

def get_color2leafs(tree, color_attr= 'color'):
    leafs= induced_leafs(tree, tree.root)
    colors= set((tree.nodes[leaf][color_attr] for leaf in leafs))
    color_2_leaf= {color:set() for color in colors}
    for leaf in leafs:
        color_2_leaf[ tree.nodes[leaf][color_attr] ].add(leaf)
    return color_2_leaf

def get_symbolic_relations(T, sym, nAttr):
    edges= []
    for node in T:
        if T.nodes[node][nAttr]==sym:
            for x0,x1 in combinations(T[node], 2):
                edges+= list(product(induced_leafs(T, x0),
                                     induced_leafs(T, x1)
                                    ))
    return edges

def copy_tree(tree):
    root= tree.root
    tree= tree.copy()
    tree.root= root
    return tree

# Leafs overlap | Andrea
def are_overlapping(set_list):
    ret= False
    for s0,s1 in combinations(set_list, 2):
        if not s0.isdisjoint(s1):
            ret= True
            break
    return ret

def leafs_overlap(tree, node):
    if not is_leaf(tree, node):
        return are_overlapping([induced_colors(tree, child)
                                for child in tree[node]])
    else:
        raise ValueError(f'leafs overlap not defined for a leaf ({node})')


def assign_symbolic_date(tree):
    for node in tree:#BFS_graph(tree, tree.root):
        if not is_leaf(tree, node):
            if leafs_overlap(tree, node):
                tree.nodes[node]['color']= 'D'
            else:
                tree.nodes[node]['color']= 'S'

# Pasar a otros tipos de datos

def get_newick(T):
    newick= {}
    for node in nx.dfs_postorder_nodes(T):
        if len(T[node])==0 :
            newick[ node ]= 'spec' + node#nxTree.nodes[node]['label']
        else:
#            newick[ node ]= '(' + ','.join([ newick[son] for son in T[node] ]) + '){}'.format(node)
            newick[ node ]= '(' + ','.join([ newick[son] for son in T[node] ]) + ')'
#    return newick[node][1:-1]+';'
    return newick[node]+';'

def __getNAme(node, idx, tree, label):
    attributes= {a:b for a,b in node.__dict__.items()
                 if b != None
                 and a not in __forbidden_attributes_phylo
                }
    n_label= attributes.get(label, None)
    if n_label==None:
        return idx, attributes
    if n_label in tree:
        raise ValueError('The label "{}" is not unique for every node'.format(n_label))
    return n_label, attributes

def nxTree_from_newick(newick, label= 'name'):
    """
    Transforma biopython.Phylo.Tree.to_networkx() a un objeto de networkx.Digraph sin ningun elemento de biopython
    label es el nombre del nodo que tendrá en el grafo, debe ser un atributo de los nodos clados del phylo tree
    Si el valor de dicho atributo es None, entonces el label es un número entero.
    El label debe ser único para todos los nodos.
    """
    bio_tree= Phylo.read(StringIO(newick), "newick")
    bionx_tree= Phylo.to_networkx(bio_tree)
    bionx_tree.root= bio_tree.root

    nxNodes= BFS_graph(bionx_tree, bionx_tree.root)
    tree= nx.DiGraph()
    node_2_idx= {}
    for idx, node in enumerate(nxNodes):
        node_new, attributes= __getNAme(node, idx, tree, label)
        if 'name' in attributes:
            attributes['nName']= attributes['name']
            del attributes['name']
        else:
            attributes['nName']= node_new
        tree.add_node(node_new, **attributes)
        node_2_idx[node]= node_new

    L= []
    for x0 in nxNodes:
        n0= node_2_idx[x0]
        L+= [x0]
        for x1 in bionx_tree[x0]:
            if x1 not in L:
                n1= node_2_idx[x1]
                w= bionx_tree[x0][x1]['weight']
                tree.add_edge(n0, n1, weight= w)

    tree.root= node_2_idx[ bio_tree.root ]

    return tree

def make_directed(X):
    """
    Transforma un árbol con estrucutura de dato nx.Graph  a un objeto de networkx.Digraph sin ningun elemento de biopython
    """
    tree= nx.DiGraph()
    L= []
    for x0 in BFS_graph(X.nx_tree, X.bio_tree.root):
        L+= [x0]
        for x1 in X.nx_tree[x0]:
            if x1 not in L:
                w= X.nx_tree[x0][x1]['weight']
                tree.add_edge(x0, x1, weight= w)

    tree.root= X.bio_tree.root
    return tree


# Recorridos

def BFS_graph(tree, root):
    """
    Returns a list of nodes visited in a BFS travel

    tree: nx.Graph
    root: node in nx.Graph.nodes
    """
    Q= [root]
    L= []
    while len(Q) > 0:
        x= Q.pop(0)
        L+= [x]
        Q+= [neighbor for neighbor in tree[x]
             if neighbor not in L]
    return L

# auxiliares

def is_superColor(color):
    return isinstance(color, Iterable) and not type(color)==str

def correct_colors(tree):
    for n in tree:
        colorts= tree.nodes[n]['color']
        #if( type(colorts)==list ):
        #if isinstance(colorts, Iterable) :
        if is_superColor(colorts):
            tree.nodes[n]['color']= list(map(str, colorts))
        else:
            tree.nodes[n]['color']= str(colorts)
    tree.root= '0'
    return tree

def induced_colors(tree, node, color_attr= 'color'):  # Andrea aquí :3
    sLeafs= set()
    for x in induced_leafs(tree, node):
        xcol= tree.nodes[x][color_attr]
        if is_superColor(xcol):
            sLeafs.update(xcol)
        else:
            sLeafs.add(xcol)
    return sLeafs


