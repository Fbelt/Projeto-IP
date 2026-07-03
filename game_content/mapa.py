import pygame
import os

TAMANHO_TILE = 25

COR_CHAO = (255,255,255)
COR_PAREDE = (145, 0, 25)
COR_PORTA = (35, 175, 75)
COR_ESCADA = (130, 130, 130)
COR_TEXTO_ESCADA = (0, 170, 60)
PORTAS_TRANCADAS = {
    "A": "chave_azul",
    "V": "chave_verde",
    "R": "chave_vermelha",}
CORES_PORTA_TRANCADA = {
    "A": (40, 130, 255),
    "V": (50, 200, 90),
    "R": (220, 45, 45),
}
TEXTURAS = None  # cache global, carregado só na primeira chamada de desenhar_mapa


def carregar_textura(nome_arquivo):
    caminho = f"imagens/{nome_arquivo}"
    imagem = pygame.image.load(caminho).convert_alpha()
    return pygame.transform.scale(imagem, (TAMANHO_TILE, TAMANHO_TILE))


def carregar_texturas():
    global TEXTURAS
    if TEXTURAS is None:
        porta_base = carregar_textura("porta.png")

        TEXTURAS = {
            "#": carregar_textura("parede.png"),
            ".": carregar_textura("chao.png"),
            "D": porta_base,
            "S": carregar_textura("escada_subida.png"),
            "B": carregar_textura("escada_descida.png"),
        }

        for bloco, cor in CORES_PORTA_TRANCADA.items():
            porta_colorida = porta_base.copy()
            porta_colorida.fill((*cor, 255), special_flags=pygame.BLEND_RGBA_MULT)
            TEXTURAS[bloco] = porta_colorida

MAPA_ANDAR_1 = [
    "P.............................#..#SSS....#..#...",
    "...........##DD###########....#..#SSS.p..D..#...",
    "...........#.............#....#..#SSS....D..#...",
    "...........#......G......#....#..#.......#..#...",
    "#########..#.............#....#..#.......#..#...",
    "........#..#.............#....#..#########..#...",
    "....G...#..###########DD##....#..#..........#...",
    "........#......#....D...#.....#..#..G.......#...",
    "........#......#....D...#.....#..#..........#...",
    "#DD######......#....#...#.....#..#....####..#...",
    "...............#....#####.....#..#....####..#...",
    "....E..........#....#.........#..#....####..#...",
    "#####.######...##DD##.........#..#....####..#...",
    "....#.D....#..........#########..#..........#...",
    "##..#.D....#......E...#..........#..#########.##",
    "##..#.#..###..........#..........#..#.........#.",
    "....#.#..###..####DD#.#..######..#..#.######..#.",
    "....#.#....#..#.....#.#..#....#..#..#.######..#.",
    "..###.###DD#..#.##..#.#..#....D..#..#.######..#.",
    ".......#...#..#.##..#.#..#....D..#..#.........D.",
    ".......#...#..#.##..#.#DD#########..#.........D.",
    ".......#...#..#.##..#.............E.###########.",
    ".......#...#..#.##..#...........................",
    ".#######.G.#..#.....############################",
    ".#.........#..#.....#..............A....#..D..D.",
    ".#.........#..#.....#...#########..A....#..####.",
    ".#DD####...#..#######.E.#########..#....####.D..",
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
    "......#..##.....E.............#..#######..######",
    "..##..#..##...................#..#######..######",
    "..G#..#..##..###############..#..#..............",
    "...#..#..##..##.......#.......#..#..............",
    "...#..#..##..##.......#.......#..#..............",
    "..#####..##..##..######..######..#..............",
    "......#..##...#..........#.......#..............",
    "......#..##...#........E.#.......#..............",
    "####..#..##############..#..###..#..............",
    "#..#............#.....#..#....#..#..............",
    "#..#............#.....#..#....#..#..............",
    "#..####..#####..#..#..#..######..#..............",
    "#.....#..#..##..#..#..#......#...#..............",
    "####..#..#..##..#..#..#..#####...#..............",
    "...#..#..#..##..#..#..#..#..######..............",
    "...#.....E.........#..#..#..#....#..............",
    "...#...............#..#..#..#....#######..######",
    "...#########..######..#.....#....#######..######",
    "...........#..#.......#.....#....#######..######",
    "...........#..#.......#..####....V..............",
    "..##########..#..######..#.......V..............",
    "..............#..#.......#.......V..............",
    "..............#..#.......#.......V..............",
    "..#############..#########.......###############",
    "..#........................E.....###############",
]


