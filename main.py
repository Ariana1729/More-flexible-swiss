import re

def parsedb(): # get database
    replayer=re.compile('^(.+):\s*$') # Check for playerv
    regame=re.compile('^(.+)(w|b)\s*(\d*\.?\d*)\s*$') # Check for game
    reempty=re.compile('^\s*$') # Check if empty
    dbf=open('mfsdb','r').read().split('\n')
    db=[] # db[i]=[name,[opp. name,color,score]]
    err=0
    for i in dbf:
        player=replayer.match(i)
        game=regame.match(i)
        empty=reempty.match(i)
        if(player):
            db.append([player.group(1).strip()])
        elif(game):
            db[-1].append([game.group(1).strip(),game.group(2),float(game.group(3))])
        elif(empty):
            continue
        else:
            print "Error parsing database "+i
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

def gentiebreak(pl): # generates tie breaks
    return pl

def pair(pl): # Pairs players
    pairs=pl
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
            db=[[nname if i[0]==player else i[0],[[nname if j[0]==player else j[0]]+j[1:] for j in i[1:]]] for i in db]
            print "Replaced "+player+" with "+nname       
            updated=0
        elif(inp=='p'):
            if(updated==0):
                print "Databases aren't updated yet, do you want to continue Y/N"
                if(raw_input().lower().strip()!='y'):
                    continue
            print 'todo'
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
            updated=1
        elif(inp==''):
            print info
        else:
            print "Unknown command"

run()
#print parsedb()
#print parsepl()
#print parsepair()
