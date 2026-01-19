import pygame, random # type: ignore

CELL = 24
W, H = 31, 21
WIDTH, HEIGHT = W*CELL, H*CELL
WHITE=(245,245,245)
BLACK=(15,15,15)
GREEN = (50,200,120) # Ulaz
RED = (220,70,70) # Izlaz



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
        if (x,y)==goal:
            return path
        if (x,y) in visited:
            continue
        visited.add((x,y))
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx,ny=x+dx,y+dy
            if maze[ny][nx]==0:
                stack.append(((nx,ny),path+[(nx,ny)]))

pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))

maze=generate_maze(W,H)

start = (1,1)
goal = (W-2, H-2)
path = dfs(maze, start, goal)

clock=pygame.time.Clock()
running=True

while running:
    clock.tick(60)
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running=False

    screen.fill(WHITE)
    for y in range(H):
        for x in range(W):
            if maze[y][x]==1:
                pygame.draw.rect(
                    screen,
                    BLACK,
                    (x*CELL,y*CELL,CELL,CELL),
                    border_radius=4
                )

    sx, sy = start
    pygame.draw.rect(
        screen,
        GREEN,
        (sx*CELL+3, sy*CELL+3, CELL-6, CELL-6),
        border_radius=6
    )
    
    gx, gy = goal
    pygame.draw.rect(
        screen,
        RED,
        (gx*CELL+3, gy*CELL+3, CELL-6, CELL-6),
        border_radius=6
    )
    for (x,y) in path:
        pygame.draw.rect(
            screen,
            (60,120,255),
            (x*CELL+5, y*CELL+5, CELL-10, CELL-10),
            border_radius=6
        )
    pygame.display.flip()
    


pygame.quit()
