import re

def parsedb(): # get database
    replayer=re.compile('^(.+):\s*$') # Check for playerv
    regame=re.compile('^(.+)(w|b)\s*(\d*\.?\d*)\s*$') # Check for game
    reempty=re.compile('^\s*$') # Check if empty
    dbf=open('mfsdb','r').read().split('\n')
    db=[] # db[i]=[name,[opp. name,color,score]]
    pl=[]
    err=0
    for i in dbf:
        player=replayer.match(i)
        game=regame.match(i)
        empty=reempty.match(i)
        if(player):
            db.append([player.group(1).strip()])
            pl.append(player.group(1).strip())
        elif(game):
            db[-1].append([game.group(1).strip(),game.group(2),float(game.group(3))])
        elif(empty):
            continue
        else:
            print "Error parsing database "+i
            err=1
    if(err==1):
        return -1
    for i in db:
        for j in i[1:]:
            if j[0] not in pl:
                print "Unknown player: "+j[0]
                err=1
    if(err==1):
        return -1
    return db

def parsecls(): # get classes and people
    reclas=re.compile('^(.+):\s*$') # Check for class
    reempty=re.compile('^\s*$') # Check if empty
    clsf=open('class','r').read().split('\n')
    cls=[] # [class,[players]]
    for i in clsf:
        clas=reclas.match(i)
        empty=reempty.match(i)
        if(clas):
            cls.append([clas.group(1).strip(),[]])
        elif(empty):
            continue
        else:
            cls[-1][1].append(i.strip())
    return cls

def parsepair(): # get pairs
    repair=re.compile('^(.+)-(.+):\s*(\d*\.?\d*)\s*-\s*(\d*\.?\d*)\s*$')
    reempty=re.compile('^\s*$') # Check if empty
    pairf=open('pairs','r').read().split('\n')
    pairs=[] # [white,black,score(w),score(b)]
    err=0
    for i in pairf:
        pair=repair.match(i)
        empty=reempty.match(i)
        if(pair):
            pairs.append([pair.group(1).strip(),pair.group(2).strip(),float(pair.group(3)),float(pair.group(4))])
        elif(empty):
            continue
        else:
            print "Error parsing pair "+i
            err=1
    if(err==1):
        return -1
    return pairs

def tbsort(tb):
    l = []
    e = []
    g = []
    if len(tb) > 1:
        p1 = tb[0]
        for p2 in tb:
            for i in [1,2,3,4,5,0]:
                if(i==0):
                    e.append(p2)
                    break
                elif(p1[i]==p2[i]):
                    continue
                l.append(p2) if p1[i]<p2[i] else g.append(p2)
                break
        return tbsort(l)+e+tbsort(g)  
    else:
        return tb

def gentiebreak(db): # generates tie breaks
    tb=[] #[player, total score, total win, no. games with black, avg. opponent rating/total games, sum of opponent rating, +_number of rep color(+ for white, - for black), played b4]
    for i in db:
        tb.append([i[0],0,0,0,0,0,0,[]])
        for j in i[1:]:
            if(j[0]=='Bye'):
                continue
            tb[-1][1]+=j[2]
            tb[-1][2]+=1 if j[2]==1.0 else 0
            tb[-1][3]+=1 if j[1]=='b' else 0
            tb[-1][7].append(j[0])
            if(j[1]=='w'):
                if(tb[-1][6]>0):
                    tb[-1][6]+=1
                else:
                    tb[-1][6]=1
            else:
                if(tb[-1][6]<0):
                    tb[-1][6]-=1
                else:
                    tb[-1][6]=-1
    for i in xrange(len(tb)):
        if(len(db[i])==1):
            continue
        for j in db[i][1:]:
            for k in tb:
                if(k[0]==j[0]):
                    tb[i][5]+=k[1]
                    break
        tb[i][4]=tb[i][5]/(len(db[i])-1)
    return tbsort(tb)

def pair(pl): # Pairs players
    pairs=[] # [white,black]
    while(True): # pairing pl[0]
        if(len(pl)==0):
            break
        if(len(pl)==1):
            pairs.append([pl[0][0],'Bye']) # effectively 
            break
        lim=0.0
        while(all([i[0] in pl[0][7] for i in pl[1:]])):
            for i in pl[1:]:
                pl[0][7].remove(i[0])
        while(True):#slowly increase the lim to allow for more weirder pairs
            for j in xrange(1,len(pl)): # finding pair
                if(pl[j][0] in pl[0][7]): # played before
                    continue
                if(pl[0][1]-pl[j][1]>lim): # score difference too large
                    break
                if((pl[0][6]>0)!=(pl[j][6]>0)): # played diff color
                    if(pl[0][6]>0): # pl[0] played white previously
                        pairs.append([pl[j][0],pl[0][0]])
                    else:
                        pairs.append([pl[0][0],pl[j][0]])
                    del pl[j]
                    del pl[0]
                    lim=-1
                    break
                if(abs(pl[0][6])>lim or abs(pl[j][6])>lim): # played same color too many times
                    continue
                if(abs(pl[0][6])>abs(pl[j][6])): # if pl[0] played same color more times
                    if(pl[0][6]>0): # pl[0] played white, now playing black
                        pairs.append([pl[j][0],pl[0][0]])
                    else:
                        pairs.append([pl[0][0],pl[j][0]])
                    del pl[j]
                    del pl[0]
                    lim=-1
                    break
                else: # if pl[j] played same color more or equal times(pl[j] is weaker, so avoid playing same color more times)
                    if(pl[j][6]>0): # pl[j] played white, now playing black
                        pairs.append([pl[0][0],pl[j][0]])
                    else:
                        pairs.append([pl[j][0],pl[0][0]])
                    del pl[j]
                    del pl[0]
                    lim=-1
                    break
            if(lim==-1):
                break
            lim+=0.5
    return pairs

