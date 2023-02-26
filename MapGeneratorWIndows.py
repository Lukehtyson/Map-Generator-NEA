from math import ceil
import pygame, random, os
pygame.font.init()
pygame.init()
Colours = {"White": (255, 255, 255), "Black": (0, 0, 0), "Blue": (0, 0, 255), "Yellow": (255, 255, 0), "Red": (255, 0, 0), "Green": (0, 51, 0), "Grey": (32, 32, 32)}
font, run, clock = pygame.font.SysFont('Comic Sans MS', 30), bool, pygame.time.Clock()

#window
screen_width, screen_height = 900, 600
window = pygame.display.set_mode((screen_width, screen_height))
window.fill("White")
Backgrounds = [pygame.image.load(
r'C:\Users\Charlie\OneDrive\Documents\Map-Generator-NEA\Pirate Game\Background1.png'), 
pygame.image.load(r'C:\Users\Charlie\OneDrive\Documents\Map-Generator-NEA\Pirate Game\Background2.png')]
Backgrounds[0] = pygame.transform.scale(Backgrounds[0], (screen_width, screen_height))
Backgrounds[1] = pygame.transform.scale(Backgrounds[1], (screen_width, screen_height))

bg_width = Backgrounds[0].get_width()

#default map variables
Grid = []
map_width, map_height = 200, 110
island_number = 10
island_size = 500
#estimated amount of cities generated
city_rate = 5
tile_size = 10
player_colour = "Red"     
border = 1 
waterfront = []
location = 5
found = True
gold = 0

#finds centre of screen
centre_screen = [int(screen_width/2), int(screen_height/2)]
#random start position
start_pos = [round(random.randint(ceil(centre_screen[0] / tile_size) + border, map_width -((ceil(centre_screen[0]/tile_size))*2) - border)) * tile_size, round(random.randint(ceil(centre_screen[1] / tile_size) + border, map_height - ((ceil(centre_screen[1]/tile_size)) * 2)- border )) * tile_size]
#player coordinates on the window (used when player is on edge of map)
player_wxy = [centre_screen[0], centre_screen[1]]
#coordinates of player in pygame
player_pxy = [start_pos[0], start_pos[1]]
#background scrolling coordinates
background_xy = [start_pos[0], start_pos[1]]

menu = False
scroll = [0, bg_width]

#creates a clickable button with given text, size colour and position
class Button:
    def __init__(self, x, y, image, scale):
        self.width = image.get_width()
        self.height = image.get_height()
        self.scale = scale
        self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def draw(self, surface):
        action = False
        
        pos = pygame.mouse.get_pos()
        
        surface.blit(self.image, (self.rect.x, self.rect.y))

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                
            if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
                action = True
        else:
            self.clicked = False
        return action



play_button = Button(100, 200, pygame.image.load(r'C:\Users\Charlie\OneDrive\Documents\Map-Generator-NEA\Pirate Game\start_button.png'), 8)
options_button = Button(100, 200, pygame.image.load(r'C:\Users\Charlie\OneDrive\Documents\Map-Generator-NEA\Pirate Game\options_button.png'), 8)
quit_button = Button(100, 400, pygame.image.load(r'C:\Users\Charlie\OneDrive\Documents\Map-Generator-NEA\Pirate Game\quit_button.png'), 8)
small_map_button = Button(180, 200, pygame.image.load(r'C:\Users\Charlie\OneDrive\Documents\Map-Generator-NEA\Pirate Game\small_map.png'), 8)
medium_map_button = Button(380, 200, pygame.image.load(r'C:\Users\Charlie\OneDrive\Documents\Map-Generator-NEA\Pirate Game\medium_map.png'), 8)
large_map_button = Button(580, 200, pygame.image.load(r'C:\Users\Charlie\OneDrive\Documents\Map-Generator-NEA\Pirate Game\large_map.png'), 8)
# map_ui = pygame.image.load(r'C:\Users\Charlie\OneDrive\Documents\Map-Generator-NEA\Pirate Game\map_size_button.png')
# map_ui = pygame.transform.scale(window, (200,100))
selected_ui = pygame.image.load(r'C:\Users\Charlie\OneDrive\Documents\Map-Generator-NEA\Pirate Game\selected_button.png')

#settings_button = Button()

