import pandas as pd
import csp
import time
from utils import argmax_random_tie
import sys

data = pd.read_csv('Στοιχεία Μαθημάτων.csv')

shape = data.shape
dates = 21
slots = 3
sizevar = dates*slots

infomath = {}
weight = 1
templist = set()
temple = set()
listi = []

temp = ' '
listv = []
tarstr = """ """      

# create domain
def create_list_of_math(listi,infomath):

    for j in range(shape[0]):
        listv.append(data.loc[j].iat[1])
        for i in range(shape[1]):
            listi.append(data.loc[j].iat[i])
            if i == shape[1]-1:
                d = data.loc[j].iat[1]
                if data.loc[j].iat[i] == True:
                    temp = 'Εργαστήριο ' + d
                    listv.append(temp)
                    listi.append(temp)
                    templist.add(d)
                    temple.add(temp)
        tempd = { data.loc[j].iat[1]:listi }
        infomath = { **infomath, **tempd }
        listi = []

    listv.append('nomath')

    return listi, infomath, listv

# create neighboors
def create_neighbors(tarstr):

    for j in range(sizevar):
        tarstr = tarstr + str(j+1) + """: """
        for i in range(sizevar):
            if i == sizevar:
                if j != i:
                    tarstr = tarstr + str(i+1)
            else:
                if j != i:
                    tarstr = tarstr + str(i+1) + """ """ 
        if j != sizevar-1:
            tarstr = tarstr + """;""" + """ """

    return tarstr

# constraint function return true when two or more variable are not in conflict
def constraint(A ,a ,B ,b):
    
    # check if two variables A and B has diff -1 and
    # if a is math with lab and if it's not in third time slot

    if (int(A) - int(B)) == -1 and a in templist:
        if (int(A) % 3) != 0 or int(A) != sizevar:
            return b == infomath[a][5]
    elif b in temple and (int(A) - int(B)) == -1:
        if a == b[11:] and int(B) != 1:
            return True
        else:
            return False
    else:  
        if csp.different_values_constraint(A, a, B, b) and int(A) != sizevar: # check if variable A has unique value
            if a in infomath and b in infomath: # check if two math are in same semester or has the same professor
                if infomath[a][2] == infomath[b][2] or infomath[a][0] == infomath[b][0]:
                    return abs(int(A) - int(B)) > (int(A) % 3 - int(B) + 2)
                elif infomath[a][3] is True and infomath[b][3] is True: # check if two math are difficult
                    return abs(int(A) - int(B)) > (int(A) % 3 + 3)
            return True
        elif a == 'nomath': # get nomath value if no one else is consistent
            return True
        else:
            return False

def dom_wdeg(assignment,csp): # get weights for all unassigned variables
    return argmax_random_tie([v for v in csp.variables if v not in assignment],
                             key=lambda var: heuristic(csp,var,weight))

def heuristic(csp,var,weight):
    # calculate weights value for variables

    sum = 0

    if revise:
        sum = sum + weight

    # use one variable as weight because for each variable
    # call same var as weight but when finish initialize
    # weight var 
    weight = 1

    return sum
                             
def revise(var ,A ,a ,B ,b,weight):
    # revised algorithm from paper reference

    listd = listv

    for i in listd:
        if constraint(A ,a ,B ,b) is False:
            listd.pop()
    if len(listd) == 0:
        weight = weight + 1

    return len(listd) != 0

if __name__=="__main__":


    # main function call csp methods

    listi, infomath, listv = create_list_of_math(listi,infomath)
    tarstr = create_neighbors(tarstr)

    neighbors = csp.parse_neighbors(tarstr)

    exam_csp = csp.CSP(list(neighbors.keys()),csp.UniversalDict(listv),neighbors,constraint)

    # Specify which method to use. Get as a command line parameter

    if len(sys.argv) > 2:
        if sys.argv[2] == 'fc' and sys.argv[4] == 'dom_wdeg':
            start = time.time()
            result,checks = csp.backtracking_search(exam_csp,select_unassigned_variable=dom_wdeg, order_domain_values=csp.lcv, inference=csp.forward_checking)
            end = time.time()
            time = end - start
            print(time)
            print(result,checks)
        elif sys.argv[2] == 'fc' and sys.argv[4] == 'mrv':
            start = time.time()
            result,checks = csp.backtracking_search(exam_csp,select_unassigned_variable=csp.mrv, order_domain_values=csp.lcv, inference=csp.forward_checking)
            end = time.time()
            time = end - start
            print(time)
            print(result,checks)
        elif sys.argv[2] == 'mac' and sys.argv[4] == 'dom_wdeg':
            start = time.time()
            result,checks = csp.backtracking_search(exam_csp,select_unassigned_variable=dom_wdeg, order_domain_values=csp.lcv, inference=csp.mac)
            end = time.time()
            time = end - start
            print(time)
            print(result,checks)
        elif sys.argv[2] == 'mac' and sys.argv[4] == 'mrv':
            start = time.time()
            result,checks = csp.backtracking_search(exam_csp,select_unassigned_variable=csp.mrv, order_domain_values=csp.lcv, inference=csp.mac)
            end = time.time()
            time = end - start
            print(time)
            print(result,checks)
        elif sys.argv[2] == 'minconflict':
            start = time.time()
            result,checks = csp.min_conflicts(exam_csp)
            end = time.time()
            time = end - start
            print(time)
            print(result,checks)
        else:
            print("Wrong name of method")