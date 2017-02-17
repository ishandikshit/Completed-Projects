goldbach(N):-goldbach(3,N).
goldbach(X,N):- is_prime(X), Y is N-X, is_prime(Y), write(X), write(', '), write(Y), !.
goldbach(X,N):- X<N, X1 is X+1, goldbach(X1, N) .

is_prime(2).
is_prime(3).
is_prime(P) :- integer(P), P > 3, P mod 2 =\= 0, \+ has_factor(P,3). 
has_factor(N,L) :- N mod L =:= 0.
has_factor(N,L) :- L * L < N, L2 is L + 2, has_factor(N,L2).