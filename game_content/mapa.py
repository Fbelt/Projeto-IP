import pygame
import os

TAMANHO_TILE = 25

COR_CHAO = (255,255,255)
COR_PAREDE = (145, 0, 25)
COR_PORTA = (35, 175, 75)
COR_ESCADA = (130, 130, 130)
COR_TEXTO_ESCADA = (0, 170, 60)

TEXTURAS = None  # cache global, carregado só na primeira chamada de desenhar_mapa
 
 
def carregar_textura(nome_arquivo):
    caminho = f"imagens/{nome_arquivo}"
    imagem = pygame.image.load(caminho).convert_alpha()
    return pygame.transform.scale(imagem, (TAMANHO_TILE, TAMANHO_TILE))
 
 
def carregar_texturas():
    global TEXTURAS
    if TEXTURAS is None:
        TEXTURAS = {
            "#": carregar_textura("parede.png"),
            ".": carregar_textura("chao.png"),
            "D": carregar_textura("porta.png"),
            "S": carregar_textura("escada_subida.png"),
            "B": carregar_textura("escada_descida.png"),
        }

MAPA_ANDAR_1 = [
    "P.............................#..#SSS....#..#...",
    "...........##DD###########....#..#SSS.p..D..#...",
    "...........#.............#....#..#SSS....D..#...",
    "...........#.............#....#..#.......#..#...",
    "#########..#.............#....#..#.......#..#...",
    "........#..#.............#....#..#########..#...",
    "........#..###########DD##....#..#..........#...",
    "........#......#....D...#.....#..#..........#...",
    "........#......#....D...#.....#..#..........#...",
    "#DD######......#....#...#.....#..#....####..#...",
    "...............#....#####.....#..#....####..#...",
    "...............#....#.........#..#....####..#...",
    "#####.######...##DD##.........#..#....####..#...",
    "....#.D....#.....I....#########..#..........#...",
    "##..#.D....#..........#..........#..#########.##",
    "##..#.#..###..........#..........#..#.........#.",
    "....#.#..###..####DD#.#..######..#..#.######..#.",
    "....#.#....#..#.....#.#..#....#..#..#.######..#.",
    "..###.###DD#..#.##..#.#..#....D..#..#.######..#.",
    ".......#...#..#.##..#.#..#....D..#..#.........D.",
    ".......#...#..#.##..#.#DD#########..#.........D.",
    ".......#...#..#.##..#...............###########.",
    ".......#...#..#.##..#...........................",
    ".#######...#..#.....############################",
    ".#.........#..#.....#..............D....#..D..D.",
    ".#.........#..#.....#...#########..D....#..####.",
    ".#DD####...#..#######...#########..#....####.D..",
    ".......#####............#########..#DD#......D..",
    "........................#########..#..#.#DD###..",
    "........................#########..#..#.#....#..",
]


MAPA_ANDAR_2 = [
    "......#.............#......#......BBB#.......SSS",
    "......#.............#......#....P.BBB#.....p.SSS",
    "####..#..####..######..#####..#...BBB#.......SSS",
    "......#..####..######..#####..#..#######..######",
    "......#..##...................#..#######..######",
    "..##..#..##...................#..#######..######",
    "..##..#..##..###############..#..#..............",
    "..##..#..##..##.......#.......#..#..............",
    "..##..#..##..##.......#.......#..#..............",
    "..#####..##..##..######..######..#..............",
    "......#..##...#..........#.......#..............",
    "......#..##...#..........#.......#..............",
    "####..#..##############..#..###..#..............",
    "#..#............#.....#..#....#..#..............",
    "#..#............#.....#..#....#..#..............",
    "#..####..#####..#..#..#..######..#..............",
    "#.....#..#..##..#..#..#......##..#..............",
    "#.....#..#..##..#..#..#......#...#..............",
    "####..#..#..##..#..#..#..#####...#..............",
    "...#..#..#..##..#..#..#..#..######..............",
    "...#...............#..#..#..#....#..............",
    "...#...............#..#..#..#....#######..######",
    "...#########..######..#.....#....#######..######",
    "...........#..#.......#.....#....#######..######",
    "...........#..#.......#..####...................",
    "..##########..#..######..#......................",
    "..............#..#.......#.........I............",
    "..............#..#.......#......................",
    "..#############..#########.......###############",
    "..#..............................###############",
]


