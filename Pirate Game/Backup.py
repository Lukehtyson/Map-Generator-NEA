from math import ceil
import pygame, random, os
pygame.font.init()
screen_width = 900
screen_height = 500
Colours = {"White": (255, 255, 255), "Black": (0, 0, 0), "Blue": (0, 0, 255), "Yellow": (255, 255, 0), "Red": (255, 0, 0), "Green": (0, 51, 0), "Grey": (32, 32, 32)}
window = pygame.display.set_mode((screen_width, screen_height))
window.fill("White")
Clock = pygame.time.Clock()
run = bool
font = pygame.font.SysFont('Comic Sans MS', 30)

#default map variables
Grid = []
map_width, map_height = 200, 110
island_number = 15
island_size = 400
#estimated amount of cities generated
city_rate = 5
tile_size = 10
player_colour = "Red"     
border = 1 

#finds centre of screen
centre_screen = [int(screen_width/2), int(screen_height/2)]

start_pos = [round(random.randint(ceil(centre_screen[0] / tile_size) + border, map_width -((ceil(centre_screen[0]/tile_size))*2) - border)) * tile_size, round(random.randint(ceil(centre_screen[1] / tile_size) + border, map_height - ((ceil(centre_screen[1]/tile_size)) * 2)- border )) * tile_size]
#player coordinates on the window
window_pxy = [centre_screen[0], centre_screen[1]]
#player coordinates on the game map
player_xy = [start_pos[0], start_pos[1]]
#coordinates of player on grid
grid_pxy = [0,0]
#coordinates of the camera
camera_xy = [start_pos[0], start_pos[1]]


class Button:
    def __init__(self, text, fontsize, x, y, width, height, colour):
        self.font = pygame.font.SysFont('Comic Sans MS', fontsize)
        self.text = self.font.render(text,  False,  "Black")
        self.clicked = False
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.colour = colour
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        action = False
        pos = pygame.mouse.get_pos()
        pygame.draw.rect(window, self.colour, self.rect)
        window.blit(self.text, (self.x + 10, self.y))
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        return action

#creates buttons
text = "Start"
play_button = Button(text, 60, 200, 200, 200, 80, "Grey")
text = "Quit"
quit_button = Button(text, 60, 200, 400, 200, 80, "Grey")
text = "Settings"
settings_button = Button(text, 60, 200, 300, 200, 80, "Grey")

class Tile():
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.neighbours = []
        self.land_count = 0
        self.city_count = 0
    def Draw(self, tile_size, camera_xy):
        if self.type == "Ocean":
            colour = "Blue"
        if self.type == "Jungle":
            colour = "Green"
        if self.type == "Beach":
            colour = "Yellow"
        if self.type == "City":
            colour = "Grey"
        if self.type == "Abyss":
            colour = "Black"
        pygame.draw.rect(window, colour, (self.x * tile_size + (camera_xy[0] * -1), self.y * tile_size - camera_xy[1], tile_size, tile_size))

#finds neighbouring tiles 
def FindNeighbours(Grid, x, y):
    Grid[x][y].land_count = 0
    Grid[x][y].city_count = 0

    Grid[x][y].neighbours = [
    Grid[x+1][y].type, 
    Grid[x-1][y].type, 
    Grid[x][y+1].type,
    Grid[x][y-1].type,
    Grid[x+1][y+1].type,
    Grid[x+1][y-1].type, 
    Grid[x-1][y+1].type,
    Grid[x-1][y-1].type]
    
    for i in range(0, 8):
        if Grid[x][y].neighbours[i] == "Jungle" or Grid[x][y].neighbours[i] == "Beach":
            Grid[x][y].land_count += 1
        if Grid[x][y].neighbours[i] == "City":
            Grid[x][y].city_count += 1

def RenderFont(player_tile, camera_xy):
    tiledisplay = font.render(str(player_tile.type),  False, "Black")
    coordinates = font.render(str(player_xy),  False, ("Black"))
    window.blit(coordinates, (15,10))
    window.blit(tiledisplay, (15,50))

#creates a random shape of a specified tile on the grid
def CreateShape(size, terraintype, start_x, start_y, map_width, map_height, border):

    for i in range(size):
        Grid[start_x][start_y].type = terraintype
        roll = random.randint(1,4)
        if roll == 1 and start_x > border:
            start_x += -1
        if roll == 2 and start_x < map_width -1 - border:
            start_x += 1
        if roll == 3 and start_y < map_height - border:
            start_y += 1
        if roll == 4 and start_y >  border:
            start_y += -1

def DrawGrid(map_width, map_height, tile_size, camera_xy):
    for x in range(map_width):
        for y in range(map_height):
            Grid[x][y].Draw(tile_size, camera_xy)

