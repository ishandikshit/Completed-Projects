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

path(X,Z,W,[X,Z]):-edge(X,Z,W).
path(X,Z,W,[X,Y|L]):-edge(X,Y,W1), path(Y,Z,W2,[Y|L] ), W is W1+W2 .