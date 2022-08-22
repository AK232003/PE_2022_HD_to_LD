import time
import math
import psutil
import plotly.express as px
import plotly.graph_objects as go


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
    for i in a:
        T.append(list(i))
    T.reverse()
    l.append(T)
# mapping for equavalence class-0
out = [[[0,0,l[0][0]]]] #base cases

# mapping for equavalence class-1
len1 = len(l[1])
x1=0
y1=1
tempo = []
tempo.append([0,1,l[1][0]])
l[1].remove(l[1][0])
tempo.append([1,0,l[1][-1]])
l[1].remove(l[1][-1])
r = 1/(len1-1)
for i in l[1]:
    x1+=r
    y1-=r
    tempo.append([x1,y1,i])
out.append(tempo)


#will do the mapping for the equivalence class c and will store the ordered points in the the out list  
def fn(c):
    #will add the first and the last hd point to of the equivalence class in the out list
    if(c<((d*n)/2)): out.append([[c,0,l[c][-1]], [0,c,l[c][0]]])
    else: out.append([[(d*n)/2,(c-(d*n)/2),l[c][-1]], [(c-(d*n)/2),(d*n)/2,l[c][0]]]) 
    
    # will store the number of points in the the equivalece class c  
    temp = len(l[c])
    
    # will remove the first and the last points from the list l as we have already done the mapping for them in out
    l[c].remove(l[c][-1])
    l[c].remove(l[c][0])
    
    #the coordinates in the 2d map till which we have already done the mapping is stored in (x,y)
    if(c<=((d*n)/2)):
        x = 0
        y = c
    else:
        x = c-((d*n)/2)
        y = ((d*n)/2) 
    
    #count will store the number of points of the equivalence class that has been already mapped
    count = 1
    
    #change will store the number of points after which we have to reverse the algorithm for the mapping of the remaining point in which we will change the reference point to the last point
    change = 0
    if(c%2==0): change+=(temp/2)
    else: change+=((temp+1)/2)

    #will continue the loop until all the points of the equivalnce class has been mapped
    while(len(l[c]) and (count<=change)):
        #p1,p2,p3 are the reference points which we will use to order the remaining points of the equivalence class
        p1 = out[c][1][2]
        p2 = out[c-1][1][2]
        p3 = out[c-1][2][2]
        #r is the distance between each point of the equivalence class in the 2d map
        r = (math.dist([out[c][0][0], out[c][0][1]], [out[c][1][0], out[c][1][1]])/(math.sqrt(2)))/(temp-1)
        
        #l[c]- the list of remaining points of the equivalence class which are remaining to be mapped
        #will calculate the distance between the first point in l[c] 
        dis = math.dist(l[c][0], p1)
        #temp1 will store the points(1 or more) from l[c] that are closest to p1
        temp1 = [l[c][0]]
        
        for i in l[c]:
            #if we get an even closer point to p1, then we will replace the current min points in temp1 with the new min point
            if(dis > math.dist(i, p1)): 
                dis = math.dist(i, p1)
                temp1.clear()
                temp1.append(i)
            #if the distance of this point from p1 is equal to the distance of the current closest point, then we will add the point to temp1
            elif( dis == math.dist(i, p1) and i != temp1[0]): 
                temp1.append(i)
            #if the distance of this point from p1 is greater thatn the distnace of the current closest point,then we will ignore this point
        
        #Now if in temp1, we have more than one point which have the same min distance to p1 then we will have to resolve those clashes by looking at their distance from p2, and then order them by their distance.The point with the min distance will come first in the ordering and will similarly do this for others.
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
            # if after looking at their distance from p2, their are still points which clash for the min distance then we wiil resolve those clashes by looking at their distance from p3, and then order them by their distance.The point with the min distance will come first in the ordering and will similarly do this for others.
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
                # if the clashes get resolved now, then the number of elements in temp3 will be 1, and hence we can map that point to the next point(x+r,y-r) in the 2d map 
                #if we get no clashes after finding the point with the min distance from p1,p2,p3 then we will map that point to the next point in 2d map
                if(len(temp3)==1):
                    x = x+r #find the next points in the 2d map for the current equivalence class 
                    y = y-r
                    out[c].append([x,y,temp3[0]]) #add the mapping result to the out list
                    l[c].remove(temp3[0]) #will remove the the mapped point from the list l as we have already done the mapping for that point(l contains only the points which are left to be mapped)
                    count+=1 # will increase the number of mapped points by 1 
                # if after looking at their distance from p3, their are still points which clash for the min distance then we wiil resolve those clashes by considering the order in the temp3 list. we will map the points with the order in which they are in temp3 list 
                elif(len(temp3)>1):
                    while(len(temp3)):
                        x = x+r #find the next points in the 2d map for the current equivalence class
                        y = y-r
                        out[c].append([x,y,temp3[0]]) #add the mapping result to the out list
                        l[c].remove(temp3[0])   #will remove the the mapped point from the list l as we have already done the mapping for that point(l contains only the points which are left to be mapped)
                        temp3.remove(temp3[0])
                        count+=1
            #if we get no clashes after finding the point with the min distance from p1 and p2, then we will map that point to the next point in 2d map
            elif(len(temp2)==1):
                x = x+r #find the next points in the 2d map for the current equivalence class
                y = y-r
                out[c].append([x,y,temp2[0]]) #add the mapping result to the out list
                l[c].remove(temp2[0]) #will remove the the mapped point from the list l as we have already done the mapping for that point(l contains only the points which are left to be mapped)
                count+=1
        #if we get no clashes after finding the point with the min distance from p1, then we will map that point to the next point in 2d map
        elif(len(temp1)==1):
            x = x+r #find the next points in the 2d map for the current equivalence class
            y = y-r
            out[c].append([x,y,temp1[0]]) #add the mapping result to the out list
            l[c].remove(temp1[0]) #will remove the the mapped point from the list l as we have already done the mapping for that point(l contains only the points which are left to be mapped)
            count+=1 # will increase the number of mapped points by 1
    
    #This while loop will take care of the mapping of the remaining half points. the algorithm for this mapping will reverse the reference point ie. will choose the reference point from the end(right)
    #the algorithm works the same way as above
    while(len(l[c])):
        p1 = out[c][0][2]
        p2 = out[c-1][0][2]
        p3 = out[c-1][2][2]
        r = (math.dist([out[c][0][0], out[c][0][1]], [out[c][1][0], out[c][1][1]])/(math.sqrt(2)))/(temp-1)
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
                if(len(temp3)==1):
                    x = x+r
                    y = y-r
                    out[c].append([x,y,temp3[0]])
                    l[c].remove(temp3[0])
                elif(len(temp3)>1):
                    while(len(temp3)):
                        x = x+r
                        y = y-r
                        out[c].append([x,y,temp3[0]])
                        l[c].remove(temp3[0])
                        temp3.remove(temp3[0])
            elif(len(temp2)==1):
                x = x+r
                y = y-r
                out[c].append([x,y,temp2[0]])
                l[c].remove(temp2[0])
        elif(len(temp1)==1):
            x = x+r
            y = y-r
            out[c].append([x,y,temp1[0]])
            l[c].remove(temp1[0])

# will do the mapping for each equvalence class from 2 to d*n-1
for i in range(2, d*n):
    fn(i)
# mapping for the last equvalence class d*n    
out.append([[(d*n)/2, (d*n)/2, [n for i in range(d)]]])

# will print out the hd coordinates and their corresponding mapped 2d coordinates
for i in out:
    for j in i:
        l1 = j[2]
        coords = [j[0],j[1]]
        print(str(l1)+": "+str(coords))

# end will store the time when the execution of the program ends
end = time.time()
print("Time Elapsed(CPU): ", time.process_time())
print("Time Elapsed(to run script): ", end-start)
print('RAM memory used:', psutil.virtual_memory()[3]/(1024**2))

it = -1
fig1 = go.Figure()
for i in out:
    it+=1
    xpos=[]
    ypos=[]
    for j in i:
        xpos.append(j[0])
        ypos.append(j[1])
    fig1.add_trace(go.Scatter(
    x=xpos,
    y=ypos,
    name = "<b>Equivalence Class- " + str(it) +"</b>", # Style name/legend entry with html tags
    connectgaps=True # override default to connect the gaps
))
    
fig1.show()







# **********************************************************************************************************************
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
# **********************************************************************************************************************
