import numpy as np
from sklearn.ensemble import RandomForestClassifier
import sys
import array as arr
#A1 = np.array([
#    [0, 1, 1, 0, 1],
#    [0, 0, 1, 1, 1],
#    [1, 1, 1, 1, 1],
#], dtype=bool)
(0, 1, 1, 0, 1,1,0,1,1,1)
a2=((0, 1, 1, 0, 1,1,0,1,1,1,0, 1, 1, 0, 1,1,0,1,1,1,0, 1, 1, 0, 1,1,0,1,1,1,0, 1, 1, 0, 1,1,0,1),(0, 1, 1, 0, 1,1,0,1,1,1,0, 1, 1, 0, 1,1,0,1,1,1,0, 1, 1, 0, 1,1,0,1,1,1,0, 1, 1, 0, 1,1,0,1))
a2=[[0, 1, 1, 0, 1,1,0,1,1,1,0, 1, 1, 0, 1,1,0,1,1,1,0, 1, 1, 0, 1,1,0,1,1,1,0, 1, 1, 0, 1,1,0,1],[0, 1, 1, 0, 1,1,0,1,1,1,0, 1, 1, 0, 1,1,0,1,1,1,0, 1, 1, 0, 1,1,0,1,1,1,0, 1, 1, 0, 1,1,0,1]]
#print(a2[:,:-1])
A6=[0, 1, 1, 0, 1,1,0,1,1,1,0, 1, 1, 0, 1,1,0,1,1,1,0, 1, 1, 0, 1,1,0,1,1,1,0, 1, 1, 0, 1,1,0,1]
A1 = np.array([
    [0, 1, 1, 0, 1,1,0,1,1,1],[0, 1, 1, 0, 1,1,0,1,1,1]
], dtype=np.int8)
#print(sys.getsizeof(A6))
#print(sys.getsizeof(A1))
#print(sys.getsizeof(a2))


A1 = np.array([
    [0, 1, 1, 0, 1,1,0,1,1,1],[0, 1, 1, 0, 1,1,0,1,1,1]
], dtype=np.int8)
A5 = np.array([
    [0, 1, 1, 0, 1,1,0,1,1,1]
], dtype=np.int8)



Features1=[[2.2,4.4,4.4,2.2],[2.2,4.4,4.4,2.2],[2.2,4.4,4.4,2.2],[2.2,4.4,4.4,2.2],[2.2,4.4,4.4,2.2],[2.2,4.4,4.4,2.2],[2.2,4.4,4.4,2.2]]
Features2=[[22,44,44,22],[22,44,44,22],[22,44,44,22],[22,44,44,22],[22,44,44,22],[22,44,44,22],[22,44,44,22]]
for each in Features1:
    for ele in each:
        print(sys.getsizeof(ele))
for each in Features2:
    for ele in each:
        print(sys.getsizeof(ele))

#print(Features.itemsize() )

labels=arr.array('d', [1,1,0,1,1,1,0])
#print(labels.itemsize() )

print(sys.getsizeof(Features1))
print(sys.getsizeof(Features2))

print(sys.getsizeof(labels))

#labels=labels.astype('int') 
clf = RandomForestClassifier(n_estimators = 100)

clf.fit(Features1,labels)
