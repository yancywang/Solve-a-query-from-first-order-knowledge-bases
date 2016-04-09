import copy;
import sys;
import types;

pofix=0;
result ='';
def print_clause(list):
    str=list[0];
    str+='(';
    for i in range(len(list[2])):
        if list[2][i].islower():
            str+='_';
        else:
            str+=list[2][i];
        if i!=len(list[2])-1:
            str+=', ';
    str+=')';
    return str;

def read_clause(str):
    vars='';
    name='';
    for i in range(len(str)):
        if str[i]=='(':
            name = str[:i];
            vars = str[i+1:len(str)-1];
            break;
    va=[];
    i=0;
    while (i<len(vars)):
        if vars[i]==',':
            va.append(vars[:i].strip());
            vars=vars[i+1:];
            i=-1;
        i+=1;
    va.append(vars.strip());
    return [name,[],va];



def read_line(line):  
    list=line.replace('=>','&&').split('&&');
    i=0;
    llist=[];
    while (i<len(list)-1):
        if list[i]!='&&' and len(list)>1:
            llist.append(read_clause(list[i].strip()));
        i+=1;
    result = read_clause(list[len(list)-1].strip());
    result[1]= llist;
    return result;





def standardize_vars(lii):
    li=copy.copy(lii);
    global pofix;
    for i in range(len(li[2])):
        if li[2][i].islower():
            li[2][i]=li[2][i][0]+str(pofix);
    for j in range(len(li[1])):
        for k in range(len(li[1][j][2])):
            if li[1][j][2][k].islower():
                li[1][j][2][k]=li[1][j][2][k][0]+str(pofix);
    pofix+=1;
    return li;


def subst(x,r):
    x1=copy.deepcopy(x);
    for lis in r:
        for i in range(len(x1[2])):
            if lis[0]==x1[2][i]:
                x1[2][i]=lis[1];
        for j in range(len(x1[1])):
            for k in range(len(x1[1][j][2])):
                if lis[0]==x1[1][j][2][k]:
                    x1[1][j][2][k]=lis[1];
    return x1;
                
            

def unify(x,y,r):
   
    if r==False:
        return False;
    elif x==y:
        return r;
    elif type(x)==type('a') and x.islower():
        return unify_var(x,y,r);
    elif type(y)==type('a') and y.islower():
        return unify_var(y,x,r); 
    elif type(x)==type([1,2,3]) and type(y)==type([1,2,3]):
        v=x[0];
        w=y[0];
        del x[0];
        del y[0];
        if len(x)==1:
            x=x[0];
        if len(y)==1:
            y=y[0];
        return unify(x,y,unify(v,w,r));
    else:
        return False;
     
def unify_var(x,y,r):
    for lis in r:
        if lis[0]==x:
            return unify(lis[1],y,r);
    for lis in r:
        if lis[0]==y:
            return unify(x,list[1],r);
    if occur_check(x,y,r)==True:
        return False;
    else:
        r.append([x,y]);
        return r;
        
def occur_check(x,y,r):
    for lis in r:
        if x==lis[0] and y==lis[1]:
            return True;
    return False;    


def fol_bc_ask(kb,query):
    return fol_bc_or(kb,query,[]);

def fol_bc_or(kb,goal8,r8):
    global result;
    r=copy.deepcopy(r8);
    global pofix;   
    index=False;
    coun=0;
    count = 0;
    for sto1 in fetch_rules_for_goal(kb,goal8):
        if sto1[1]==[] and sto1[0]==index:
            coun+=1;
        if index==False:
            index = sto1[0];
        
        if not sto1[0]==index:
            coun=0;
        if coun<1:
            result=result + "ASK: "+print_clause(goal8)+'\n';
        goal = copy.deepcopy(goal8);
        sto = copy.deepcopy(sto1);
        sto = standardize_vars(sto);
        for r1 in fol_bc_and(kb,sto[1],unify(sto[2], goal[2], r)):
            count+=1;
            result=result + "True: "+print_clause(subst(goal8,r1))+'\n';
            yield r1;
    if count==0:
        result=result +"False: "+print_clause(goal8)+'\n';

    
            
def fol_bc_and(kb,goals,r):
    if r==False:
        return;
    elif len(goals)==0:
        yield r;
    else:
        first = goals[0];
        rest = goals[1:];
        for r1 in fol_bc_or(kb,subst(first, r),r):
            for r2 in fol_bc_and(kb,rest,r1):
                yield r2;
                
def fetch_rules_for_goal(kb,goal):     
      
    for li in kb:
        ist = True;
        if li[0]==goal[0]:
            yield li;

filename = 'sample05.txt';
file = open(filename,"r"); 
ack=read_clause(file.readline().strip());
kb1=[];
lengt = int(file.readline().strip());
for i in range(lengt):
    line=file.readline().strip();
    kb1.append(read_line(line));

isget = True;
for isd in fol_bc_ask(kb1,ack):
    result +='True';
    isget = False;
if isget:
    result +='False';
print result;
file = open('output.txt','w+');
file.write(result);
file.close();
