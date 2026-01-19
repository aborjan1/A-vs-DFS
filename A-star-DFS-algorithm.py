import pygame, random

CELL = 24
W, H = 31, 21
WIDTH, HEIGHT = W*CELL, H*CELL
WHITE=(245,245,245)
BLACK=(15,15,15)

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

pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
maze=generate_maze(W,H)
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
                pygame.draw.rect(screen,BLACK,(x*CELL,y*CELL,CELL,CELL),border_radius=4)
    pygame.display.flip()

pygame.quit()