def run():
    info='''
    (A)dd players
    (D)elete players
    (G)one players(dont pair for current round)
    (H)elp
    (M)ove players
    (N)ame replace(change name)
    (P)air players
    (Q)uit
    (R)anking display
    (U)pdate database
    '''
    db=parsedb()
    if(db==-1):
        print "An error occured when parsing the database"
        return
    cls=parsecls()
    if(cls==-1):
        print "An error occured when parsing the classes"
        return
    topair=[j for i in cls for j in i[1]]
    updated=0
    while True:
        print "Welcome to Ariana's chess pairing system"
        print "Please input a command:"
        inp=raw_input().lower().strip()
        if(inp=='a'):
            print "Enter player name"
            player=raw_input().strip()
            if(not all(player not in i[1] for i in cls)):
                print "Player already exists"
                continue
            if(player=='Bye'):
                print "Can't take Bye"
            while True:
                print "Enter class"
                pclass=raw_input().strip()
                if(not all(pclass!=i[0] for i in cls)):
                    break
                print "Class not found, do you want to add a new class? Y/N"
                if(raw_input().lower().strip()=='y'):
                    cls.append([pclass,[]])
                    break
            for i in cls:
                if(i[0]==pclass):
                    i[1].append(player)
                    topair.append(player)
                    print "Added player "+player+" to class "+pclass
                    updated=0
                    break
            topair.append(player)
        elif(inp=='d'):
            print "Enter player name"
            player=raw_input().strip()
            for i in cls:
                if player in i[1]:
                    i[1].remove(player)
                    topair.remove(player)
                    print "Removed "+player+" from class "+i[0]
                    updated=0
                    break
        elif(inp=='g'): 
            print "Enter player name"
            player=raw_input().strip()
            if(player not in topair):
                print "Player not found"
                continue
            topair.remove(player)
        elif(inp=='h'):
            print info
        elif(inp=='m'):
            print "Enter player name"
            player=raw_input().strip()
            if(all(player not in i[1] for i in cls)):
                print "Player does exists"
                continue 
            j=0
            for i in xrange(len(cls)):
                if player in cls[i][1]:
                    print "Found "+player+" from class "+cls[i][0]
                    j=i
                    break
            print "Enter class"
            pclass=raw_input().strip()
            if(all(pclass!=i[0] for i in cls)):
                print "Class not found"
            for i in cls:
                if pclass==i[0]:
                    if pclass==cls[j][0]:
                        print "Player is already in "+pclass
                        break
                    cls[j][1].remove(player)
                    i[1].append(player)
                    print "Moved "+player+" from class "+cls[j][0]+" to class "+i[0]       
                    break
        elif(inp=='n'):
            print "Enter player name"
            player=raw_input().strip()
            if(all(player not in i[1] for i in cls)):
                print "Player does exists"
                continue 
            print "Enter new name"
            nname=raw_input().strip()
            if(not all(nname not in i[1] for i in cls)):
                print "Name already exists"
                continue
            if(nname=='Bye'):
                print "Can't take Bye"
            if(player==nname):
                print "The new name is the same"
                continue
            for i in cls:
                for j in xrange(len(i[1])):
                    if(i[1][j]!=player):
                        continue
                    i[1][j]=nname
                    j=-1
                    break
                if(j==-1):
                    break
            for j in xrange(len(topair)):
                if(topair[j]!=player):
                    continue
                topair[j]=nname
                break
            db=[([nname] if i[0]==player else [i[0]])+[([nname] if j[0]==player else [j[0]])+j[1:] for j in i[1:]] for i in db]
            print "Replaced "+player+" with "+nname       
            updated=0
        elif(inp=='p'):
            if(updated==0):
                print "Databases aren't updated yet, do you want to continue Y/N"
                if(raw_input().lower().strip()!='y'):
                    continue
            dbexp=[i for i in gentiebreak(db) if i[0] in topair]
            pairs=[pair([j for j in dbexp if j[0] in i[1]]) for i in cls]
            pairf=open('pairs','w')
            for i in pairs:
                for j in i:
                    pairf.write(j[0]+" - "+j[1]+" : ? - ?\n")
                pairf.write('\n')
            pairf.close()
            print("Paired players")
        elif(inp=='q'):
            if(updated==0):
                print "Databases aren't updated yet, do you want to continue Y/N"
                if(raw_input().lower().strip()!='y'):
                    continue
            print "Quitting program"
            return 0
        elif(inp=='r'):
            print cls
            print db
            print topair
            print 'todo'
        elif(inp=='u'):
            pairs=parsepair()
            if(pairs==-1):
                print "An error occured"
                continue
            for i in []:#pairs
                for j in db:
                    if(j[0]==i[0]):
                        j.append([i[1],'w',i[2]])
                    if(j[0]==i[1]):
                        j.append([i[0],'b',i[3]])
            clf=open('class','w')
            for i in cls:
                clf.write(i[0]+':\n')
                for j in i[1]:
                    clf.write('\t'+j+'\n')
            clf.close()
            dbf=open('mfsdb','w')
            for i in db:
                dbf.write(i[0]+':\n')
                for j in i[1:]:
                    dbf.write('\t'+' '.join(str(k) for k in j)+'\n')
            dbf.close()
            updated=1
        elif(inp==''):
            print info
        else:
            print "Unknown command"

run()
#print parsedb()
#print parsepl()
#print parsepair()
