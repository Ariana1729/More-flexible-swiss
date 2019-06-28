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
    topair=db
    db=gentiebreak(db)
    print "Welcome to Ariana's chess pairing system"
    print "Please input a command:"
    while True:
        inp=raw_input().lower().strip()
        if(inp=='a'):
            a
        elif(inp=='d'):
            a
        elif(inp=='g'):
            a
        elif(inp=='h'):
            print info
        elif(inp=='m'):
            a
        elif(inp=='n'):
            a
        elif(inp=='p'):
            a
        elif(inp=='q'):
            print "Quitting program"
            return 0
        elif(inp=='r'):
            a
        elif(inp=='u'):
            pairs=parsepair()
            if(pairs==-1):
                print "An error occured"
                continue
        elif(inp==''):
            print info
        else:
            print "Unknown command"

#print parsedb()
#print parsepl()
#print parsepair()
