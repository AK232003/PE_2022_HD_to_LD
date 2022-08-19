import time
import math
import psutil

print("Enter maximum value of the element of vector:", end = ' ')
n = int(input()) #max no of value in T1, T2, T3

print("Enter the dimension of vector:", end = ' ')
d = int(input())

start = time.time()
###################################################

# l1 = []
# l = []
# z = 0
# for i in range(d*n+1):
#     for z in range(n+1):
#         for y in range(n+1):
#             for x in range(n+1):
#                 if (x+y+z)==i :
#                     l1.append([x,y,z])
#     l.append(l1)
#     l1 = []
# print(l)

# max1 = int(input("Enter max Value: "))
# dim = int(input("Enter Dimension: "))

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
    for i in a:
        T.append(list(i))
    T.reverse()
    l.append(T)

# ###################################################

# l = [[[0, 0, 0]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[2, 0, 0], [1, 1, 0], [0, 2, 0], [1, 0, 1], [0, 1, 1], [0, 0, 2]], [[2, 1, 0], [1, 2, 0], [2, 0, 1], [1, 1, 1], [0, 2, 1], [1, 0, 2], [0, 1, 2]], [[2, 2, 0], [2, 1, 1], [1, 2, 1], [2, 0, 2], [1, 1, 2], [0, 2, 2]], [[2, 2, 1], [2, 1, 2], [1, 2, 2]], [[2, 2, 2]]]
out = [[[0,0,l[0][0]]]] #base cases

len1 = len(l[1])
x1=0
y1=1
tempo = []
r = 1/(len1-1)
for i in l[1]:
    x1+=r
    y1-=r
    tempo.append([x1,y1,i])
out.append(tempo)


