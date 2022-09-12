import time
import math
import psutil
import plotly.express as px
import plotly.graph_objects as go
import csv
import os
import pandas as pd
import shutil

if os.path.exists('./outputs'):
    shutil.rmtree('./outputs')
os.mkdir("./outputs")
# #Enter the max value each dimention in the input can take
# #The Range of value each dimention can take then will be [0-max value]
print("Enter maximum value of the element of vector:", end = ' ')
n = int(input()) #max no of value in T1, T2, T3

#Enter the number of dimentions in the vector
print("Enter the dimension of vector:", end = ' ')
d = int(input())

#Hence Number of equavalence class will be equal to d*n+1 and will be {0,1,2,....,d*n+1}

#notes the starting execution time of the program
start = time.time()

# mapping for equavalence class-0
df = pd.read_csv("./inputs/{}.csv".format(0), usecols = ['HD Point of equivalence class {}'.format(0)])
hdpoint=df['HD Point of equivalence class {}'.format(0)][0]
hdpoint = hdpoint.strip('][').split(', ')
hdpoint=[int(j) for j in hdpoint]
with open('./outputs/0.csv', 'w',newline="") as f:
        thewriter = csv.writer(f)
        thewriter.writerow(["HD Point of equivalence class {}".format(d*n),"LD Point"])
        thewriter.writerow([hdpoint,[0,0]])
# with open('./inputs/0.csv', mode ='r')as file:
#     csvFile = csv.reader(file)
#     # displaying the contents of the CSV file
#     input=[]
#     for line in csvFile:
#         if "HD Point of equivalence class 0" in line: continue
#         else:
#             for x in line:
#                 x = x.strip('][').split(', ')
#                 input.append([int(j) for j in x])
# with open('./outputs/0.csv', 'w',newline="") as f:
#         thewriter = csv.writer(f)
#         thewriter.writerow(["HD Point of equivalence class 0","LD Point"])
#         thewriter.writerow([input[0],[0,0]])
        
# out = [[[0,0,input[0]]]] #base cases
input=[]
# mapping for equavalence class-1
with open('./inputs/1.csv', mode ='r')as file:
    csvFile = csv.reader(file)
    # displaying the contents of the CSV file
    input=[]
    for line in csvFile:
        if "HD Point of equivalence class 1" in line: continue
        else:
            for x in line:
                x = x.strip('][').split(', ')
                input.append([int(j) for j in x])
len1 = len(input)
x1=0
y1=1
with open('./outputs/1.csv', 'w',newline="") as f:
    thewriter = csv.writer(f)
    thewriter.writerow(["HD Point of equivalence class 1","LD Point"])
    r = 1/(len1-1)
    thewriter.writerow([input[-1],[1,0]])    
    thewriter.writerow([input[0],[0,1]])
    input.remove(input[-1])
    input.remove(input[0])
    for i in input:
        x1+=r
        y1-=r
        thewriter.writerow([i,[x1,y1]])

