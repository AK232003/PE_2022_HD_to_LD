import numpy as np
import math

n = int(input()) #max no of value in T1, T2, T3

def Sum(l):
    sum1=0
    for i in l: sum1+=i

    return sum1

# inp = np.zeros([(n+1)**3,3], dtype='int') #populating list with [0, 0, 0]...
###################################################

# l = []

# for i in range(3*n+1):
#     for x in range(n+1):
#         for y in range(n+1):
#             for z in range(n+1):
#                 if (x+y+z)==i :
#                     l.append([x,y,z])
# print(l)

###################################################

l = [[0, 0, 0], [[0, 0, 1], [0, 1, 0], [1, 0, 0]], [[0, 0, 2], [0, 1, 1], [0, 2, 0], [1, 0, 1], [1, 1, 0], [2, 0, 0]]]#, [0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 1, 1], [1, 2, 0], [2, 0, 1], [2, 1, 0], [0, 2, 2], [1, 1, 2], [1, 2, 1], [2, 0, 2], [2, 1, 1], [2, 2, 0], [1, 2, 2], [2, 1, 2], [2, 2, 1], [2, 2, 2]]
out = [[0,0,[0,0,0]],[[1,0,[0,0,1]], [0,1,[1,0,0]], [0.5, 0.5,[0,1,0]]]]
out.append([[2,0,[0,0,2]], [0,2,[2,0,0]]])
temp = len(l[2])
l[2].remove([0,0,2])
l[2].remove([2,0,0])
x = 0
y = 2
# print(l[2])
while(len(l[2])):
    p2 = out[1][1][2]
    p1 = out[2][1][2]
    p3 = out[1][2][2]
    r = 2/(temp-1)
    # print(l[2][0], p1)
    dis = math.dist(l[2][0], p1)
    temp1 = [l[2][0]]
    for i in l[2]:
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
            print("This:", temp3[0])
            if(len(temp3)==1):
                x = x+r
                y = y-r
                out[2].append([x,y,temp3[0]])
                l[2].remove(temp3[0])
            elif(len(temp3)>1):
                while(len(temp3)):
                    x = x+r
                    y = y-r
                    out[2].append([x,y,temp3[0]])
                    print(temp3[0])
                    l[2].remove(temp3[0])
                    temp3.remove(temp3[0])
        elif(len(temp2)==1):
            x = x+r
            y = y-r
            out[2].append([x,y,temp2[0]])
            l[2].remove(temp2[0])
    elif(len(temp1)==1):
        x = x+r
        y = y-r
        out[2].append([x,y,temp1[0]])
        l[2].remove(temp1[0])
print(out)        