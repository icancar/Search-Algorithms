import pygame
import os
import config


class BaseSprite(pygame.sprite.Sprite):
    images = dict()

    def __init__(self, row, col, file_name, transparent_color=None):
        pygame.sprite.Sprite.__init__(self)
        if file_name in BaseSprite.images:
            self.image = BaseSprite.images[file_name]
        else:
            self.image = pygame.image.load(os.path.join(config.IMG_FOLDER, file_name)).convert()
            self.image = pygame.transform.scale(self.image, (config.TILE_SIZE, config.TILE_SIZE))
            BaseSprite.images[file_name] = self.image
        # making the image transparent (if needed)
        if transparent_color:
            self.image.set_colorkey(transparent_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (col * config.TILE_SIZE, row * config.TILE_SIZE)
        self.row = row
        self.col = col


class Agent(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Agent, self).__init__(row, col, file_name, config.DARK_GREEN)

    def move_towards(self, row, col):
        row = row - self.row
        col = col - self.col
        self.rect.x += col
        self.rect.y += row

    def place_to(self, row, col):
        self.row = row
        self.col = col
        self.rect.x = col * config.TILE_SIZE
        self.rect.y = row * config.TILE_SIZE

    # game_map - list of lists of elements of type Tile
    # goal - (row, col)
    # return value - list of elements of type Tile
    def get_agent_path(self, game_map, goal):
        pass


class ExampleAgent(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]

        row = self.row
        col = self.col
        while True:
            if row != goal[0]:
                row = row + 1 if row < goal[0] else row - 1
            elif col != goal[1]:
                col = col + 1 if col < goal[1] else col - 1
            else:
                break
            path.append(game_map[row][col])
        return path


class Aki(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = []
        depth_level = 0
        lista_cvorova = [[game_map[self.row][self.col], 0]]
        # Strategija pretrage po dubini, prednost daje onim poljima sa manjom cenom, a u slucaju istih cena onda bira
        # po stranama sveta (Sever, Istok, Jug, Zapad)
        row = self.row
        col = self.col

        neighbors = []
        visited = []
        while len(lista_cvorova) > 0:
            visited.append(game_map[row][col])
            sledeci_cvor = lista_cvorova[0][0]
            depth_level = lista_cvorova[0][1]
            lista_cvorova.pop(0)
            row = sledeci_cvor.row
            col = sledeci_cvor.col
            while depth_level < len(path):
                path.pop()
            if row == goal[0] and col == goal[1]:
                path.append(game_map[row][col])
                break
            else:
                neighbors.clear()
                # sever
                if 0 <= row - 1 < len(game_map) and 0 <= col < len(game_map[0]):
                    if game_map[row - 1][col] not in path:
                        neighbors.append([game_map[row - 1][col], depth_level + 1, "sever"])

                # istok
                if 0 <= row < len(game_map) and 0 <= col + 1 < len(game_map[0]):
                    if game_map[row][col + 1] not in path:
                        neighbors.append([game_map[row][col + 1], depth_level + 1, "istok"])
                # jug
                if 0 <= row + 1 < len(game_map) and 0 <= col < len(game_map[0]):
                    if game_map[row + 1][col] not in path:
                        neighbors.append([game_map[row + 1][col], depth_level + 1, "jug"])
                # zapad
                if 0 <= row < len(game_map) and 0 <= col - 1 < len(game_map[0]):
                    if game_map[row][col - 1] not in path:
                        neighbors.append([game_map[row][col - 1], depth_level + 1, "zapad"])

                neighbors.sort(key=lambda x: x[0].cost(), reverse=False)
                # dodavanje na pocetak liste
                neighbors.reverse()
                for n in neighbors:
                    lista_cvorova.insert(0, [game_map[n[0].row][n[0].col], n[1]])
                if len(neighbors) > 0:
                    path.append(game_map[row][col])
        return path


class Jocke(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        # path = [game_map[self.row][self.col]
        # Strategija pretrage po sirini, prednost daje poljima cini su susedi kolektivno prohodniji,( sa nizom prosjecnom cijenom)
        path = []
        depth_level = 1
        row = self.row
        col = self.col
        # print("X:", row)
        # print("Y: ", col)
        neighbors = []
        lista_cvorova = [[game_map[self.row][self.col], [], depth_level]]
        while len(lista_cvorova) > 0:
            sledeci_cvor = lista_cvorova[0][0]
            path = lista_cvorova[0][1]
            lista_cvorova.pop(0)
            row = sledeci_cvor.row
            col = sledeci_cvor.col
            # print("Koordinate: (", row, col, ")")
            if row == goal[0] and col == goal[1]:
                path.append(game_map[row][col])
                return path
            else:
                neighbors.clear()
                # sever
                if 0 <= row - 1 < len(game_map) and 0 <= col < len(game_map[0]):
                    if game_map[row - 1][col] not in path:
                        x_coord = row - 1
                        y_coord = col
                        neighbor_cnt = 0
                        sum = 0
                        avg_val = 0
                        # racunanje avg_vrijednosti komsija
                        # sever
                        if 0 <= x_coord - 1 < len(game_map) and 0 <= y_coord < len(game_map[0]):
                            if not (x_coord - 1 == row and y_coord == col):  # provjera da nije izvorno polje
                                sum += game_map[x_coord - 1][y_coord].cost()
                                neighbor_cnt += 1
                        # istok
                        if 0 <= x_coord < len(game_map) and 0 <= y_coord + 1 < len(game_map[0]):
                            if not (x_coord == row and y_coord + 1 == col):  # provjera da nije izvorno polje
                                sum += game_map[x_coord][y_coord + 1].cost()
                                neighbor_cnt += 1
                        # jug
                        if 0 <= x_coord + 1 < len(game_map) and 0 <= y_coord < len(game_map[0]):
                            if not (x_coord + 1 == row and y_coord == col):  # provjera da nije izvorno polje
                                sum += game_map[x_coord + 1][y_coord].cost()
                                neighbor_cnt += 1
                        # zapad
                        if 0 <= x_coord < len(game_map) and 0 <= y_coord - 1 < len(game_map[0]):
                            if not (x_coord == row and y_coord - 1 == col):  # provjera da nije izvorno polje
                                sum += game_map[x_coord][y_coord - 1].cost()
                                neighbor_cnt += 1

                        # avg_vrijednost
                        if (neighbor_cnt != 0):
                            avg_val = sum / neighbor_cnt
                        current_path = path.copy()
                        current_path.append(game_map[row][col])
                        neighbors.append([game_map[row - 1][col], current_path, depth_level + 1, "sever", avg_val])

                # istok
                if 0 <= row < len(game_map) and 0 <= col + 1 < len(game_map[0]):
                    if game_map[row][col + 1] not in path:
                        x_coord = row
                        y_coord = col + 1
                        neighbor_cnt = 0
                        avg_val = 0
                        sum = 0
                        # racunanje avg_vrijednosti komsija
                        # sever
                        if 0 <= x_coord - 1 < len(game_map) and 0 <= y_coord < len(game_map[0]):
                            if not (x_coord - 1 == row and y_coord == col):  # provjera da nije izvorno polje
                                sum += game_map[x_coord - 1][y_coord].cost()
                                neighbor_cnt += 1
                        # istok
                        if 0 <= x_coord < len(game_map) and 0 <= y_coord + 1 < len(game_map[0]):
                            if not (x_coord == row and y_coord + 1 == col):  # provjera da nije izvorno polje
                                sum += game_map[x_coord][y_coord + 1].cost()
                                neighbor_cnt += 1
                        # jug
                        if 0 <= x_coord + 1 < len(game_map) and 0 <= y_coord < len(game_map[0]):
                            if not (x_coord + 1 == row and y_coord == col):  # provjera da nije izvorno polje
                                sum += game_map[x_coord + 1][y_coord].cost()
                                neighbor_cnt += 1
                        # zapad
                        if 0 <= x_coord < len(game_map) and 0 <= y_coord - 1 < len(game_map[0]):
                            if not (x_coord == row and y_coord - 1 == col):  # provjera da nije izvorno polje
                                sum += game_map[x_coord][y_coord - 1].cost()
                                neighbor_cnt += 1

                        # avg_vrijednost
                        if (neighbor_cnt != 0):
                            avg_val = sum / neighbor_cnt

                        current_path = path.copy()
                        current_path.append(game_map[row][col])
                        neighbors.append([game_map[row][col + 1], current_path, depth_level + 1, "istok", avg_val])
                # jug
                if 0 <= row + 1 < len(game_map) and 0 <= col < len(game_map[0]):
                    if game_map[row + 1][col] not in path:
                        x_coord = row + 1
                        y_coord = col
                        neighbor_cnt = 0
                        avg_val = 0
                        sum = 0
                        # racunanje avg_vrijednosti komsija
                        # sever
                        if 0 <= x_coord - 1 < len(game_map) and 0 <= y_coord < len(game_map[0]):
                            if not (x_coord - 1 == row and y_coord == col):  # provjera da nije izvorno polje
                                sum += game_map[x_coord - 1][y_coord].cost()
                                neighbor_cnt += 1
                        # istok
                        if 0 <= x_coord < len(game_map) and 0 <= y_coord + 1 < len(game_map[0]):
                            if not (x_coord == row and y_coord + 1 == col):  # provjera da nije izvorno polje
                                sum += game_map[x_coord][y_coord + 1].cost()
                                neighbor_cnt += 1
                        # jug
                        if 0 <= x_coord + 1 < len(game_map) and 0 <= y_coord < len(game_map[0]):
                            if not (x_coord + 1 == row and y_coord == col):  # provjera da nije izvorno polje
                                sum += game_map[x_coord + 1][y_coord].cost()
                                neighbor_cnt += 1
                        # zapad
                        if 0 <= x_coord < len(game_map) and 0 <= y_coord - 1 < len(game_map[0]):
                            if not (x_coord == row and y_coord - 1 == col):  # provjera da nije izvorno polje
                                sum += game_map[x_coord][y_coord - 1].cost()
                                neighbor_cnt += 1

                        # avg_vrijednost
                        if (neighbor_cnt != 0):
                            avg_val = sum / neighbor_cnt
                        current_path = path.copy()
                        current_path.append(game_map[row][col])
                        neighbors.append([game_map[row + 1][col], current_path, depth_level + 1, "jug", avg_val])
                # zapad
                if 0 <= row < len(game_map) and 0 <= col - 1 < len(game_map[0]):
                    if game_map[row][col - 1] not in path:
                        x_coord = row
                        y_coord = col - 1
                        neighbor_cnt = 0
                        avg_val = 0
                        sum = 0
                        # racunanje avg_vrijednosti komsija
                        # sever
                        if 0 <= x_coord - 1 < len(game_map) and 0 <= y_coord < len(game_map[0]):
                            if not (x_coord - 1 == row and y_coord == col):  # provjera da nije izvorno polje
                                sum += game_map[x_coord - 1][y_coord].cost()
                                neighbor_cnt += 1
                        # istok
                        if 0 <= x_coord < len(game_map) and 0 <= y_coord + 1 < len(game_map[0]):
                            if not (x_coord == row and y_coord + 1 == col):  # provjera da nije izvorno polje
                                sum += game_map[x_coord][y_coord + 1].cost()
                                neighbor_cnt += 1
                        # jug
                        if 0 <= x_coord + 1 < len(game_map) and 0 <= y_coord < len(game_map[0]):
                            if not (x_coord + 1 == row and y_coord == col):  # provjera da nije izvorno polje
                                sum += game_map[x_coord + 1][y_coord].cost()
                                neighbor_cnt += 1
                        # zapad
                        if 0 <= x_coord < len(game_map) and 0 <= y_coord - 1 < len(game_map[0]):
                            if not (x_coord == row and y_coord - 1 == col):  # provjera da nije izvorno polje
                                sum += game_map[x_coord][y_coord - 1].cost()
                                neighbor_cnt += 1

                        # avg_vrijednost
                        if (neighbor_cnt != 0):
                            avg_val = sum / neighbor_cnt
                        current_path = path.copy()
                        current_path.append(game_map[row][col])
                        neighbors.append([game_map[row][col - 1], current_path, depth_level + 1, "zapad", avg_val])

                # print("Nesortirani:")
                # for n in neighbors:
                #     print(n[0].row, n[0].col, n[2], n[3],n[4])
                neighbors.sort(key=lambda x: x[4], reverse=False)
                # print("Sortirani:")
                # for n in neighbors:
                #     print(n[0].row, n[0].col, n[2], n[3],n[4])
                # dodavanje na pocetak liste
                # neighbors.reverse()
                # print("Pred ubacivanje:")
                # for n in neighbors:
                #     print(n[0].row, n[0].col, n[2], n[3],n[4])
                for n in neighbors:
                    lista_cvorova.append([game_map[n[0].row][n[0].col], n[1], n[2]])
                # if len(neighbors) > 0:
                #     path.append(game_map[row][col])

        return path


class Draza(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]
        pocetna_cijena=game_map[self.row][self.col].cost()
        # Strategija pretrage grananje i ogranicavanje, bira onu sa manjom cijenom a ako su iste cijene bira sa manje cvorova
        lista_parcijalnih_putanja = [[path, pocetna_cijena]]  # startni cvor
        while len(lista_parcijalnih_putanja) > 0:  # sve dok je lista parcijalnih putanja neprazna
            trenutna_putanja = lista_parcijalnih_putanja[0][0]
            trenutna_cijena = lista_parcijalnih_putanja[0][1]
            neighbors = []
            lista_parcijalnih_putanja.pop(0)
            poslednji_cvor = trenutna_putanja[len(trenutna_putanja) - 1]
            row = poslednji_cvor.row
            col = poslednji_cvor.col
           # print("ROW:", row, " COL:", col, " PRICE:", trenutna_cijena)
            if row == goal[0] and col == goal[1]:
                return trenutna_putanja
            else:
                #za svakog sljedbenika poslednjeg cvora na uklonjenoj putanji formira se po jedna nova putanja
                # sever
                if 0 <= row - 1 < len(game_map) and 0 <= col < len(game_map[0]):
                    if game_map[row - 1][col] not in trenutna_putanja:
                        nova_cijena=trenutna_cijena+game_map[row-1][col].cost()
                        nova_putanja=trenutna_putanja.copy()
                        nova_putanja.append(game_map[row-1][col])
                        lista_parcijalnih_putanja.append([nova_putanja,nova_cijena])

                # istok
                if 0 <= row < len(game_map) and 0 <= col + 1 < len(game_map[0]):
                    if game_map[row][col + 1] not in trenutna_putanja:
                        nova_cijena = trenutna_cijena + game_map[row][col+1].cost()
                        nova_putanja = trenutna_putanja.copy()
                        nova_putanja.append(game_map[row][col+1])
                        lista_parcijalnih_putanja.append([nova_putanja, nova_cijena])

                # jug
                if 0 <= row + 1 < len(game_map) and 0 <= col < len(game_map[0]):
                    if game_map[row + 1][col] not in trenutna_putanja:
                        nova_cijena = trenutna_cijena + game_map[row + 1][col].cost()
                        nova_putanja = trenutna_putanja.copy()
                        nova_putanja.append(game_map[row + 1][col])
                        lista_parcijalnih_putanja.append([nova_putanja, nova_cijena])

                # zapad
                if 0 <= row < len(game_map) and 0 <= col - 1 < len(game_map[0]):
                    if game_map[row][col - 1] not in trenutna_putanja:
                        nova_cijena = trenutna_cijena + game_map[row][col-1].cost()
                        nova_putanja = trenutna_putanja.copy()
                        nova_putanja.append(game_map[row][col-1])
                        lista_parcijalnih_putanja.append([nova_putanja, nova_cijena])

                #sortiranje liste parcijalnih putanja po cijeni putanje
                lista_parcijalnih_putanja.sort(key=lambda x:len(x[0]), reverse=False) #daje prioritet linijama sa manje cvorova (reverse=True daje prioritet duzim linijama)
                lista_parcijalnih_putanja.sort(key=lambda x: x[1], reverse=False)

        return path


class Bole(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]
        pocetna_cijena = game_map[self.row][self.col].cost()
        pocetna_heuristika=0
        # Strategija A*
        goal_row=goal[0]
        goal_col=goal[1]
        koeficijent=1
        lista_parcijalnih_putanja = [[path, pocetna_cijena, pocetna_heuristika]]  # startni cvor
        while len(lista_parcijalnih_putanja) > 0:  # sve dok je lista parcijalnih putanja neprazna
            trenutna_putanja = lista_parcijalnih_putanja[0][0]
            trenutna_cijena = lista_parcijalnih_putanja[0][1]
            neighbors = []
            lista_parcijalnih_putanja.pop(0)
            poslednji_cvor = trenutna_putanja[len(trenutna_putanja) - 1]
            row = poslednji_cvor.row
            col = poslednji_cvor.col
            #print("ROW:", row, " COL:", col, " PRICE:", trenutna_cijena)
            if row == goal[0] and col == goal[1]:
                return trenutna_putanja
            else:
                # za svakog sljedbenika poslednjeg cvora na uklonjenoj putanji formira se po jedna nova putanja
                # sever
                if 0 <= row - 1 < len(game_map) and 0 <= col < len(game_map[0]):
                    if game_map[row - 1][col] not in trenutna_putanja:
                        nova_cijena = trenutna_cijena + game_map[row - 1][col].cost()
                        nova_putanja = trenutna_putanja.copy()
                        nova_putanja.append(game_map[row - 1][col])
                        #racunanje heuristike
                        heuristika=(((goal_row-(row-1))**2 + (goal_col-col)**2)**0.5)*koeficijent
                        #print("Heuristika:", heuristika)
                        lista_parcijalnih_putanja.append([nova_putanja, nova_cijena, heuristika])

                # istok
                if 0 <= row < len(game_map) and 0 <= col + 1 < len(game_map[0]):
                    if game_map[row][col + 1] not in trenutna_putanja:
                        nova_cijena = trenutna_cijena + game_map[row][col + 1].cost()
                        nova_putanja = trenutna_putanja.copy()
                        nova_putanja.append(game_map[row][col + 1])
                        #racunanje heuristike
                        heuristika=(((goal_row-row)**2 + (goal_col-(col+1))**2)**0.5)*koeficijent
                       # print("Heuristika:", heuristika)
                        lista_parcijalnih_putanja.append([nova_putanja, nova_cijena, heuristika])

                # jug
                if 0 <= row + 1 < len(game_map) and 0 <= col < len(game_map[0]):
                    if game_map[row + 1][col] not in trenutna_putanja:
                        nova_cijena = trenutna_cijena + game_map[row + 1][col].cost()
                        nova_putanja = trenutna_putanja.copy()
                        nova_putanja.append(game_map[row + 1][col])

                        #racunanje heuristike
                        heuristika=(((goal_row-(row+1))**2 + (goal_col-col)**2)**0.5)*koeficijent
                       # print("Heuristika:", heuristika)
                        lista_parcijalnih_putanja.append([nova_putanja, nova_cijena, heuristika])

                # zapad
                if 0 <= row < len(game_map) and 0 <= col - 1 < len(game_map[0]):
                    if game_map[row][col - 1] not in trenutna_putanja:
                        nova_cijena = trenutna_cijena + game_map[row][col - 1].cost()
                        nova_putanja = trenutna_putanja.copy()
                        nova_putanja.append(game_map[row][col - 1])


                        #racunanje heuristike
                        heuristika=(((goal_row-row)**2 + (goal_col-(col-1))**2)**0.5)*koeficijent
                        #print("Heuristika:", heuristika)
                        lista_parcijalnih_putanja.append([nova_putanja, nova_cijena, heuristika])

                # sortiranje liste parcijalnih putanja po cijeni putanje
                lista_parcijalnih_putanja.sort(key=lambda x: len(x[0]),
                                               reverse=False)  # daje prioritet linijama sa manje cvorova (reverse=True daje prioritet duzim linijama)
                lista_parcijalnih_putanja.sort(key=lambda x: (x[1]+x[2]), reverse=False)

        return path


class Tile(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Tile, self).__init__(row, col, file_name)

    def position(self):
        return self.row, self.col

    def cost(self):
        pass

    def kind(self):
        pass


class Stone(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'stone.png')

    def cost(self):
        return 1000

    def kind(self):
        return 's'


class Water(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'water.png')

    def cost(self):
        return 500

    def kind(self):
        return 'w'


class Road(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'road.png')

    def cost(self):
        return 2

    def kind(self):
        return 'r'


class Grass(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'grass.png')

    def cost(self):
        return 3

    def kind(self):
        return 'g'


class Mud(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'mud.png')

    def cost(self):
        return 5

    def kind(self):
        return 'm'


class Dune(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'dune.png')

    def cost(self):
        return 7

    def kind(self):
        return 's'


class Goal(BaseSprite):
    def __init__(self, row, col):
        super().__init__(row, col, 'x.png', config.DARK_GREEN)


class Trail(BaseSprite):
    def __init__(self, row, col, num):
        super().__init__(row, col, 'trail.png', config.DARK_GREEN)
        self.num = num

    def draw(self, screen):
        text = config.GAME_FONT.render(f'{self.num}', True, config.WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
