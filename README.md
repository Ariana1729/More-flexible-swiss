# More-flexible-swiss
A chess pairing system that allows for multiple groups and transfering between, along with tempoarily removing people

## Features

Transfer ppl between classes
Display rankings
Add people/Remove people

## Usage

Run `main.py` to start

Options:
 - (A)dd players
 - (D)elete players
 - (G)one players(dont pair for current round)
 - (H)elp
 - (M)ove players
 - (N)ame replace(change name)
 - (P)air players
 - (Q)uit
 - (R)anking display
 - (U)pdate database

The pairings will be at a file called `pairs`, if you want to swop around people and add people it's perfectly ok as long as the format stays the same

## Technical details

The detials of the current state is stored in `mfsdb` and pairings are at `pairs`. List of players and classes are in `class`

Past databases and pairings are stored in `./Archive/mfsdb[i]` and  `./Archive/pairs[i]`

### Ranking

 - Total score
 - Total wins
 - No. games with black
 - Avg. rating of opponent
 - Sum of opponent's score
 - Position in database

### Database format

Player:
Rd num - opponent \[w/b\] \[score\]
Player:
etc.

### Classes format

Classname:
player
player
etc.
Classname:
player
etc.
etc.

### Pairing format

Player1(white) - Player2(black): ? - ?
etc.

etc.(class2)

etc.

? to be replaced with actual score
Bye is used when there's a odd number of ppl
