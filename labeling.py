from time import time
import math
from tkinter import N
from xml.dom.minicompat import NodeList
import matplotlib.pyplot as plt
import networkx as nx
from pathlib import Path
import xlsxwriter
import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize) #print all numpy datas without truncation
#------------------
nodes=[]
edges=[]
entryname=''
augmentpaths=[]
start=0
flow=0
n=0
m=0
edgex = np.zeros((n, n), dtype=np.int)
#------------------
class Edge:
    def __init__(self,u,v,c,x,r):
        self.u=u
        self.v=v
        self.c=c
        self.x=x
        self.r=r
#------------------
class Node:
    def __init__(self,i,pred,islabeled):
        self.i=i
        self.pred=pred
        self.islabeled=islabeled
#------------------
def labeling():
    global nodes
    global edges
    global flow
    global start
    global m
    global n
    global entryname
    global augmentpaths
    global edgex
    edgex=np.zeros((n, n), dtype=np.int)
    augmentpaths=[]
    flow=0
    start = time()
    listt=[]
    nodes[n-1].islabeled = True
    while nodes[n-1].islabeled == True and m>0:
        end=time()
        exectime = end-start
        if exectime>22:
            break
        for node in nodes: 
            node.islabeled=False #unlabel all nodes
            node.pred=Edge(0,0,0,0,0) #delete preds

        nodes[0].islabeled=True #label node s
        listt.append(nodes[0]) #add s to list
        while listt!=[] : #while list.. and nodes[n-1].islabeled==False
            end=time()
            exectime = end-start
            if exectime>22:
                break
            i=listt[0]
            listt.pop(0) #remove i from list
            for e in edges :
                end=time()
                exectime = end-start
                if exectime>22:
                    break
                if e.u == i.i: #find i arcs
                    j = nodes[e.v-1]
                    if e.r>0 and j.islabeled==False: #if rij>0 and j is unlabaled
                        nodes[e.v-1].pred=e #set edge pred j
                        nodes[e.v-1].islabeled=True   #label node j
                        listt.append(j)
        if nodes[n-1].islabeled:
            augment()

    end=time()
    exectime = end-start
    
    with open('E:/master99/3/optimization_algo/HW/hw4/evacuation/graphs/'+entryname+'.txt' , 'w' , encoding='utf-8') as f: #cleare file 
        f.write("**edges:")
        f.write("\n")
        f.close
    for tp in augmentpaths:
        ed=tp[0]
        sigma=tp[1]
        last=0
        with open('E:/master99/3/optimization_algo/HW/hw4/evacuation/graphs/'+entryname+'.txt' ,'a', encoding='utf-8') as f: #appends to file 
            f.write(" path: ")
            for z in ed:
                last=z
                f.write(str(z.u))
                f.write(" -> ")
            f.write(str(last.v))
            f.write(" flow: ")
            f.write(str(sigma))
            f.write("\n")
            f.close()
    with open('E:/master99/3/optimization_algo/HW/hw4/evacuation/graphs/'+entryname+'.txt' ,'a', encoding='utf-8') as f: #appends to file 
        f.write("\n")
        f.write("max flow:")
        f.write(str(flow))
        f.write("\n\n\n")
        f.write("edges flow:")
        f.write("\n")
        f.write(str(edgex))
        f.close()
    return exectime,flow
