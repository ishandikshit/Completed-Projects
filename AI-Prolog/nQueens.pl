queens(N,Qs) :- in_between(1,N,Ns), 
    queens(Ns,[],Qs).
queens([],Qs,Qs).
queens(Q1,Q2,Qs) :- select(Q1,UQ1,Q), is_safe(Q2,Q), queens(UQ1,[Q|Q2],Qs). %tail-recursion
is_safe(QXs,Q) :- is_safe(QXs,Q,1).
is_safe([],_,_) :- !.
is_safe([Y|Ys],X,N) :- X =\= Y+N, X =\= Y-N, N1 is N+1, is_safe(Ys,X,N1).
select([Q1|Q1s],Q1s,Q1).
select([Q2|Q2s],[Q2|Q3s],Q) :- select(Q2s,Q3s,Q).
in_between(N,N,[N]) :- !.
in_between(M,N,[M|Ns]) :- M < N, M1 is M+1, in_between(M1,N,Ns).