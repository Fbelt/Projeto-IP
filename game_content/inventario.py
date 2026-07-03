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

TECLAS_HABILIDADE = {
    "logo_claude": "1",
    "logo_gpt": "2",
    "logo_gemini": "3",
}

CAMINHO_FONTE_TECLA = "fontes/PressStart2P-Regular.ttf"
TAMANHO_FONTE_TECLA = 12
COR_TECLA = (255, 255, 255)

_imagens_coloridas = {}
_imagens_silhueta = {}
_fonte_tecla = None


def obter_fonte_tecla():
    global _fonte_tecla
    if _fonte_tecla is None:
        _fonte_tecla = pygame.font.Font(CAMINHO_FONTE_TECLA, TAMANHO_FONTE_TECLA)
    return _fonte_tecla


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

    def tem_item(self, tipo):
        return tipo in self.itens_coletados

    def quantidade_total(self):
        return len(self.itens_coletados)

    def completo(self):
        return self.quantidade_total() >= TOTAL_COLETAVEIS


def desenhar_hud(tela, inventario, progresso_recarga_gpt=None):
    carregar_icones()

    tamanho_com_borda = TAMANHO_ICONE + ESPESSURA_CONTORNO * 2
    largura_tela = tela.get_width()
    largura_total = (
        TOTAL_COLETAVEIS * tamanho_com_borda
        + (TOTAL_COLETAVEIS - 1) * ESPACAMENTO
    )
    x_inicial = largura_tela - MARGEM - largura_total

    for i, tipo in enumerate(ORDEM_TIPOS):
        x = x_inicial + i * (tamanho_com_borda + ESPACAMENTO)
        y = MARGEM

        if inventario.tem_item(tipo):
            em_recarga = (
                tipo == "logo_gpt"
                and progresso_recarga_gpt is not None
                and progresso_recarga_gpt < 1
            )

            if em_recarga:
                tela.blit(_imagens_silhueta[tipo], (x, y))

                icone_colorido = _imagens_coloridas[tipo]
                altura_icone = icone_colorido.get_height()
                altura_preenchida = int(altura_icone * progresso_recarga_gpt)

                if altura_preenchida > 0:
                    origem_y = altura_icone - altura_preenchida
                    area_preenchida = pygame.Rect(0, origem_y, icone_colorido.get_width(), altura_preenchida)
                    tela.blit(icone_colorido, (x, y + origem_y), area_preenchida)
            else:
                tela.blit(_imagens_coloridas[tipo], (x, y))
        else:
            tela.blit(_imagens_silhueta[tipo], (x, y))

        if tipo in TECLAS_HABILIDADE:
            fonte_tecla = obter_fonte_tecla()
            texto_tecla = fonte_tecla.render(TECLAS_HABILIDADE[tipo], True, COR_TECLA)
            texto_rect = texto_tecla.get_rect(
                midtop=(x + tamanho_com_borda // 2, y + tamanho_com_borda + 4)
            )
            tela.blit(texto_tecla, texto_rect)