def fn(c):
    if(c<((d*n)/2)): out.append([[c,0,l[c][-1]], [0,c,l[c][0]]])
    else: out.append([[(d*n)/2,(c-(d*n)/2),l[c][-1]], [(c-(d*n)/2),(d*n)/2,l[c][0]]]) 
    # print(c)
    temp = len(l[c])
    l[c].remove(l[c][-1])
    l[c].remove(l[c][0])
    if(c<=((d*n)/2)):
        x = 0
        y = c
    else:
        x = c-((d*n)/2)
        y = ((d*n)/2) 
    # print(l[c])
    count = 1
    change = 0
    if(c%2==0): change+=(temp/2)
    else: change+=((temp+1)/2)
    while(len(l[c]) and (count<=change)):
        p1 = out[c][1][2]
        p2 = out[c-1][1][2]
        p3 = out[c-1][2][2]
        r = (math.dist([out[c][0][0], out[c][0][1]], [out[c][1][0], out[c][1][1]])/(math.sqrt(2)))/(temp-1)
        #print(r,c, temp, math.dist([out[c][0][0], out[c][0][1]], [out[c][1][0], out[c][1][1]])/(math.sqrt(2)), [out[c][0][0], out[c][0][1]], [out[c][1][0], out[c][1][1]])
        # print(l[c][0], p1)
        dis = math.dist(l[c][0], p1)
        temp1 = [l[c][0]]
        for i in l[c]:
            if(dis > math.dist(i, p1)):
                dis = math.dist(i, p1)
                temp1.clear()
                temp1.append(i)
            elif( dis == math.dist(i, p1) and i != temp1[0]):
                temp1.append(i)
        if(len(temp1) > 1):
            temp2 = [temp1[0]]
            print(p2, temp1[0])
            dis1 = math.dist(temp1[0], p2)
            for i in temp1:
                if(dis1 > math.dist(i, p2)):
                    dis1 = math.dist(i, p2)
                    temp2.clear()
                    temp2.append(i)
                elif(dis == math.dist(i, p1) and i != temp2[0]):
                    temp2.append(i)
            if(len(temp2)>1):
                temp3 = [temp2[0]]
                dis2 = math.dist(temp2[0], p3)
                for i in temp2:
                    if(dis2 > math.dist(i, p3)):
                        dis2 = math.dist(i, p3)
                        temp3.clear()
                        temp3.append(i)
                    elif(dis == math.dist(i, p1) and i != temp3[0]):
                        temp3.append(i)
                # print("This:", temp3[0])
                if(len(temp3)==1):
                    x = x+r
                    y = y-r
                    out[c].append([x,y,temp3[0]])
                    l[c].remove(temp3[0])
                    count+=1
                elif(len(temp3)>1):
                    while(len(temp3)):
                        x = x+r
                        y = y-r
                        out[c].append([x,y,temp3[0]])
                        # print(temp3[0])
                        l[c].remove(temp3[0])
                        temp3.remove(temp3[0])
                        count+=1
            elif(len(temp2)==1):
                x = x+r
                y = y-r
                out[c].append([x,y,temp2[0]])
                l[c].remove(temp2[0])
                count+=1
        elif(len(temp1)==1):
            x = x+r
            y = y-r
            out[c].append([x,y,temp1[0]])
            l[c].remove(temp1[0])
            count+=1
        # pint(y+r)
    while(len(l[c])):
        p1 = out[c][0][2]
        p2 = out[c-1][0][2]
        p3 = out[c-1][2][2]
        r = (math.dist([out[c][0][0], out[c][0][1]], [out[c][1][0], out[c][1][1]])/(math.sqrt(2)))/(temp-1)
        # print(p1, p2, p3)
        # print(l[c][0], p1)
        dis = math.dist(l[c][0], p1)
        temp1 = [l[c][0]]
        for i in l[c]:
            if(dis > math.dist(i, p1)):
                dis = math.dist(i, p1)
                temp1.clear()
                temp1.append(i)
            elif( dis == math.dist(i, p1) and i != temp1[0]):
                temp1.append(i)
        if(len(temp1) > 1):
            temp2 = [temp1[0]]
            dis1 = math.dist(temp1[0], p2)
            for i in temp1:
                if(dis1 > math.dist(i, p2)):
                    dis1 = math.dist(i, p2)
                    temp2.clear()
                    temp2.append(i)
                elif(dis == math.dist(i, p1) and i != temp2[0]):
                    temp2.append(i)
            if(len(temp2)>1):
                temp3 = [temp2[0]]
                dis2 = math.dist(temp2[0], p3)
                for i in temp2:
                    if(dis2 > math.dist(i, p3)):
                        dis2 = math.dist(i, p3)
                        temp3.clear()
                        temp3.append(i)
                    elif(dis == math.dist(i, p1) and i != temp3[0]):
                        temp3.append(i)
                # print("This:", temp3[0])
                if(len(temp3)==1):
                    x = x+r
                    y = y-r
                    out[c].append([x,y,temp3[0]])
                    l[c].remove(temp3[0])
                    # count+=1
                elif(len(temp3)>1):
                    while(len(temp3)):
                        x = x+r
                        y = y-r
                        out[c].append([x,y,temp3[0]])
                        # print(temp3[0])
                        l[c].remove(temp3[0])
                        temp3.remove(temp3[0])
                        # count+=1
            elif(len(temp2)==1):
                x = x+r
                y = y-r
                out[c].append([x,y,temp2[0]])
                l[c].remove(temp2[0])
                # count+=1
        elif(len(temp1)==1):
            x = x+r
            y = y-r
            out[c].append([x,y,temp1[0]])
            l[c].remove(temp1[0])
            # count+=1

for i in range(2, d*n):
    fn(i)
out.append([[(d*n)/2, (d*n)/2, [n for i in range(d)]]])
for i in out:
    for j in i:
        l1 = j[2]
        coords = [j[0],j[1]]
        print(str(l1)+": "+str(coords))

end = time.time()
print("Time Elapsed(CPU): ", time.process_time())
print("Time Elapsed(to run script): ", end-start)
print('RAM memory used:', psutil.virtual_memory()[3]/(1024**2))