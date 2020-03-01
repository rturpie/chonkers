import random

# How big the grid is
GRID_WIDTH = random.randint(50,120)
GRID_HEIGHT = random.randint(50,120)

# Parameters for cellular automata
CHANCE_TO_START_ALIVE = 0.4
DEATH_LIMIT = 3
BIRTH_LIMIT = 4
NUMBER_OF_STEPS = 4


def create_grid(width, height):
    """ Create a two-dimensional grid of specified size. """
    return [[0 for _x in range(width)] for _y in range(height)]


def initialize_grid(grid):
    """ Randomly set grid locations to on/off based on chance. """
    height = len(grid)
    width = len(grid[0])
    for row in range(height):
        for column in range(width):
            if random.random() <= CHANCE_TO_START_ALIVE:
                grid[row][column] = 1


def count_alive_neighbors(grid, x, y):
    """ Count neighbors that are alive. """
    height = len(grid)
    width = len(grid[0])
    alive_count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            neighbor_x = x + i
            neighbor_y = y + j
            if i == 0 and j == 0:
                continue
            elif neighbor_x < 0 or neighbor_y < 0 or neighbor_y >= height or neighbor_x >= width:
                # Edges are considered alive. Makes map more likely to appear naturally closed.
                alive_count += 1
            elif grid[neighbor_y][neighbor_x] == 1:
                alive_count += 1
    return alive_count


def do_simulation_step(old_grid):
    """ Run a step of the cellular automaton. """
    height = len(old_grid)
    width = len(old_grid[0])
    new_grid = create_grid(width, height)
    for x in range(width):
        for y in range(height):
            alive_neighbors = count_alive_neighbors(old_grid, x, y)
            if old_grid[y][x] == 1:
                if alive_neighbors < DEATH_LIMIT:
                    new_grid[y][x] = 0
                else:
                    new_grid[y][x] = 1
            else:
                if alive_neighbors > BIRTH_LIMIT:
                    new_grid[y][x] = 1
                else:
                    new_grid[y][x] = 0
    return new_grid

def location_name(level):
    name = ""
    adj1 = ["borkest", "ultimate", "increbily bopping", "soulful"]
    adj2= ["borky", "hopeful", "sunset"]
    places = ["fields", "meadows", "beaches", "gardens"]
    adj3 = ["bork", "love", "respect", "boop"]

    n_adj1 = level - 2
    for _ in range(n_adj1):
        name = name + adj1[random.randint(0,len(adj1)-1)] + "_"
    name = name + adj2[random.randint(0,len(adj2)-1)] + "_"
    name = name + places[random.randint(0,len(places)-1)]
    if level > 1:
        name = name + "_of_" + adj3[random.randint(0,len(adj3)-1)]
    return name

def enemy_name():
    return "bork bork's best friend"

def gen_enemies(grid):
    enemies = []
    for i in range(random.randint(60,100)):
        ax = random.randint(0, len(grid[0])-1)
        ay = random.randint(0, len(grid)-1)

        while grid[ay][ax] == 0:
            ax = random.randint(0, len(grid[0])-1)
            ay = random.randint(0, len(grid)-1)

        name = enemy_name()
        enemies.append((ax,ay,name+str(i)))
    return enemies


def generate_cave(blocks, level):
    # Create cave system using a 2D grid
    global GRID_WIDTH
    global GRID_HEIGHT

    GRID_WIDTH = random.randint(50,120)
    GRID_HEIGHT = random.randint(50,120) 

    grid = create_grid(GRID_WIDTH, GRID_HEIGHT)
    initialize_grid(grid)
    for _ in range(NUMBER_OF_STEPS):
        grid = do_simulation_step(grid)

    # pick random points and check connectivity
    ax = random.randint(0, len(grid[0])-1)
    ay = random.randint(0, len(grid)-1)
    bx = random.randint(0, len(grid[0])-1)
    by = random.randint(0, len(grid)-1)

    while grid[ay][ax] == 1:
        ax = random.randint(0, len(grid[0])-1)
        ay = random.randint(0, len(grid)-1)

    while grid[by][bx] == 1:
        bx = random.randint(0, len(grid[0])-1)
        by = random.randint(0, len(grid)-1)

    x = lambda a: list(map(lambda q: -1 if q == 0 else q, a))
    y = lambda a: list(map(lambda q: blocks[0] if q == 1 else q, a))
    z = lambda a: list(map(lambda q: blocks[1] if q == -1 else q, a))
    grid = list(map(x,grid))
    grid = list(map(y,grid))
    grid = list(map(z,grid))

    name = location_name(level)
    enemies = gen_enemies(grid)

    with open('locations/%s.map' % name,'w') as f:
        for line in grid:
            f.write(''.join(list(map(str,line)))+"\n")
    print(enemies)
    return (name, (ax,ay), (bx,by), enemies)