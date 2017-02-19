edge(a,b,1) .
edge(a,c,6) .
edge(b,a,1) .
edge(b,c,4) .
edge(b,d,3) .
edge(b,e,1) .
edge(c,a,6) .
edge(c,b,4) .
edge(c,d,1) .
edge(d,b,3) .
edge(d,c,1) .
edge(d,e,1) .
edge(e,d,1) .
edge(e,b,1) .

is_path(X,Y,W) :- edge(X,Y,W).

findpath(X,Y,P,W):- check(X,Y,[X],Q,W),reverse(Q,P).
check(X,Y,P,[Y|P],W):- is_path(X,Y,W).

check(X,Y,V,P,W) :- is_path(X,Z,W1), Z\==Y, \+ member(Z,V), check(Z,Y,[Z|V],P,W2), W is W1 + W2.