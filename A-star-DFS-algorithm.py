import pygame, random, heapq # type: ignore


CELL = 22
W, H = 31, 21
WIDTH = W * CELL
HEIGHT = H * CELL * 2 + 60

WHITE=(245,245,245) # Polja
BLACK=(15,15,15) # Zidovi
GRAY=(180,180,180) # Pathfinder
BLUE=(60,120,255) # FoundPath
GREEN=(50,200,120) # Ulaz
RED=(220,70,70) # Izlaz



def generate_map(width, height, room_attempts=40, min_size=3, max_size=7):
    grid = [[1]*width for _ in range(height)]
    rooms = []

    def carve_room(x, y, w, h):
        for yy in range(y, y+h):
            for xx in range(x, x+w):
                grid[yy][xx] = 0

    def carve_h_corridor(x1, x2, y):
        for x in range(min(x1,x2), max(x1,x2)+1):
            grid[y][x] = 0

    def carve_v_corridor(y1, y2, x):
        for y in range(min(y1,y2), max(y1,y2)+1):
            grid[y][x] = 0

    for _ in range(room_attempts):
        w = random.randint(min_size, max_size)
        h = random.randint(min_size, max_size)
        x = random.randint(1, width - w - 2)
        y = random.randint(1, height - h - 2)

        failed = False
        for yy in range(y-1, y+h+1):
            for xx in range(x-1, x+w+1):
                if grid[yy][xx] == 0:
                    failed = True

        if not failed:
            carve_room(x,y,w,h)
            center = (x+w//2, y+h//2)

            if rooms:
                prev = rooms[-1]
                if random.random() < 0.5:
                    carve_h_corridor(prev[0], center[0], prev[1])
                    carve_v_corridor(prev[1], center[1], center[0])
                else:
                    carve_v_corridor(prev[1], center[1], prev[0])
                    carve_h_corridor(prev[0], center[0], center[1])

            rooms.append(center)

    start = rooms[0]
    goal = rooms[-1]
    return grid, start, goal

def generate_big_maze(w,h):
    maze=[[1]*w for _ in range(h)]
    stack=[(1,1)]
    maze[1][1]=0

    while stack:
        x,y=stack[-1]
        dirs=[(2,0),(-2,0),(0,2),(0,-2)]
        random.shuffle(dirs)
        carved=False
        for dx,dy in dirs:
            nx,ny=x+dx,y+dy
            if 0<nx<w-1 and 0<ny<h-1 and maze[ny][nx]==1:
                maze[y+dy//2][x+dx//2]=0
                maze[ny][nx]=0
                stack.append((nx,ny))
                carved=True
                break
        if not carved:
            stack.pop()

    return maze, (1,1), (w-2,h-2)

def generate_hybrid(w,h):
    maze, s, g = generate_big_maze(w,h)
    for _ in range((w*h)//15):
        x=random.randint(1,w-3)
        y=random.randint(1,h-3)
        rw=random.randint(3,6)
        rh=random.randint(3,6)
        for yy in range(y,y+rh):
            for xx in range(x,x+rw):
                if 0<=xx<w and 0<=yy<h:
                    maze[yy][xx]=0
    return maze, s, g


def dfs(maze, start, goal):
    stack = [(start, [start])]
    visited = set()
    h = len(maze)
    w = len(maze[0])

    while stack:
        (x, y), path = stack.pop()

        if (x, y) in visited:
            continue

        visited.add((x, y))
        yield visited, None

        if (x, y) == goal:
            yield visited, path
            return

        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                if maze[ny][nx] == 0 and (nx, ny) not in visited:
                    stack.append(((nx, ny), path + [(nx, ny)]))


def h(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

def astar(maze,start,goal):
    open_set=[]
    heapq.heappush(open_set,(0,start))
    came={}
    g={start:0}
    visited = set()


    while open_set:
        _,cur=heapq.heappop(open_set)

        if cur in visited: 
            continue

        visited.add(cur)
        yield visited,None

        if cur==goal:
            yield visited,reconstruct(came,cur)
            return

        x,y=cur
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx,ny=x+dx,y+dy
            if maze[ny][nx]==1: continue
            nb=(nx,ny)
            tg=g[cur]+1
            if nb not in g or tg<g[nb]:
                came[nb]=cur
                g[nb]=tg
                heapq.heappush(open_set,(tg+h(nb,goal),nb))

def reconstruct(came,cur):
    path=[cur]
    while cur in came:
        cur=came[cur]
        path.append(cur)
    return path[::-1]

def draw_maze(screen,maze,offset_y,visited,path,title):
    font=pygame.font.SysFont("consolas",18)
    screen.blit(font.render(title,True,(20,20,20)),(10,offset_y-28))

    for y in range(H):
        for x in range(W):
            if maze[y][x]==1:
                pygame.draw.rect(screen,BLACK,(x*CELL,y*CELL+offset_y,CELL,CELL),border_radius=4)

    for (x,y) in visited:
        pygame.draw.rect(screen,GRAY,(x*CELL+4,y*CELL+offset_y+4,CELL-8,CELL-8),border_radius=4)

    if path:
        for (x,y) in path:
            pygame.draw.rect(screen,BLUE,(x*CELL+4,y*CELL+offset_y+4,CELL-8,CELL-8),border_radius=6)

    sx,sy=start; gx,gy=goal
    pygame.draw.rect(screen,GREEN,(sx*CELL+3,sy*CELL+offset_y+3,CELL-6,CELL-6),border_radius=6)
    pygame.draw.rect(screen,RED,(gx*CELL+3,gy*CELL+offset_y+3,CELL-6,CELL-6),border_radius=6)


pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
clock=pygame.time.Clock()

def reset_map():
    global maze, start, goal, dfs_gen, astar_gen, dfs_v, dfs_p, astar_v, astar_p

    if map_type == 1:
        maze, start, goal = generate_map(W, H)
    elif map_type == 2:
        maze, start, goal = generate_big_maze(W, H)
    else:
        maze, start, goal = generate_hybrid(W, H)

    dfs_gen = dfs(maze, start, goal)
    astar_gen = astar(maze, start, goal)

    dfs_v=set(); dfs_p=None
    astar_v=set(); astar_p=None

map_type = 1
maze, start, goal = generate_map(W, H)


reset_map()
running=True

while running:

    clock.tick(30)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        if e.type==pygame.KEYDOWN:
            if e.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                reset_map()

            if e.key == pygame.K_1:
                map_type = 1
                reset_map()

            if e.key == pygame.K_2:
                map_type = 2
                reset_map()

            if e.key == pygame.K_3:
                map_type = 3
                reset_map()

    if dfs_p is None:
        try: dfs_v,dfs_p=next(dfs_gen)
        except: pass

    if astar_p is None:
        try: astar_v,astar_p=next(astar_gen)
        except: pass

    screen.fill((220,220,220))
    draw_maze(screen,maze,30,dfs_v,dfs_p,"DFS – pretraživanje prvo u dubinu")
    draw_maze(screen,maze,H*CELL+60,astar_v,astar_p,"A* – heurističko pretraživanje")

    pygame.display.flip()
    


pygame.quit()
