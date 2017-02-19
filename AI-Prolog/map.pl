vtx(1) .
vtx(2) .
vtx(3) .
vtx(4) .
vtx(5) .
vtx(6) .
adj( 1, 2 ).
adj( 1, 3 ).
adj( 1, 4 ).
adj( 1, 6 ).
adj( 2, 3 ).
adj( 2, 5 ).
adj( 3, 6 ).
adj( 3, 4 ).
adj( 4, 5 ).
adj( 4, 6 ).
color( red ).
color( green ).
color( blue ).
color( yellow ).
neighbor( N1, N2 ) :- adj( N1, N2 ).
neighbor( N1, N2 ) :- adj( N2, N1 ).

color_map(L) :- color_map(1, [1,2,3,4,5,6],L).
color_map( [], [] ).
color_map( [N | Ns], [C | Cs] ) :- color_map( Ns, Cs ), C = color( N, Color ), color( Color ),is_pass( C, Cs ).

is_pass( _, [] ).
is_pass( C1, [C2 | Cs] ) :- not( is_fail( C1, C2 )),is_pass( C1, Cs ).

is_fail( color( N1, Color ), color( N2, Color )) :- neighbor( N1, N2 ).