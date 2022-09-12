import csv
import time
import psutil
import os
import shutil

if os.path.exists('./inputs'):
    shutil.rmtree('./inputs')
if os.path.exists('./outputs'):
    shutil.rmtree('./outputs')
os.mkdir("./inputs")
#Enter the max value each dimention in the input can take
#The Range of value each dimention can take then will be [0-max value]
print("Enter maximum value of the element of vector:", end = ' ')
n = int(input()) #max no of value in T1, T2, T3
#Enter the number of dimentions in the vector
print("Enter the dimension of vector:", end = ' ')
d = int(input())
#Hence Number of equavalence class will be equal to d*n+1 and will be {0,1,2,....,d*n+1}
#notes the starting execution time of the program
start = time.time()
#Generates the hd points of all the equivalence classes and stores them in the list l  
def sums(length, total_sum):
    if length == 1:
        yield (total_sum,)
    else:
        for value in range(total_sum + 1):
            for permutation in sums(length - 1, total_sum - value):
                yield (value,) + permutation
l = []
for i in range(0, n*d+1):
    l1 = list(sums(d,i))
    a = []
    for j in l1:
        if(max(j)>n): 
            continue
        else:
            a.append(j)
    T=[]
    for j in a:
        T.append(list(j))
    T.reverse()
    with open('./inputs/{}.csv'.format(i), 'w',newline='') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(["HD Point of equivalence class {}".format(i)])
        for j in T:
            thewriter.writerow([j])

end = time.time()
print("Time Elapsed(CPU): ", time.process_time())
print("Time Elapsed(to run script): ", end-start)
print('RAM memory used:', psutil.virtual_memory()[3]/(1024**2))
