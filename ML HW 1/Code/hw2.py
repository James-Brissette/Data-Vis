# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 17:06:58 2018

@author: James
"""

from data import Data
import numpy as np
DATA_DIR = 'data/'


def listToJSON(tree):
    out = open('ML_Tree.json','w')
    tree.treeToList()
    json = tree.JSON
    json += ']'
    out.write(json.replace('}{','},\n{'))
        
    
    
def loadData(fileName):
    """
	Returns the complete test set into a variable.
	Returns:
		TYPE: numpy.ndarray
	"""
    data = np.loadtxt(DATA_DIR + fileName, delimiter=',', dtype = str)
    print(type(data))
    data_obj = Data(data=data)
    return data_obj
    

def crossValidate(fold,depth):
    
    cv_train = None
    cv_test = np.loadtxt(DATA_DIR + '/CVfolds_new/fold' + str(fold) + '.csv', \
                                                 delimiter=',', dtype = str)
    for i in range(1,5):
        if i == fold:
            continue
        if cv_train is None:
            cv_train = np.loadtxt(DATA_DIR + '/CVfolds/fold' + str(i) + '.csv', \
                                                  delimiter=',', dtype = str)
        else:
            cv_train = np.concatenate((cv_train,np.loadtxt(DATA_DIR + '/CVfolds/fold' \
                         + str(i) + '.csv', delimiter=',', dtype = str)[1:]),0)
    
    train = Data(data=cv_train)
    test = Data(data=cv_test)
    
    tree = Tree(ID3(train, train.attributes,max_depth=depth))
    tree.setDepth
    acc = tree.predict(test)                                                                              
    return acc
        

# @param attribute: Attribute to split on in order to calculate H(dataset)'
def findEntropy(dataset, attribute='label'):
    if attribute == 'label':
        S = dataset.get_column([attribute])
        size = S.size
        prob_p = list(S).count('p') / size
        prob_e = 1 - prob_p
        HS = -prob_p*np.log2(prob_p) - prob_e*np.log2(prob_e)
        return HS
    
    S_A=dataset.get_column([attribute])
    a, counta = np.unique(S_A, return_counts = True)
    attr_counts = dict(zip(a, counta))
    HS_A = 0
    for i in a:
        i_count_p = list(dataset.get_row_subset(attribute, i).get_column('label')).count('p')
        i_prob_p  = i_count_p / attr_counts[i]
        
        if i_prob_p == 1 or i_prob_p == 0:
            continue
        
        i_prob_e  = 1 - i_prob_p
        HS_A += (attr_counts[i]/S_A.size)* \
                (-i_prob_p*np.log2(i_prob_p)-i_prob_e*np.log2(i_prob_e))
        
    return HS_A

# @param attribute: Attribute to split on in order to calculate ME(dataset)'
def findMajorityErr(dataset, attribute='label'):
    if attribute == 'label':
        S = dataset.get_column([attribute])
        size = S.size
        prob_p = list(S).count('p') / size
        prob_e = 1 - prob_p
        ME_S = 1 - max(prob_p,prob_e)
        return ME_S
    
    S_A = dataset.get_column([attribute])
    a, counta = np.unique(S_A, return_counts = True)   
    attr_counts = dict(zip(a, counta))
    ME_SA = 0
    
    for i in a:
        i_count_p = list(dataset.get_row_subset(attribute, i).get_column('label')).count('p')
        i_prob_p  = i_count_p / attr_counts[i]
        
        if i_prob_p == 1 or i_prob_p == 0:
            continue
        
        i_prob_e  = 1 - i_prob_p
        ME_SA += (attr_counts[i]/S_A.size)*(1 - max(i_prob_p,i_prob_e))
        
    return ME_SA 

def ID3(dataset, attributes, method='entropy', current_depth=0, max_depth=100):
#    print('Starting function')
    d = dataset.get_column('label')
    size = d.size
    if list(d).count('p') == 0:
#        print(' |---> labels are all e, returning.')
        return Node('e')
    if list(d).count('p') == size:
#        print(' |---> labels are all p, returning.')
        return Node('p')
    
#   mcl => most_common_label
    mcl = 'p'
    if list(d).count('e')/size > .5:
        mcl ='e'
        
    if current_depth >= max_depth:
        return Node(mcl)
    
    best = {'attribute':'tbd','result':float('inf')}
    i_result = None
    for i in attributes:
        if method == 'majority':
            i_result = findMajorityErr(dataset, i)
        if method == 'entropy':
            i_result = findEntropy(dataset, i)
            
        if i_result < best['result']:
            
            best['attribute'] = str(i)
            best['result'] = i_result
    
    n = Node(best['attribute'])
    
    a = np.unique(dataset.get_column(best['attribute']))  
#    print('best attribute: ' + str(best['attribute']) + ' .. unique values: ' + str(a))
    
    
#    print('Current Level is: ' + str(level) + ' -- Splitting on attribute: ' + str(best['attribute']))
    for i in a:
#        print(i)
        child = Node(i)
        n.push(child)
        child.setParent(n)
    
    for i in n.children:
#        print(i.label)
        Sv = dataset.get_row_subset(best['attribute'],i.label)
        if Sv.get_column('label').size == 0:
#            print(' |---> Shouldnt ever hit this, but ' + i.label +' fell into here')
            return Node(mcl)
        
        att = attributes.copy()
        del att[best['attribute']]
#        print('Recursive call being made on Av = ' + i.label)
        i.push(ID3(Sv, att, method, current_depth + 1,max_depth))  
    
    return n
    
    
    
class Node:
    
    def __init__(self, label='', parentNode = None):
        self.label = label
        self.parentNode = parentNode
        self.children = []
#        self.attributes = {'label':self.label,'parentNode':self.parentNode,'children':self.children}
        
    def setParent(self, parentNode):
        if isinstance(parentNode, Node):
            self.parentNode = parentNode
#            self.attributes['parentNode'] = self.parentNode
            return
        raise TypeError("Parent must be of type 'Node'")
    
    def push(self, child):
#        if isinstance(child, Node):
        self.children.append(child)
#            self.attributes['children'] = self.children
        return
#        raise TypeError("Child must be of type 'Node'")
    
    def setLabel(self, label):
        self.label = label
#        self.attributes['label'] = self.label
    
class Tree:
    
    def __init__(self, root):
        self.root = root
        self.depth = 0        
        self.JSON = ''
    
#   Data can be passed in either as a Data object or ndArray
    def predict(self, data):
        header = np.asarray(list(data.attributes.keys()))
        target = data.get_column('label')
        predictions = np.zeros(target.size, dtype='U24')
        correct_predictions = 0
        if isinstance(data,Data):
            data = data.raw_data
        
        i = 0
        for row in data:
            instance = dict(zip(header,row[1:]))
            predictions[i] = Tree.determineLabel(self, instance, self.root)
            
            if predictions[i] == target[i]:
                correct_predictions += 1
#            print('Prediction: ' + predictions[i] + ' Actual: ' + target[i])
            
            i += 1
            
        print("Prediction accuracy: " + str(correct_predictions / i ) )
#        print("Predictions returned as array")
        return correct_predictions / i
        
    
    def determineLabel(self, data, node):            
        if node.children == []:
            return node.label
        a = node.label
        b = data[a]
        
        for i in node.children:
            if i.label == b:
                p = Tree.determineLabel(self,data,i.children[0])
                return p
                
    def setDepth(self, node, level=0):
        if node.children == []:
            self.depth = max(self.depth, level)
            return self.depth
        
        for c in node.children:
            for d in c.children:
                Tree.setDepth(self, d, level+1)
                
    def treeToList(self, node=None, parent=""):
        if node is None:
            node = self.root
            parent = "root"
            self.JSON = '['
            
        self.JSON += '{"name":"'+ node.label + '","parent":"' + parent + '"}'
        if node.children == []:
            return
        
        for branches in node.children:
            for nodes in branches.children:
                Tree.treeToList(self, nodes,node.label)
            
    
    
data = loadData('train.csv')
t = Tree(ID3(data,data.attributes,max_depth=10))

#for i in [1,2,3,4,5,10,15]:
#    accuracy_arary = np.ones(5)
#    for j in range(5):
#        accuracy_arary[j] = crossValidate(j+1,i)
#    print('Average for depth ' + str(i) + ': ' + str(np.average(accuracy_arary)))
#    print('Std.Dev for depth ' + str(i) + ': ' + str(np.std(accuracy_arary)))
#    print('')
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    