:-ensure_loaded("pokemon_list.pl").
:-ensure_loaded("pokemon_info_attacks.pl").
:-ensure_loaded("pokemon_route.pl").

player_starts(0,0).

% TO DO
next_rooms(X,Y,Rooms) :-
    route(M).


/*Predicado next_rooms(X, Y, Rooms):
Identifica os vizinhos de (X, Y)(coordenadas da posição do pokemon inicial)  com base na matriz route(M) em pokemon_route.pl.
Rooms deve ser uma  lista de listas, em que cada lista contém a informação dos Pokémons vizinhos [Id, Name, Level, X, Y, Types], ou seja, o identificador, o nome, o nível, as coordenadas da posição e ainda a lista de tipos desse Pokémon.
?-next_rooms(0, 0, Rooms).
Rooms = [ [19, rattata, 2, 1, 0, [normal]],<
[16, pidgey, 2, 0, 1, [normal, flying]] ]
Deve carregar os outros ficheiros via ensure_loaded.
 Pode criar predicados auxiliares ao predicado next_rooms, mas não pode utilizar nenhum mecanismo do Prolog que não tenha sido lecionado em aula.
*/