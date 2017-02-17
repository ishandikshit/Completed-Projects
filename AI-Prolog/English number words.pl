numberword(0,zero).
numberword(1,one).
numberword(2,two).
numberword(3,three).
numberword(4,four).
numberword(5,five).
numberword(6,six).
numberword(7,seven).
numberword(8,eight).
numberword(9,nine).

fullword(0):-!.
fullword(N):- N>0, 
    N1 is N//10, 
    N2 is N mod 10, 
    fullword(N1), 
    numberword(N2, Word), 
	print_dash(N1),
    write(Word) .

print_dash(0):-! .

print_dash(M):- M>0, 
    write('-') .