#creates a tile with position on the grid 
class Tile():
    def __init__(self, x, y, type):
        #x and y position on the grid for tile
        self.x = x
        self.y = y
        #each tile has a designated terrain type
        self.type = type
        #list of neighbouring tiles
        self.neighbours = []
        self.surrounding_land = 0
        self.surrounding_cities = 0

    def Draw(self, tile_size, background_xy):
        if self.type == "Ocean":
            colour = "Blue"
        if self.type == "Jungle":
            colour = "Green"
        if self.type == "waterfront":
            colour = "Yellow"
        if self.type == "City":
            colour = "Grey"
        if self.type == "Abyss":
            colour = "Black"
        pygame.draw.rect(window, colour, (self.x * tile_size - background_xy[0], self.y * tile_size - background_xy[1], tile_size, tile_size))

#finds neighbouring tiles 
def FindNeighbours(Grid, x, y):

    Grid[x][y].surrounding_land = 0
    Grid[x][y].surrounding_cities = 0

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
        if Grid[x][y].neighbours[i] == "Jungle" or Grid[x][y].neighbours[i] == "waterfront":
            Grid[x][y].surrounding_land += 1
        if Grid[x][y].neighbours[i] == "City":
            Grid[x][y].surrounding_cities += 1

#on-screen text
def RenderFont(player_tile, background_xy, player_xy):
    tiledisplay = font.render(str(player_tile.type),  False, "Black")
    font_pxy = font.render('player' + str(background_xy),  False, ("Black"))
    font_cxy = font.render('gold ' + str(gold),  False, ("Black"))
    window.blit(font_cxy, (15,50))
    window.blit(font_pxy, (15,10))
    #window.blit(tiledisplay, (15,90))

#creates a random shape of a specified tile on the grid
def CreateShape(size, terraintype, start_x, start_y, map_width, map_height, border):

    #forms a path through the grid 
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

def CityFound():
    global menu
    menu = True
    while menu:
        if quit_button.draw(window):
            menu = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
def SpawnTreasure(player_xy):
    global found
    global location
    global gold
    if found:
        location = random.randint(0,len(waterfront)-1)
        found = False
    pygame.draw.rect(window, player_colour, (waterfront[location].x * tile_size - background_xy[0], waterfront[location].y * tile_size - background_xy[1], tile_size, tile_size))
    if abs(player_xy[0] - (waterfront[location].x) ) < 3 and abs(player_xy[1] - waterfront[location].y) < 3:
        gold = gold + 1
        found = True

def DrawGrid():
    for x in range(map_width):
        for y in range(map_height):
            Grid[x][y].Draw(tile_size, background_xy)

#handles player movement with the WASD keys
def PlayerMovement(player_tile):
    keys = pygame.key.get_pressed()
    global tile_size
    #left
    if player_tile.neighbours[1] == "Ocean" and keys[pygame.K_a] and not (keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]):
        if player_wxy[0] == centre_screen[0]:
            if background_xy[0] > 0: 
                background_xy[0] -= tile_size
        player_pxy[0] -= tile_size
    #right
    if player_tile.neighbours[0] == "Ocean" and keys[pygame.K_d] and not (keys[pygame.K_a] or keys[pygame.K_w] or keys[pygame.K_s]):
        if player_wxy[0] == centre_screen[0]:
            if background_xy[0] < (map_width * tile_size) - screen_width:
                background_xy[0] += tile_size
        player_pxy[0] += tile_size
    #up
    if player_tile.neighbours[3] == "Ocean" and keys[pygame.K_w] and not (keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_s]):
        if player_wxy[1] == centre_screen[1]:
            if background_xy[1] > 0:
                background_xy[1] -= tile_size
        player_pxy[1] -= tile_size
    #down
    if player_tile.neighbours[2] == "Ocean" and keys[pygame.K_s] and not (keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w]):
        if player_wxy[1] == centre_screen[1]:
            if background_xy[1] < (map_height * tile_size) - screen_height:
                background_xy[1] += tile_size
        player_pxy[1] += tile_size

    #handles player movement near map borders
    for p in range (0,2):
        if player_pxy[p] < background_xy[p]:
            player_wxy[p] = player_pxy[p] + centre_screen[p]
        elif player_pxy[p] > background_xy[p]:
            player_wxy[p] = player_pxy[p] - background_xy[p] + centre_screen[p]
        else:
            player_wxy[p] = centre_screen[p]

    if player_tile.neighbours[1] == "City" and keys[pygame.K_a]:
        CityFound()
    if player_tile.neighbours[0] == "City" and keys[pygame.K_d]:
        CityFound()
    if player_tile.neighbours[2] == "City" and keys[pygame.K_s]:
        CityFound()
    if player_tile.neighbours[3] == "City" and keys[pygame.K_w]:
        CityFound()