MAPA_ANDAR_3 = [
    ".............#....#...#..........#...#......#BBB",
    "..#########..#....D...D..........D...#......#BBB",
    "..#.......#..#....D...D..........D...#......#BBB",
    "..D.......#..#....#...#..........#...#####..#...",
    "..D.......#..#....#..######DD######......#..#.P.",
    "..#########..#....#..#............#......#..#...",
    ".............######..#............#......#..#...",
    ".....................#............#......D..#...",
    "##########...........#............#......D..#...",
    ".........#..######...##################..####...",
    ".........#..#.............#...........#.........",
    ".........#..#.............#...........#.........",
    "...##DD###..#.............#...........#....#####",
    "...#........#.............#####DD######....#....",
    "...#........#.....I.......#................#....",
    "...#.......................................#....",
    "...#.............................########..#....",
    "####.............................#......#..#....",
    "............#.............#......#......#..#....",
    "............#.............#####..#......#..#....",
    "#DD##.......#.............#...#..#......#..###DD",
    "....#.......#.............#...#..#......#.......",
    "....#.......#.............#...#..#......#.......",
    "....#..###DD######...######...#..##DD#########DD",
    "....#..#.........#...#........#......#..........",
    "....#..#.........#...#........#......#..........",
    "....#..#.........#...#........#......#..........",
    "....#..#.........#...##DD######......#..........",
    "....#..#.........#...................D..........",
    "....#..#.........#...................D..........",
]


mapas = [MAPA_ANDAR_1, MAPA_ANDAR_2, MAPA_ANDAR_3]


def desenhar_mapa(tela, mapa):
    carregar_texturas()
    fonte_escada = pygame.font.SysFont(None, 20)

    for linha_indice, linha in enumerate(mapa):
        for coluna_indice, bloco in enumerate(linha):
            x = coluna_indice * TAMANHO_TILE
            y = linha_indice * TAMANHO_TILE

            retangulo = pygame.Rect(x, y, TAMANHO_TILE, TAMANHO_TILE)

            if bloco == "#":
                tela.blit(TEXTURAS["#"], retangulo)

            elif bloco == "." or bloco == "P" or bloco == "p" or bloco == "I" :
                tela.blit(TEXTURAS["."], retangulo)

            elif bloco == "D":
                tela.blit(TEXTURAS["D"], retangulo)

            elif bloco == "S":
                tela.blit(TEXTURAS["S"], retangulo)
 
            elif bloco == "B":
                tela.blit(TEXTURAS["B"], retangulo)

            pygame.draw.rect(tela, (60, 60, 60), retangulo, 1)


def encontrar_posicao_inicial(mapa):
    for linha_indice, linha in enumerate(mapa):
        for coluna_indice, bloco in enumerate(linha):
            if bloco == "P":
                x = coluna_indice * TAMANHO_TILE
                y = linha_indice * TAMANHO_TILE
                return x, y

    return 0, 0


def pegar_bloco(mapa, x, y):
    coluna = int(x // TAMANHO_TILE)
    linha = int(y // TAMANHO_TILE)

    if linha < 0 or linha >= len(mapa):
        return "#"

    if coluna < 0 or coluna >= len(mapa[0]):
        return "#"

    return mapa[linha][coluna]


def eh_bloqueado(mapa, x, y):
    bloco = pegar_bloco(mapa, x, y)

    return bloco == "#"


def jogador_colide_com_mapa(mapa, jogador):
    pontos = [
        (jogador.x, jogador.y),
        (jogador.x + jogador.largura - 1, jogador.y),
        (jogador.x, jogador.y + jogador.altura - 1),
        (jogador.x + jogador.largura - 1, jogador.y + jogador.altura - 1),
    ]

    for x, y in pontos:
        if eh_bloqueado(mapa, x, y):
            return True

    return False


def jogador_esta_na_escada_subida(mapa, jogador):
    centro_x = jogador.x + jogador.largura // 2
    centro_y = jogador.y + jogador.altura // 2

    return pegar_bloco(mapa, centro_x, centro_y) == "S"

def jogador_esta_na_escada_descida(mapa, jogador):
    centro_x = jogador.x + jogador.largura // 2
    centro_y = jogador.y + jogador.altura // 2

    return pegar_bloco(mapa, centro_x, centro_y) == "B"

def encontrar_posicao_spawn_descida(mapa):
    for linha_indice, linha in enumerate(mapa):
        for coluna_indice, bloco in enumerate(linha):
            if bloco == "p":
                x = coluna_indice * TAMANHO_TILE
                y = linha_indice * TAMANHO_TILE
                return x, y

    return encontrar_posicao_inicial(mapa)

def encontrar_posicao_inimigo(mapa):
    for linha_indice, linha in enumerate(mapa):
        for coluna_indice, bloco in enumerate(linha):
            if bloco == "I":
                x = coluna_indice * TAMANHO_TILE
                y = linha_indice * TAMANHO_TILE
                return x, y

    return 400, 400 