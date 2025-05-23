# Oskars Lintiņš 221RDB434
from collections import deque

# Funkcija, kura nolasa datus no faila un aizpilda labirinta sarakstu ar tiem
def read_maze(filename):
    maze = [] # tiek definēts labirinta saraksts
    with open(filename, 'r') as f: # atver failu lasīšanai, izmantojot 'r'
        for line in f: # cikls, kurš aizpilda labirinta sarakstu ar datiem
            maze.append(list(line.strip())) # pievieno datus sarakstam. Strip tiek izmantots, lai izdēst liekas atstarpes
    return maze # kad funkcija pabeidz darbību, tā atgriež aizpildītu labirinta sarakstu ar datiem

# Funkcija, kura pēc labirinta saraksta aizpildīšanas atrod sākumpuntu 'S' un galapunktu 'G'
def find_points(maze):
    start = finish = None # Sākumā punkti definēti kā
    # ārējais cikls, kurš iziet cauri labirinta rindām 'i'
    for i in range(len(maze)):
        # iekšējais cikls, kurš iziet cauri labirinta kolonnām 'j' rindā 'i'
        for j in range(len(maze[0])):
            if maze[i][j] == 'S':
                start = (i, j) # ja ir atrasts simbols 'S', tad sākumpunktam ir pieškirta 'S' rindas un kolonnas pozīcija
            elif maze[i][j] == 'G':
                finish = (i, j) # ja ir atrasts simbols 'G', tad sākumpunktam ir pieškirta 'S' rindas un kolonnas pozīcija
    return start, finish # kad funkcija pabeidz darbību, tā atgriež sākumpunktu un galapunktu

# Funkcija, kas pārbauda, vai dotās koordinātas ir derīgas
def is_valid(x, y, maze):
    # tiek pārbaudīts vai vērtība nav ārpus labirinta un vai tā ir siena ('X')
    return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] != 'X'

# Funkcija, kurā meklē ceļu, izmantojot Breadth-First Search algoritmu
# kā ieejas datus saņem labirinta sarakstu, sākumpunktu un galapunktu
def bfs(maze, start, finish):
    rows, cols = len(maze), len(maze[0]) # tiek inicializētas rindas un kolonnas vērtības

    # Tiek definēti 8 virzieni : uz augšu, uz apakšu, pa labi, pa kresi un pa visām diagonālēm
    directions = [(-1,0), (1,0), (0,-1), (0,1),
                  (-1,-1), (-1,1), (1,-1), (1,1)]

    queue = deque() # tiek definēta rinda, kura glabās apmeklētos punktus
    queue.append((start[0], start[1], 0, 0)) # rinda satur 'x' un 'y' koordinātes, soļu skaitu un monētu summu 

    # Tiek definēta vārdnīca, kura glabās informāciju par ampleklēto punktu minimālo soļu skaitu un monētu summu
    visited = {}
    visited[start] = (0, 0) # sākumā soļu skaits un monētu summa ir 0

    # cikls, kurš izpildīs savu darbību, kamēr rinda (queue) nebūs tukša
    while queue:
        x, y, steps, coins = queue.popleft()

        # ja x un y koordinātes sakrīt ar galapunktu, tas nozīmē, ka ceļš ir atrasts un cikls beidz savu darbību
        if (x, y) == finish:
            return coins  # kad cikls beidz savu darbību, tas atgriež monētu summu

        # iekšējais cikls, kurš katram virzienam no 'direction' saraksta aprēķina nākamo šūnas x un y koordinātes
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # tiek veikta vērtības pārbaude ar is_valid funkcijas palīdzību
            if is_valid(nx, ny, maze):
                punkts = maze[nx][ny] # ja vērtība ir derīga, tad tā tiek definēta kā 'punkts'
                # Ja 'punkts' ir skaitlis, tad uzskatam, ka tā ir monēta, kura tiek pievienota monētu summai
                if punkts.isdigit():
                    new_coins = coins + int(punkts)
                else:
                    new_coins = coins # ja 'punkts' ir 'S' vai 'G', tad monētu summa nemainās

                new_steps = steps + 1 # tiek palielināts soļu skaits
                # Tiek veikta pārbaude, vai var turpināt ceļu.
                # Ja x un y koordinates nav vārdnīcā 'visited' (jauns ceļš) vai ir, bet tās ir vairāk
                # par jauno soļu skaitu un monētu summu (tāds cēļš būs labāks), tad 
                # vārdnīca tiek atjaunota ar jaunām vērtībām.
                if (nx, ny) not in visited or visited[(nx, ny)] > (new_steps, new_coins):
                    visited[(nx, ny)] = (new_steps, new_coins)
                    # Pievieno rindai jaunas x un y koordinātes, kā arī soļu skaitu un monētu summu
                    queue.append((nx, ny, new_steps, new_coins))

    return -1  # Cikls atgriež kļūdu (-1), ja galapunkts nav sasniedzams

# SĀKUMA DAĻA
# Funkcijai read_maze tiek padots fails ar labirintu, kurš aizpilda maze sarakstu ar datiem no faila
maze = read_maze("maze_11x11.txt")
# Tālāk tiek atrasti sākuma 'S' un beigu 'G' punkti, izmantojot funkciju find_points, kura saņem labirintu kā sarakstu
start, finish = find_points(maze)

# Tiek iegūti gala rezultāti
result = bfs(maze, start, finish)
print(result)
