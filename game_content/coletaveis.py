import pygame
import random
from game_content import mapa as mapa_modulo

PROXIMIDADE = 50
DIST_MINIMA_ENTRE_ITENS = 80
TAMANHO_SPRITE = 20  

_fonte_mensagem = None

CAMINHOS_IMAGEM = {
    "chave_azul": "imagens/chave_azul.png",
    "chave_verde": "imagens/chave_verde.png",
    "chave_vermelha": "imagens/chave_vermelha.png",
    "logo_claude": "imagens/logoclaude.png",
    "logo_gpt": "imagens/logogpt.png",
    "logo_gemini": "imagens/logogemini.png",
}

_imagens_carregadas = {}


def carregar_imagem(tipo):
    if tipo not in _imagens_carregadas:
        caminho = CAMINHOS_IMAGEM[tipo]
        imagem = pygame.image.load(caminho).convert_alpha()
        imagem = pygame.transform.scale(imagem, (TAMANHO_SPRITE, TAMANHO_SPRITE))
        _imagens_carregadas[tipo] = imagem
    return _imagens_carregadas[tipo]


class Coletaveis(pygame.sprite.Sprite):
    def __init__(self, x, y, andar, tipo):
        super().__init__()
        self.image = carregar_imagem(tipo)
        self.rect = self.image.get_rect(center=(x, y))
        self.andar = andar
        self.tipo = tipo
        self.coletado = False


def obter_posicao_andavel_aleatoria(andar):
    grade = mapa_modulo.mapas[andar]

    while True:
        linha_indice = random.randrange(len(grade))
        coluna_indice = random.randrange(len(grade[linha_indice]))
        bloco = grade[linha_indice][coluna_indice]

        if bloco != "#":
            x = coluna_indice * mapa_modulo.TAMANHO_TILE + mapa_modulo.TAMANHO_TILE // 2
            y = linha_indice * mapa_modulo.TAMANHO_TILE + mapa_modulo.TAMANHO_TILE // 2
            return x, y


def posicao_valida(x, y, andar, existentes, dist_minima=DIST_MINIMA_ENTRE_ITENS):
    for c in existentes:
        if c.andar == andar:
            d = pygame.math.Vector2(x, y).distance_to(c.rect.center)
            if d < dist_minima:
                return False
    return True


def sortear_posicoes_coletaveis(andares=(0, 1, 2)):
    tipos = [
        "chave_azul",
        "chave_verde",
        "chave_vermelha",
        "logo_claude",
        "logo_gpt",
        "logo_gemini",
    ]
    random.shuffle(tipos)

    coletaveis = []
    tentativas_max = 200

    for tipo in tipos:
        for _ in range(tentativas_max):
            andar = random.choice(andares)
            x, y = obter_posicao_andavel_aleatoria(andar)
            if posicao_valida(x, y, andar, coletaveis):
                coletaveis.append(Coletaveis(x, y, andar, tipo))
                break

    return coletaveis


def obter_rect_jogador(player):
    return pygame.Rect(player.x, player.y, player.largura, player.altura)


def checar_proximidade(player, coletaveis, andar_atual):
    rect_jogador = obter_rect_jogador(player)
    item_proximo = None

    for item in coletaveis:
        if item.andar != andar_atual or item.coletado:
            continue
        dist = pygame.math.Vector2(rect_jogador.center).distance_to(item.rect.center)
        if dist <= PROXIMIDADE:
            item_proximo = item
            break

    return item_proximo


def desenhar_mensagem(tela, texto, rect_referencia):
    global _fonte_mensagem
    if _fonte_mensagem is None:
        _fonte_mensagem = pygame.font.SysFont(None, 28)

    superficie = _fonte_mensagem.render(texto, True, (255, 255, 255))
    fundo = superficie.get_rect()
    fundo.midbottom = (rect_referencia.centerx, rect_referencia.top - 10)
    pygame.draw.rect(tela, (0, 0, 0), fundo.inflate(10, 6))
    tela.blit(superficie, fundo)


def atualizar_coletaveis(tela, player, coletaveis, andar_atual, eventos, inventario):
    rect_jogador = obter_rect_jogador(player)
    item_proximo = checar_proximidade(player, coletaveis, andar_atual)

    if item_proximo:
        desenhar_mensagem(tela, "Aperte F para coletar este item", rect_jogador)

    for evento in eventos:
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_f:
            if item_proximo:
                item_proximo.coletado = True
                coletaveis.remove(item_proximo)
                inventario.adicionar_item(item_proximo.tipo)

    return item_proximo