def PlayerMovement(player_tile, window_pxy, centre_screen, camera_xy, tile_size, player_xy, map_width, map_height):
    keys = pygame.key.get_pressed()
    #left
    if player_tile.neighbours[1] == "Ocean" and keys[pygame.K_a] and not (keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]):
            if window_pxy[0] == centre_screen[0]:
                if camera_xy[0] > 0:
                    camera_xy[0] -= tile_size
            if player_xy[0] > camera_xy[0] - centre_screen[0]:
                player_xy[0] -= tile_size
    #right
    if player_tile.neighbours[0] == "Ocean" and keys[pygame.K_d] and not (keys[pygame.K_a] or keys[pygame.K_w] or keys[pygame.K_s]):
        if window_pxy[0] == centre_screen[0]:
            if camera_xy[0] < (map_width * tile_size) - screen_width:
                camera_xy[0] += tile_size
        if player_xy[0] < (map_width * tile_size) - centre_screen[0] -tile_size :
            player_xy[0] += tile_size
    #up
    if player_tile.neighbours[3] == "Ocean" and keys[pygame.K_w] and not (keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_s]):
        if window_pxy[1] == centre_screen[1]:
            if camera_xy[1] > 0:
                camera_xy[1] -= tile_size
        if player_xy[1] > camera_xy[1] - centre_screen[1]:
            player_xy[1] -= tile_size
    #down
    if player_tile.neighbours[2] == "Ocean" and keys[pygame.K_s] and not (keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w]):
        if window_pxy[1] == centre_screen[1]:
            if camera_xy[1] < (map_height * tile_size) - screen_height:
                camera_xy[1] += tile_size
        if player_xy[1] < (map_height * tile_size) - centre_screen[1] -tile_size :
            player_xy[1] += tile_size

    #handles player movement at map borders
    for p in range (0,2):
        if player_xy[p] < camera_xy[p]:
            window_pxy[p] = player_xy[p] + centre_screen[p]
        elif player_xy[p] > camera_xy[p]:
            window_pxy[p] = player_xy[p] - camera_xy[p] + centre_screen[p]
        else:
            window_pxy[p] = centre_screen[p]

def CreateMap(map_width, map_height, islands, islandsize, cityrate):
    global Grid
    c = 0
    cityareas = []
    Grid = [[Tile(x,y, "Ocean") for y in range(map_height)] for x in range(map_width)]

    #generates islands
    for a in range (islands):
        xy = [random.randint(border, map_width-border), random.randint(border, map_height - border)]
        CreateShape(islandsize * 2, "Jungle", xy[0], xy[1], map_width, map_height, border)
            

    #smoothing
    for a in range(0,2):
        for x in range(border, map_width-border):
            for y in range(border, map_height-border):
                FindNeighbours(Grid, x, y)
                if Grid[x][y].land_count > 4:
                    Grid[x][y].type = "Jungle"
                if Grid[x][y].land_count < 3:
                    Grid[x][y].type = "Ocean"
                if Grid[x][y].land_count < 7 and Grid[x][y].type == "Jungle":
                    Grid[x][y].type = "Beach" 
                if Grid[x][y].land_count > 2 and Grid[x][y].land_count < 6 and Grid[x][y].type == "Beach":
                    cityareas.append(Grid[x][y])  
                
    #generates cities
    for x in range(0, cityrate):
        position = random.randint(0,len(cityareas)-1)
        cityareas[position].type = "City"
        CreateShape(20, "City", cityareas[position].x, cityareas[position].y, map_width, map_height, border)

    #city smoothing
    for x in range(border, map_width-border):
        for y in range(border, map_height-border):
            FindNeighbours(Grid, x, y)
            if Grid[x][y].type == "City":
                if Grid[x][y].city_count < 3:
                    if Grid[x][y].land_count > 5:
                        Grid[x][y].type = "Beach"
                    if Grid[x][y].land_count < 6:
                        Grid[x][y].type = "Ocean"

    #creates borders
    for x in range(0,border):
        for y in range(0, map_height):
            Grid[x][y].type = "Abyss"
    for x in range(map_width - border, map_width):
        for y in range(0, map_height):
            Grid[x][y].type = "Abyss"
    for y in range(0,border):
        for x in range(0, map_width):
            Grid[x][y].type = "Abyss"
    for y in range(map_height - border, map_height):
        for x in range(0, map_width):
            Grid[x][y].type = "Abyss"
    
    #finalises tile placement                    
    for x in range(border, map_width-border):
        for y in range(border, map_height-border):
            FindNeighbours(Grid, x, y)

def TitleScreen():
    global run
    
    if play_button.draw(window):
        CreateMap(map_width, map_height, island_number, island_size, city_rate)
        run = False

    #if settings_button.draw(window):
        #Settings()

    if quit_button.draw(window):
        run = False
        pygame.quit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.update()


def Main(): 

    global run
    run = True
    while run:
        TitleScreen()

    FPS = 60

    run = True
    while run:
        Clock.tick(FPS)

        grid_pxy = [int((player_xy[0]+ centre_screen[0]) / 10), int((player_xy[1]+ centre_screen[1]) / 10)]
        player_tile = Grid[grid_pxy[0]][grid_pxy[1]]

        if player_tile.type != "Ocean":
            camera_xy[0] += tile_size * 3
            player_xy[0] += tile_size * 3

        
        
        PlayerMovement(player_tile, window_pxy, centre_screen, camera_xy, tile_size, player_xy, map_width, map_height)
        DrawGrid(map_width, map_height, tile_size, camera_xy)
        RenderFont(player_tile, camera_xy)


        pygame.draw.rect(window, player_colour, (window_pxy[0], window_pxy[1], tile_size, tile_size))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    Main()
