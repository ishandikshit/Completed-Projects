num_to_word(0,zero).
num_to_word(1,one).
num_to_word(2,two).
num_to_word(3,three).
num_to_word(4,four).
num_to_word(5,five).
num_to_word(6,six).
num_to_word(7,seven).
num_to_word(8,eight).
num_to_word(9,nine).

full_words(0):-!.
full_words(N):- N>0, N1 is N//10, N2 is N mod 10, full_words(N1), 
    num_to_word(N2, Word), print_dash(N1), write(Word) .

print_dash(0):-! .

print_dash(M):- M>0, 
    write('-') .