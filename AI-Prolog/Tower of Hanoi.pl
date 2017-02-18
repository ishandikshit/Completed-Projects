hanoi(1,P1,P2,_) :-  write('Move '), write(P1), write(' to '), write(P2), nl. 
hanoi(N,P1,P2,P3) :- N>1, M is N-1, hanoi(M,P1,P3,P2), hanoi(1,P1,P2,_), hanoi(M,P3,P2,P1). 