MAPA_ANDAR_3 = [
    ".............#....#...#..........#...#......#BBB",
    "..#########..#....D...D....G.....D...#......#BBB",
    "..#.......#..#....D...D..........D...#......#BBB",
    "..R.......#..#....#...#..........#...#####..#...",
    "..R.......#..#....#..######RR######......#..#.P.",
    "..#########..#....#..#............#......#..#...",
    ".E...........######..#............#......#..#...",
    ".....................#............#......D..#...",
    "##########...........#............#....E.D..#...",
    ".........#..######...##################..####...",
    "...G.....#..#.............#...........#.........",
    ".........#..#.............#...........#.........",
    "...##DD###..#.............#...........#....#####",
    "...#........#.............#####DD######....#....",
    "...#........#.............#................#....",
    "...#.......................................#....",
    "...#.............................########..#....",
    "####....E........................#......#..#....",
    "............#.............#......#......#..#....",
    "............#.............#####..#......#..#....",
    "#DD##.......#.............#...#..#......#..###DD",
    "....#.......#.............#...#..#......#.......",
    "....#.......#.............#...#..#......#.......",
    "....#..###DD######...######...#..##DD#########DD",
    "....#..#.........#...#........#......#..........",
    "....#..#.........#...#........#......#..........",
    "....#..#...G.....#...#........#......#..........",
    "....#..#.........#...##RR######.E....#..........",
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

            elif bloco == "." or bloco == "P" or bloco == "p" or bloco == "E" or bloco == "G":
                tela.blit(TEXTURAS["."], retangulo)

            elif bloco == "D" or bloco == "A" or bloco == "V" or bloco == "R":
                tela.blit(TEXTURAS[bloco], retangulo)

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


def eh_bloqueado(mapa, x, y, inventario=None):
    bloco = pegar_bloco(mapa, x, y)

    if bloco == "#":
        return True

    if bloco in PORTAS_TRANCADAS:
        chave_necessaria = PORTAS_TRANCADAS[bloco]

        if inventario is not None and inventario.tem_item(chave_necessaria):
            return False

        return True

    return False


def jogador_colide_com_mapa(mapa, jogador, inventario=None):
    pontos = [
        (jogador.x, jogador.y),
        (jogador.x + jogador.largura - 1, jogador.y),
        (jogador.x, jogador.y + jogador.altura - 1),
        (jogador.x + jogador.largura - 1, jogador.y + jogador.altura - 1),
    ]

    for x, y in pontos:
        if eh_bloqueado(mapa, x, y, inventario):
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

def trocar_bloco_do_mapa(mapa, linha, coluna, novo_bloco):
    novo_mapa = [list(linha_texto) for linha_texto in mapa]
    novo_mapa[linha][coluna] = novo_bloco
    return ["".join(linha_texto) for linha_texto in novo_mapa]


def encontrar_porta_trancada_perto(mapa, jogador):
    centro_x = jogador.x + jogador.largura // 2
    centro_y = jogador.y + jogador.altura // 2

    coluna = int(centro_x // TAMANHO_TILE)
    linha = int(centro_y // TAMANHO_TILE)

    posicoes_para_testar = [
        (linha, coluna),
        (linha - 1, coluna),
        (linha + 1, coluna),
        (linha, coluna - 1),
        (linha, coluna + 1),
    ]

    for linha_teste, coluna_teste in posicoes_para_testar:
        if linha_teste < 0 or linha_teste >= len(mapa):
            continue

        if coluna_teste < 0 or coluna_teste >= len(mapa[0]):
            continue

        bloco = mapa[linha_teste][coluna_teste]

        if bloco in PORTAS_TRANCADAS:
            return linha_teste, coluna_teste, bloco

    return None


def tentar_abrir_porta(mapa, jogador, inventario):
    porta = encontrar_porta_trancada_perto(mapa, jogador)

    if porta is None:
        return mapa

    linha, coluna, tipo_porta = porta
    chave_necessaria = PORTAS_TRANCADAS[tipo_porta]

    if inventario.tem_item(chave_necessaria):
        return trocar_bloco_do_mapa(mapa, linha, coluna, "D")

    return mapa

def encontrar_posicoes_patrulhas(mapa):
    posicoes = []
    for linha_indice, linha in enumerate(mapa):
        for coluna_indice, bloco in enumerate(linha):
            if bloco == "E":
                x = coluna_indice * TAMANHO_TILE
                y = linha_indice * TAMANHO_TILE
                posicoes.append((x, y))
    return posicoes

def encontrar_posicoes_vigias(mapa):
    posicoes = []

    for linha_indice, linha in enumerate(mapa):
        for coluna_indice, bloco in enumerate(linha):
            if bloco == "G":
                x = coluna_indice * TAMANHO_TILE
                y = linha_indice * TAMANHO_TILE
                posicoes.append((x, y))

    return posicoes