combination(0,_,[]).
combination(N,L,[X|Z]) :- N > 0,elem(X,L,R), K1 is N-1, combination(K1,R,Z).
elem(X,[X|L],L).
elem(X,[_|L],R) :- elem(X,L,R).