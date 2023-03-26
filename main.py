from tkinter import messagebox, Tk
import pygame
import sys
import random
import heapq

pygame.font.init()
white = (255, 255, 255)


def throw_instructions():
    Tk().wm_withdraw()
    messagebox.showinfo("Instructions", "-> Right click for creating walls. \n\n -> Left click for removing walls. \n\n"
                                        "-> pink box: Start Box. \n\n -> yellow box: Target Box. \n\n"
                                        " -> To move Start Box : \n "
                                        "---> W: UP \n ---> S: DOWN \n ---> A: LEFT \n ---> D: RIGHT \n\n"
                                        " -> To move Target : \n "
                                        "---> UPArrow: UP \n ---> DOWNArrow: DOWN \n ---> LEFTArrow: LEFT \n"
                                        " --->RIGHRArrow: RIGHT \n\n"
                                        "-> Press SPACE to start search.")


window_width = 1000
window_height = 600

throw_instructions()
window = pygame.display.set_mode((window_width, window_height))

columns = 50
rows = 25

box_width = window_width // columns
box_height = window_height // rows

grid = []
queue = []
path = set()


class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None
        self.f = pygame.font.SysFont('Arial', 15)
        self.wight = random.randint(1, 9)
        self.dist = sys.maxsize

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2))

    def write(self, win, color):
        win.blit(self.f.render(f"{self.wight}", True, color), (self.x * box_width, self.y * box_height))

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])


# Create Grid
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)

# Set Neighbours
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()

# start box
start_box = grid[columns // 2 - 15][rows // 2]
start_box.start = True
start_box.queued = True
start_box.dist = 0
heapq.heappush(queue, (0, start_box.x, start_box.y))

# end box
target_box = grid[columns // 2 + 15][rows // 2]
target_box.target = True


def main(start_box, target_box):
    begin_search = False
    searching = True

    while True:
        for event in pygame.event.get():
            # Quit Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEMOTION and not begin_search:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                # Draw Wall
                if event.buttons[0]:
                    i = x // box_width
                    j = y // box_height

                    if not grid[i][j].target and not grid[i][j].start:
                        grid[i][j].wall = True

                # remove walls
                if event.buttons[2]:
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = False

            if event.type == pygame.KEYDOWN and not begin_search:
                # Start Algorithm
                if event.key == pygame.K_SPACE:
                    begin_search = True

                if event.key == pygame.K_w:
                    cor_i = start_box.x
                    cor_j = start_box.y
                    if cor_j >= 0 and not grid[cor_i][cor_j - 1].wall:
                        grid[cor_i][cor_j].start = False
                        grid[cor_i][cor_j].queued = False
                        grid[cor_i][cor_j].dist = grid[cor_i][cor_j - 1].dist
                        heapq.heappop(queue)
                        start_box = grid[cor_i][cor_j - 1]
                        start_box.start = True
                        start_box.queued = True
                        start_box.dist = 0
                        heapq.heappush(queue, (0, cor_i, cor_j - 1))

                if event.key == pygame.K_a:
                    cor_i = start_box.x
                    cor_j = start_box.y
                    if cor_i >= 0 and not grid[cor_i - 1][cor_j].wall:
                        grid[cor_i][cor_j].start = False
                        grid[cor_i][cor_j].queued = False
                        grid[cor_i][cor_j].dist = grid[cor_i - 1][cor_j].dist
                        heapq.heappop(queue)
                        start_box = grid[cor_i - 1][cor_j]
                        start_box.start = True
                        start_box.queued = True
                        start_box.dist = 0
                        heapq.heappush(queue, (0, cor_i - 1, cor_j))

                if event.key == pygame.K_d:
                    cor_i = start_box.x
                    cor_j = start_box.y
                    if cor_i < columns - 1 and not grid[cor_i + 1][cor_j].wall:
                        grid[cor_i][cor_j].start = False
                        grid[cor_i][cor_j].queued = False
                        grid[cor_i][cor_j].dist = grid[cor_i + 1][cor_j].dist
                        heapq.heappop(queue)
                        start_box = grid[cor_i + 1][cor_j]
                        start_box.start = True
                        start_box.queued = True
                        start_box.dist = 0
                        heapq.heappush(queue, (0, cor_i + 1, cor_j))

                if event.key == pygame.K_s:
                    cor_i = start_box.x
                    cor_j = start_box.y
                    if cor_j < rows - 1 and not grid[cor_i][cor_j + 1].wall:
                        grid[cor_i][cor_j].start = False
                        grid[cor_i][cor_j].queued = False
                        grid[cor_i][cor_j].dist = grid[cor_i][cor_j + 1].dist
                        heapq.heappop(queue)
                        start_box = grid[cor_i][cor_j + 1]
                        start_box.start = True
                        start_box.queued = True
                        start_box.dist = 0
                        heapq.heappush(queue, (0, cor_i, cor_j + 1))

                if event.key == pygame.K_UP:
                    cor_i = target_box.x
                    cor_j = target_box.y
                    if cor_j >= 0 and not grid[cor_i][cor_j - 1].wall:
                        grid[cor_i][cor_j].target = False
                        target_box = grid[cor_i][cor_j - 1]
                        target_box.target = True

                if event.key == pygame.K_DOWN:
                    cor_i = target_box.x
                    cor_j = target_box.y
                    if cor_j < rows - 1 and not grid[cor_i][cor_j + 1].wall:
                        grid[cor_i][cor_j].target = False
                        grid[cor_i][cor_j + 1].target = True
                        target_box = grid[cor_i][cor_j + 1]

                if event.key == pygame.K_LEFT:  # Left for end
                    cor_i = target_box.x
                    cor_j = target_box.y
                    if cor_i >= 0 and not grid[cor_i - 1][cor_j].wall:
                        grid[cor_i][cor_j].target = False
                        grid[cor_i - 1][cor_j].target = True
                        target_box = grid[cor_i - 1][cor_j]

                if event.key == pygame.K_RIGHT:  # Right for end
                    cor_i = target_box.x
                    cor_j = target_box.y
                    if cor_i < columns - 1 and not grid[cor_i + 1][cor_j].wall:
                        grid[cor_i][cor_j].target = False
                        grid[cor_i + 1][cor_j].target = True
                        target_box = grid[cor_i + 1][cor_j]

        if begin_search and searching:
            if len(queue) > 0:
                pair = heapq.heappop(queue)
                d = pair[0]
                current_box = grid[pair[1]][pair[2]]
                current_box.visited = True
                for neighbour in current_box.neighbours:
                    if neighbour.dist > d + neighbour.wight and not neighbour.wall:
                        neighbour.dist = d + neighbour.wight
                        neighbour.prior = current_box
                        neighbour.queued = True
                        heapq.heappush(queue, (neighbour.dist, neighbour.x, neighbour.y))
            else:
                if target_box.dist == sys.maxsize:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There is no solution!")
                    searching = False
                else:
                    current_box = target_box
                    while current_box.prior != start_box:
                        path.add(current_box.prior)
                        current_box = current_box.prior

        window.fill((0, 0, 0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (50, 50, 50))

                if box.queued:
                    box.draw(window, (153, 204, 255))

                if box.visited:
                    box.draw(window, (51, 153, 255))

                box.write(window, white)

                if box in path:
                    box.draw(window, (255, 255, 51))

                if box.start:
                    box.draw(window, (255, 204, 255))

                if box.wall:
                    box.draw(window, (100, 100, 100))

                if box.target:
                    box.draw(window, (255, 255, 51))

        pygame.display.flip()


main(start_box, target_box)