#function that will do the mapping for the equivalence class c and will store the ordered points in the the out list and in a csv file
def fn(c):
    input=[]
    out=[]
    with open('./inputs/{}.csv'.format(c), mode ='r')as file:
        csvFile = csv.reader(file)
        # displaying the contents of the CSV file
        input=[]
        for line in csvFile:
            if "HD Point of equivalence class {}".format(c) in line: continue
            else:
                for x in line:
                    x = x.strip('][').split(', ')
                    input.append([int(j) for j in x])
    #input list consists of all the LD points of equivalence class c               
    # will store the number of points in the the equivalece class c  
    temp = len(input)
    with open('./outputs/{}.csv'.format(c), 'w',newline="") as f:
        thewriter = csv.writer(f)
        thewriter.writerow(["HD Point of equivalence class {}".format(c),"LD Point"])    
        #will add the first and the last hd point to of the equivalence class in the out list
        if(c<((d*n)/2)):
            out.append([c,0,input[-1]]) 
            out.append([0,c,input[0]]) 
            thewriter.writerow([input[-1],[c,0]])
            thewriter.writerow([input[0],[0,c]])
        else: 
            out.append([(d*n)/2,(c-(d*n)/2),input[-1]])
            out.append([(c-(d*n)/2),(d*n)/2,input[0]])
            thewriter.writerow([input[-1],[(d*n)/2,(c-(d*n)/2)]])
            thewriter.writerow([input[0],[(c-(d*n)/2),(d*n)/2]])
        # will remove the first and the last points from the input list as we have already done the mapping for them in out
        input.remove(input[0])
        input.remove(input[-1])
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
        #will continue the loop until half of the points of the equivalnce class has been mapped
        while(len(input) and (count<=change)):
            #p1,p2,p3 are the reference points which we will use to order the remaining points of the equivalence class
            p1=out[1][2]
            df = pd.read_csv("./outputs/{}.csv".format(c-1), usecols = ['HD Point of equivalence class {}'.format(c-1),'LD Point'])
            p2=df['HD Point of equivalence class {}'.format(c-1)][1] 
            p2 = p2.strip('][').split(', ')
            p2=[int(j) for j in p2]
            p3=df['HD Point of equivalence class {}'.format(c-1)][2]
            p3 = p3.strip('][').split(', ')
            p3=[int(j) for j in p3]
            #r is the distance between each point of the equivalence class in the 2d map
            r = (math.dist([out[0][0], out[0][1]], [out[1][0], out[1][1]])/(math.sqrt(2)))/(temp-1)
            #input- the list of remaining points of the equivalence class which are remaining to be mapped
            #will calculate the distance between the first point in input 
            dis = math.dist(input[0], p1)
            #temp1 will store the points(1 or more) from input that are closest to p1
            temp1 = [input[0]]       
            for i in input:
                #if we get an even closer point to p1, then we will replace the current min points in temp1 with the new min point
                if(dis > math.dist(i, p1)): 
                    dis = math.dist(i, p1)
                    temp1.clear()
                    temp1.append(i)
                #if the distance of this point from p1 is equal to the distance of the current closest point, then we will add the point to temp1
                elif( dis == math.dist(i, p1) and i != temp1[0]): 
                    temp1.append(i)
                #if the distance of this point from p1 is greater thatn the distnace of the current closest point,then we will ignore this point

            #Now if in temp1, we have more than one point which have the same min distance to p1 then we will have to resolve those clashes by looking  at their distance from p2, and then order them by their distance.The point with the min distance will come first in the ordering and will    similarly do this for others.
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
                        thewriter.writerow([temp3[0],[x,y]])
                        out.append([x,y,temp3[0]]) #add the mapping result to the out list
                        input.remove(temp3[0]) #will remove the the mapped point from the list input as we have already done the mapping for that point(input contains only the points which are left to be mapped)
                        count+=1 # will increase the number of mapped points by 1 
                    # if after looking at their distance from p3, their are still points which clash for the min distance then we wiil resolve those clashes by considering the order in the temp3 list. we will map the points with the order in which they are in temp3 list 
                    elif(len(temp3)>1):
                        while(len(temp3)):
                            x = x+r #find the next points in the 2d map for the current equivalence class
                            y = y-r
                            thewriter.writerow([temp3[0],[x,y]])
                            out.append([x,y,temp3[0]]) #add the mapping result to the out list
                            input.remove(temp3[0])   #will remove the the mapped point from the list input as we have already done the mapping for that point(input contains only the points which are left to be mapped)
                            temp3.remove(temp3[0])
                            count+=1
                #if we get no clashes after finding the point with the min distance from p1 and p2, then we will map that point to the next point in 2d map
                elif(len(temp2)==1):
                    x = x+r #find the next points in the 2d map for the current equivalence class
                    y = y-r
                    thewriter.writerow([temp2[0],[x,y]])
                    out.append([x,y,temp2[0]]) #add the mapping result to the out list
                    input.remove(temp2[0]) #will remove the the mapped point from the list input as we have already done the mapping for that point(input contains only the points which are left to be mapped)
                    count+=1
            #if we get no clashes after finding the point with the min distance from p1, then we will map that point to the next point in 2d map
            elif(len(temp1)==1):
                x = x+r #find the next points in the 2d map for the current equivalence class
                y = y-r
                thewriter.writerow([temp1[0],[x,y]])
                out.append([x,y,temp1[0]]) #add the mapping result to the out list
                input.remove(temp1[0]) #will remove the the mapped point from the list input as we have already done the mapping for that point(input contains only the points which are left to be mapped)
                count+=1 # will increase the number of mapped points by 1
    
        #This while loop will take care of the mapping of the remaining half points. the algorithm for this mapping will reverse the reference point ie. will choose the reference point from   the end(right)
        #the algorithm works the same way as above
        while(len(input)):
            p1=out[0][2]
            df = pd.read_csv("./outputs/{}.csv".format(c-1), usecols = ['HD Point of equivalence class {}'.format(c-1),'LD Point'])
            p2=df['HD Point of equivalence class {}'.format(c-1)][0] 
            p2 = p2.strip('][').split(', ')
            p2=[int(j) for j in p2]
            p3=df['HD Point of equivalence class {}'.format(c-1)][len(df.index)-1]
            p3 = p3.strip('][').split(', ')
            p3=[int(j) for j in p3]
            r = (math.dist([out[0][0], out[0][1]], [out[1][0], out[1][1]])/(math.sqrt(2)))/(temp-1)
            dis = math.dist(input[0], p1)
            temp1 = [input[0]]
            for i in input:
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
                        thewriter.writerow([temp3[0],[x,y]])
                        out.append([x,y,temp3[0]])
                        input.remove(temp3[0])
                    elif(len(temp3)>1):
                        while(len(temp3)):
                            x = x+r
                            y = y-r
                            thewriter.writerow([temp3[0],[x,y]])
                            out.append([x,y,temp3[0]])
                            input.remove(temp3[0])
                            temp3.remove(temp3[0])
                elif(len(temp2)==1):
                    x = x+r
                    y = y-r
                    thewriter.writerow([temp2[0],[x,y]])
                    out.append([x,y,temp2[0]])
                    input.remove(temp2[0])
            elif(len(temp1)==1):
                x = x+r
                y = y-r
                thewriter.writerow([temp1[0],[x,y]])
                out.append([x,y,temp1[0]])
                input.remove(temp1[0])

