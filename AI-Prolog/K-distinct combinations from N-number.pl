combination(0,_,[]).
combination(N,L,[X|Z]) :- N > 0,el(X,L,R), K1 is N-1, combination(K1,R,Z).
el(X,[X|L],L).
el(X,[_|L],R) :- el(X,L,R).