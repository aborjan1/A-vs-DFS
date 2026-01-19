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



def generate_maze(w,h):
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
    return maze

def dfs(maze,start,goal):
    stack=[(start,[start])]
    visited=set()
    while stack:

        (x,y),path=stack.pop()

        
        if (x,y) in visited:
            continue

        if (x,y)==goal:
            yield visited, path
            return

        visited.add((x,y))
        yield visited, None

        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx,ny=x+dx,y+dy

            if maze[ny][nx]==0 and (nx,ny) not in visited:
                stack.append(((nx,ny),path+[(nx,ny)]))

import heapq

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

maze=generate_maze(W,H)
start = (1,1)
goal = (W-2, H-2)

path_gen = dfs(maze, start, goal)
visited = set()
path = None



dfs_gen=dfs(maze,start,goal)
astar_gen=astar(maze,start,goal)
dfs_v=set(); dfs_p=None
astar_v=set(); astar_p=None

running=True

while running:
    clock.tick(30)
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running=False

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