# will do the mapping for each equvalence class from 2 to d*n-1
for i in range(2, d*n):
    fn(i)
# mapping for the last equvalence class d*n 
df = pd.read_csv("./inputs/{}.csv".format(d*n), usecols = ['HD Point of equivalence class {}'.format(d*n)])
hdpoint=df['HD Point of equivalence class {}'.format(d*n)][0]
hdpoint = hdpoint.strip('][').split(', ')
hdpoint=[int(j) for j in hdpoint]
with open('./outputs/{}.csv'.format(d*n), 'w',newline="") as f:
        thewriter = csv.writer(f)
        thewriter.writerow(["HD Point of equivalence class {}".format(d*n),"LD Point"])
        thewriter.writerow([hdpoint,[(d*n)/2, (d*n)/2]])

# # will print out the hd coordinates and their corresponding mapped 2d coordinates
# for i in out:
#     for j in i:
#         l1 = j[2]
#         coords = [j[0],j[1]]
#         print(str(l1)+": "+str(coords))

# end will store the time when the execution of the program ends
end = time.time()
print("Time Elapsed(CPU): ", time.process_time())
print("Time Elapsed(to run script): ", end-start)
print('RAM memory used:', psutil.virtual_memory()[3]/(1024**2))

# it = -1
# fig1 = go.Figure()
# for i in out:
#     it+=1
#     xpos=[]
#     ypos=[]
#     for j in i:
#         xpos.append(j[0])
#         ypos.append(j[1])
#     fig1.add_trace(go.Scatter(
#     x=xpos,
#     y=ypos,
#     name = "<b>Equivalence Class- " + str(it) +"</b>", # Style name/legend entry with html tags
#     connectgaps=True # override default to connect the gaps
# ))
    
# fig1.show()







# **********************************************************************************************************************
# l1 = []
# input = []
# z = 0
# for i in range(d*n+1):
#     for z in range(n+1):
#         for y in range(n+1):
#             for x in range(n+1):
#                 if (x+y+z)==i :
#                     l1.append([x,y,z])
#     input.append(l1)
#     l1 = []
# print(input)

# max1 = int(input("Enter max Value: "))
# dim = int(input("Enter Dimension: "))
# **********************************************************************************************************************