#------------------
def augment():
    global nodes
    global edges
    global flow
    global start
    global augmentpaths
    global edgex
    augmentpath=[] #edge haye masir (har pred edge hast)
    p= nodes[n-1].pred
    while p.u!=0: #find augment path
        end=time()
        exectime = end-start
        if exectime>22:
            break
        augmentpath.append(p)
        p= nodes[p.u-1].pred
    augmentpath.reverse() #reverse preds to reach the path from source to sink
    min=augmentpath[0].r #find min r in path and name it 'sigma'
    for i in range(1,len(augmentpath)):
        end=time()
        exectime = end-start
        if exectime>22:
            break
        if augmentpath[i].r<min:
            min=augmentpath[i].r
    sigma=min

    augmentpaths.append((augmentpath,sigma))
    #augment sigma units and add more edges in residual network and update x,r for each edge, remove r=0 edges (age az v be u augment kardim bayad sigma vahed az u be v bargardunim va in yal age vojod nadasht ezafe konim age ham vojod dasht be r oon yale baraxe ezafe konim)
    for p in augmentpath:
        p.r-=sigma
        p.x+=sigma
        edgex[p.u-1][p.v-1]+=sigma
    for p in augmentpath: #update edges 
        flag = False
        for e in edges:
            end=time()
            exectime = end-start
            if exectime>22:
                break
            if e.u == p.u and e.v == p.v : #find edge
                e.r=p.r #update edge's r

                for ee in edges:
                    end=time()
                    exectime = end-start
                    if exectime>22:
                        break
                    if ee.u==e.v and ee.v==e.u: #if we have reverse edge vu add r
                        flag=True
                        ee.r+=sigma
                        break

                if flag==False: #if we dont have reverse edge add reverse edge with r=sigma and x=0
                    edge=Edge(p.v,p.u,p.c,0,sigma)
                    edges.append(edge)

                break
    flow+=sigma
    return augmentpath,flow
#------------------
def create_file(name):
    workbook = xlsxwriter.Workbook('E:/master99/3/optimization_algo/HW/hw4/evacuation/results/'+name+'.xlsx')
    worksheet = workbook.add_worksheet(name)

    worksheet.write('A1', 'File Name')
    worksheet.write('B1', 'N')
    worksheet.write('C1', 'M')
    worksheet.write('D1', 'Max Flow')
    worksheet.write('E1', 'expected flow')
    worksheet.write('F1', 'Execution Time')

    return workbook, worksheet
#------------------
def write_to_file(workbook, worksheet,filename,n,m,maxflow, exresult,exectime,i):
    worksheet.write('A' + str(i+2), filename)
    worksheet.write('B' + str(i+2), n)
    worksheet.write('C' + str(i+2), m)
    worksheet.write('D' + str(i+2), maxflow)
    worksheet.write('E' + str(i+2), exresult)
    worksheet.write('F' + str(i+2), exectime)
#------------------
def main():
    global nodes
    global edges
    global m
    global n
    global entryname
    entries = Path('E:/master99/3/optimization_algo/HW/hw4/evacuation/Instances')
    results = Path('E:/master99/3/optimization_algo/HW/hw4/evacuation/expected_results')
    index=0
    exresult=0
    wb, ws = create_file("labeling")
    for entry in entries.iterdir():
        entryname=entry.name
        nodes=[]
        edges=[]
        
        print("entry name:"+entry.name)
        f = open('E:/master99/3/optimization_algo/HW/hw4/evacuation/Instances/'+entry.name, "r")
        line1=f.readline().split()
        n=int(line1[0])
        m=int(line1[1])

        for i in range(m):
            lines=f.readline().split()
            edge=Edge(int(lines[0]),int(lines[1]),int(lines[2]),0,int(lines[2]))
            edges.append(edge)
        
        for i in range(n):
            node=Node(i+1,Edge(0,0,0,0,0),False)
            nodes.append(node)

        executiontime , maxflow = labeling()
        print("execution time:",executiontime)
        print("maxflow:",maxflow)

        for result in results.iterdir():
            name = result.name.split('.')
            if name[0]==entry.name:
                f = open('E:/master99/3/optimization_algo/HW/hw4/evacuation/expected_results/'+result.name, "r")
                line1=f.readline().split()
                exresult=int(line1[0])
                
        write_to_file(wb, ws, entry.name,n,m, maxflow,exresult, executiontime, index)
        index+=1
    wb.close()
#-------------------------
if __name__ == "__main__":
   print ('Start')
   main()
   print ('Done!')