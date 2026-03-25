:-ensure_loaded("pokemon_list.pl").
:-ensure_loaded("pokemon_info_attacks.pl").
:-ensure_loaded("pokemon_route.pl").

player_starts(0,0).


% o caso mais simples é quando o pokemon se encontra na posição inicial (0,0)
next_rooms(X,Y,Rooms) :-
    route(M),
    findall(
        [Id,Name,Level,NX,NY,Types], 
        (neighbour_position(X,Y,NX,NY), pokemon_at(NX,NY,M,Id,Level),pokemon(Id,Name,Types)),
        Rooms).


% estabelecer vizinhança (sem diagonais)
neighbour_position(X,Y,NX,NY):-
    NX is X-1,
    NY is Y.

neighbour_position(X,Y,NX,NY):-
    NX is X+1,
    NY is Y.

neighbour_position(X,Y,NX,NY):-
    NX is X,
    NY is Y-1.

neighbour_position(X,Y,NX,NY):-
    NX is X,
    NY is Y+1.

% pokemon na posição
pokemon_at(X,Y,M,Id,Level):-
    element(Y,M,Linha),
    element(X,Linha,(Id,Level)).


element(0,[X|_],X).
element(N,[_|T], Y):-
    N > 0,
    M is N-1,
    element(M,T,Y).