def CreateMap(map_width, map_height, islands, island_size, cityrate):
    global Grid
    c = 0
    
    Grid = [[Tile(x,y, "Ocean") for y in range(map_height)] for x in range(map_width)]

    #generates islands
    for a in range (islands):
        xy = [random.randint(border, map_width-border), random.randint(border, map_height - border)]
        CreateShape(island_size * 2, "Jungle", xy[0], xy[1], map_width, map_height, border)
            

    #smoothing
    for a in range(0,2):
        for x in range(border, map_width-border):
            for y in range(border, map_height-border):
                FindNeighbours(Grid, x, y)
                if Grid[x][y].surrounding_land > 4:
                    Grid[x][y].type = "Jungle"
                if Grid[x][y].surrounding_land < 3:
                    Grid[x][y].type = "Ocean"
                if Grid[x][y].surrounding_land < 7 and Grid[x][y].type == "Jungle":
                    Grid[x][y].type = "waterfront" 
                if Grid[x][y].surrounding_land > 2 and Grid[x][y].surrounding_land < 6 and Grid[x][y].type == "waterfront":
                    waterfront.append(Grid[x][y])  
                
    #generates cities
    for x in range(0, cityrate):
        position = random.randint(0,len(waterfront)-1)
        waterfront[position].type = "City"
        CreateShape(20, "City", waterfront[position].x, waterfront[position].y, map_width, map_height, border)

    #city smoothing
    for x in range(border, map_width-border):
        for y in range(border, map_height-border):
            FindNeighbours(Grid, x, y)
            if Grid[x][y].type == "City":
                if Grid[x][y].surrounding_cities < 3:
                    if Grid[x][y].surrounding_land > 5:
                        Grid[x][y].type = "waterfront"
                    if Grid[x][y].surrounding_land < 6:
                        Grid[x][y].type = "Ocean"

    #creates borders for map
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

def Settings():
    # selected = -100
    run = True
    while run == True:
        for s in range(2):
            window.blit(Backgrounds[s], (scroll[s], 0))
            scroll[s] -= 2
            if abs(scroll[s]) > bg_width:
                scroll[s] = bg_width
        if small_map_button.draw(window):
            map_width = 150
            map_height = 100
            run = False
            # selected = 100

        if medium_map_button.draw(window):
            map_width = 200
            map_height = 150
            run = False
            # selected = 300

        if large_map_button.draw(window):
            map_width = 300
            map_height = 250
            run = False
            # selected = 500

        # window.blit(map_ui, (100, 300))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        # window.blit(selected_ui, (selected, 430))
        
def TitleScreen():
    global run
    
    for s in range(2):
        window.blit(Backgrounds[s], (scroll[s], 0))
        scroll[s] -= 2
        if abs(scroll[s]) > bg_width:
            scroll[s] = bg_width
    
    if play_button.draw(window):
        
        run = False


    if quit_button.draw(window):
        run = False
        pygame.quit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.update()


def Main(): 
    global player_pxy
    global background_xy
    global run
    run = True
    while run:
        TitleScreen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    Settings()
    CreateMap(map_width, map_height, island_number, island_size, city_rate)

    #ensures player spawns in ocean terrain
    for i in range(0,5):
        player_xy = [int((player_pxy[0]+ centre_screen[0]) / tile_size), int((player_pxy[1]+ centre_screen[1]) / tile_size)]
        player_tile = Grid[player_xy[0]][player_xy[1]]

        if player_tile.type != "Ocean":
            start_pos = [round(random.randint(ceil(centre_screen[0] / tile_size) + border, map_width -((ceil(centre_screen[0]/tile_size))*2) - border)) * tile_size, round(random.randint(ceil(centre_screen[1] / tile_size) + border, map_height - ((ceil(centre_screen[1]/tile_size)) * 2)- border )) * tile_size]
            player_pxy = [start_pos[0], start_pos[1]]
            background_xy = [start_pos[0], start_pos[1]]

    FPS = 60

    run = True
    while run:
        clock.tick(FPS)

        #finds the tile the player is currently on
        player_xy = [round((player_pxy[0]+ centre_screen[0]) / tile_size), round((player_pxy[1]+ centre_screen[1]) / tile_size)]
        player_tile = Grid[player_xy[0]][player_xy[1]]
        
        DrawGrid()
        SpawnTreasure(player_xy)
        if menu == False:
            PlayerMovement(player_tile)
            RenderFont(player_tile, background_xy, player_xy)

        

        #player
        pygame.draw.rect(window, player_colour, (player_wxy[0], player_wxy[1], tile_size, tile_size))


        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    Main()
