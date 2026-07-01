import pygame

TOTAL_COLETAVEIS = 6
TAMANHO_ICONE = 28
ESPESSURA_CONTORNO = 2
ESPACAMENTO = 8
MARGEM = 15

COR_CONTORNO = (255, 255, 255, 255)

ORDEM_TIPOS = [
    "chave_azul",
    "chave_verde",
    "chave_vermelha",
    "logo_claude",
    "logo_gpt",
    "logo_gemini",
]

CAMINHOS_IMAGEM = {
    "chave_azul": "imagens/chave_azul.png",
    "chave_verde": "imagens/chave_verde.png",
    "chave_vermelha": "imagens/chave_vermelha.png",
    "logo_claude": "imagens/logoclaude.png",
    "logo_gpt": "imagens/logogpt.png",
    "logo_gemini": "imagens/logogemini.png",
}

_imagens_coloridas = {}
_imagens_silhueta = {}


def aplicar_contorno(imagem, cor=COR_CONTORNO, espessura=ESPESSURA_CONTORNO):
    mascara = pygame.mask.from_surface(imagem)
    forma_solida = mascara.to_surface(setcolor=cor, unsetcolor=(0, 0, 0, 0))

    largura, altura = imagem.get_size()
    resultado = pygame.Surface(
        (largura + espessura * 2, altura + espessura * 2), pygame.SRCALPHA
    )

    for dx in range(-espessura, espessura + 1):
        for dy in range(-espessura, espessura + 1):
            if dx == 0 and dy == 0:
                continue
            resultado.blit(forma_solida, (espessura + dx, espessura + dy))

    resultado.blit(imagem, (espessura, espessura))
    return resultado


def carregar_icones():
    if _imagens_coloridas:
        return

    for tipo, caminho in CAMINHOS_IMAGEM.items():
        imagem = pygame.image.load(caminho).convert_alpha()
        imagem = pygame.transform.scale(imagem, (TAMANHO_ICONE, TAMANHO_ICONE))

        _imagens_coloridas[tipo] = aplicar_contorno(imagem)

        mascara = pygame.mask.from_surface(imagem)
        silhueta = mascara.to_surface(
            setcolor=(0, 0, 0, 255), unsetcolor=(0, 0, 0, 0)
        )
        _imagens_silhueta[tipo] = aplicar_contorno(silhueta)


class Inventario:
    def __init__(self):
        self.itens_coletados = []

    def adicionar_item(self, tipo):
        self.itens_coletados.append(tipo)

    def quantidade_total(self):
        return len(self.itens_coletados)

    def completo(self):
        return self.quantidade_total() >= TOTAL_COLETAVEIS


def desenhar_hud(tela, inventario):
    carregar_icones()

    restantes = list(ORDEM_TIPOS)
    for tipo_coletado in inventario.itens_coletados:
        restantes.remove(tipo_coletado)

    slots = inventario.itens_coletados + restantes
    coletados_count = inventario.quantidade_total()

    tamanho_com_borda = TAMANHO_ICONE + ESPESSURA_CONTORNO * 2
    largura_tela = tela.get_width()
    largura_total = (
        TOTAL_COLETAVEIS * tamanho_com_borda
        + (TOTAL_COLETAVEIS - 1) * ESPACAMENTO
    )
    x_inicial = largura_tela - MARGEM - largura_total

    for i, tipo in enumerate(slots):
        x = x_inicial + i * (tamanho_com_borda + ESPACAMENTO)
        y = MARGEM

        if i < coletados_count:
            tela.blit(_imagens_coloridas[tipo], (x, y))
        else:
            tela.blit(_imagens_silhueta[tipo], (x, y))