import pygame

from game_content.personagens import jogador as Jogador, InimigoPatrulha, InimigoVigia
from game_content.visao import (
    aplicar_visao,
    criar_animacao_revelacao_portas,
    TEMPO_MAPA_VISIVEL,
    TEMPO_FECHAMENTO_VISAO
)
from game_content.batalha import verificar_colisao
from game_content.mapa import (
    mapas,
    desenhar_mapa,
    encontrar_posicao_inicial,
    encontrar_posicao_spawn_descida,
    jogador_colide_com_mapa,
    jogador_esta_na_escada_subida,
    jogador_esta_na_escada_descida,
    encontrar_posicoes_patrulhas,
    encontrar_posicoes_vigias
)

from game_content.sistema_vida import sistemavida, vidas_maximas
from game_content import coletaveis as coletaveis_modulo
from game_content import inventario as inventario_modulo
from game_content.fernanda import BossFernanda
from game_content.ricardo import ProfessorRicardo

pygame.init()

fonte = pygame.font.Font("fontes/PixelOperator8-Bold.ttf", 45)
fonte2 = pygame.font.Font("fontes/PixelOperator8.ttf", 28)
fonte3 = pygame.font.Font("fontes/PressStart2P-Regular.ttf", 15)

# configurando a tela
altura, largura = 750, 1200
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Find AI at CIN")
clock = pygame.time.Clock()
tela_de_inicio = True

fundo_inicio = pygame.image.load("imagens/cin_fnaf_final5 (1).png")
fundo_inicio = pygame.transform.scale(fundo_inicio, (largura, altura))

andar_atual = 0
mapa_atual = mapas[andar_atual]

# onde vai nascer o jogador
jogador = Jogador(x=15, y=15)
jogador.x, jogador.y = encontrar_posicao_inicial(mapa_atual)

patrulhas_por_andar = []
for mapa in mapas:
    lista_do_andar = []
    posicoes_v = encontrar_posicoes_patrulhas(mapa)
    
    # Cria um inimigo de patrulha para cada 'V' encontrado
    # Alterna entre horizontal e vertical para dar variedade
    for i, (x_v, y_v) in enumerate(posicoes_v):
        eixo = "horizontal" if i % 2 == 0 else "vertical" 
        lista_do_andar.append(InimigoPatrulha(x=x_v, y=y_v, direcao=eixo))
        
    patrulhas_por_andar.append(lista_do_andar)

vigias_por_andar = []

for mapa in mapas:
    lista_do_andar = []
    posicoes_g = encontrar_posicoes_vigias(mapa)

    for x_g, y_g in posicoes_g:
        lista_do_andar.append(InimigoVigia(x=x_g, y=y_g))

    vigias_por_andar.append(lista_do_andar)

# Boss Fernanda
boss_fernanda = BossFernanda()

# Professor Ricardo
professor_ricardo = ProfessorRicardo()

# Sistema de Vida
sistema_vida = sistemavida()

# coletáveis e inventário
lista_coletaveis = coletaveis_modulo.sortear_posicoes_coletaveis()
inventario = inventario_modulo.Inventario()

# cooldown para evitar trocar de andar várias vezes seguidas
tempo_ultima_escada = 0
COOLDOWN_ESCADA = 500

tempo_inicio_visao = 0
animacoes_revelacao_portas = []
jogo_ganho = False

# habilidade do ChatGPT: revela o mapa todo por alguns segundos
tempo_ultimo_uso_habilidade_gpt = -coletaveis_modulo.COOLDOWN_HABILIDADE_GPT
tempo_fim_habilidade_gpt = 0

# habilidade do Claude: recupera 1 vida, uso único
habilidade_claude_usada = False

# habilidade do Gemini: invencibilidade temporária
tempo_ultimo_uso_habilidade_gemini = -coletaveis_modulo.COOLDOWN_HABILIDADE_GEMINI

# instruções mostradas ao coletar cada IA ou chave
TEXTOS_INSTRUCAO_HABILIDADE = {
    "logo_claude": "Aperte 1 para recuperar vida!",
    "logo_gpt": "Aperte 2 para revelar o mapa!",
    "logo_gemini": "Aperte 3 para ficar invencivel!",
    "chave_azul": "Porta azul desbloqueada!",
    "chave_verde": "Porta verde desbloqueada!",
    "chave_vermelha": "Portas vermelhas desbloqueadas!",
}

DURACAO_MENSAGEM_INSTRUCAO = 3000
mensagem_instrucao = None
tempo_inicio_mensagem_instrucao = 0

# mensagem mostrada ao entrar em cada andar
TEXTOS_ANDARES = {
    0: "1º ANDAR DO CIN",
    1: "2º ANDAR DO CIN",
    2: "3º ANDAR DO CIN",
}

DURACAO_MENSAGEM_ANDAR = TEMPO_MAPA_VISIVEL + TEMPO_FECHAMENTO_VISAO
mensagem_andar = None
tempo_inicio_mensagem_andar = 0

# transição entre andares
DURACAO_TRANSICAO_ANDAR = 600

transicao_andar = {
    "fase": None,
    "inicio": 0,
    "andar_destino": 0,
    "tipo_spawn": None,
    "alpha": 0
}
# transições da Fernanda
DURACAO_TRANSICAO_FERNANDA = 1200

transicao_fernanda = {
    "inicio": 0,
    "texto": "",
    "proximo_estado": "normal",
    "acao": None
}


def iniciar_transicao_fernanda(texto, proximo_estado, acao=None):
    transicao_fernanda["inicio"] = pygame.time.get_ticks()
    transicao_fernanda["texto"] = texto
    transicao_fernanda["proximo_estado"] = proximo_estado
    transicao_fernanda["acao"] = acao

estado_jogo = "normal"

# textos da tela de game over
texto_go = fonte.render("GAME OVER", True, (220, 30, 30))
texto_reiniciar = fonte3.render("Pressione ESPAÇO para reiniciar", True, (255, 255, 255))

# loop do jogo
rodando = True
while rodando:

    eventos = pygame.event.get()

    for evento in eventos:
        if evento.type == pygame.QUIT:
            pygame.quit()
            rodando = False
            break

    if not rodando:
        break

    if tela_de_inicio:
        tela.blit(fundo_inicio, (0, 0))

        texto = fonte.render("Find AI at CIN", True, (255, 255, 255))
        texto2 = fonte2.render("Encontre a IA escondida no CIN!", True, (255, 255, 255))
        texto3 = fonte3.render("Pressione ESPAÇO para começar", True, (255, 255, 255))

        tela.blit(texto, (largura // 2 - texto.get_width() // 2, 125))
        tela.blit(texto2, (largura // 2 - texto2.get_width() // 2, 200))
        tela.blit(texto3, (largura // 2 - texto3.get_width() // 2, 500))

        pygame.display.flip()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            tela_de_inicio = False
            tempo_inicio_visao = pygame.time.get_ticks()

            mensagem_andar = TEXTOS_ANDARES[andar_atual]
            tempo_inicio_mensagem_andar = pygame.time.get_ticks()

    else:
        teclas = pygame.key.get_pressed()
        patrulhas_atuais = patrulhas_por_andar[andar_atual]
        vigias_atuais = vigias_por_andar[andar_atual]

        # --- estado: jogador morreu ---
        if sistema_vida.fim_jogo:
            tela.fill((0, 0, 0))

            tela.blit(texto_go, (largura // 2 - texto_go.get_width() // 2, altura // 2 - 80))
            tela.blit(texto_reiniciar, (largura // 2 - texto_reiniciar.get_width() // 2, altura // 2 + 20))

            pygame.display.flip()

            if teclas[pygame.K_SPACE]:
                sistema_vida = sistemavida()
                andar_atual = 0
                mapa_atual = mapas[andar_atual]
                jogador.x, jogador.y = encontrar_posicao_inicial(mapa_atual)
                jogo_ganho = False
                lista_coletaveis = coletaveis_modulo.sortear_posicoes_coletaveis()
                inventario = inventario_modulo.Inventario()
                tempo_inicio_visao = pygame.time.get_ticks()
                animacoes_revelacao_portas = []
                estado_jogo = "normal"
                boss_fernanda = BossFernanda()
                professor_ricardo = ProfessorRicardo()
                tempo_ultimo_uso_habilidade_gpt = -coletaveis_modulo.COOLDOWN_HABILIDADE_GPT
                tempo_fim_habilidade_gpt = 0
                habilidade_claude_usada = False
                tempo_ultimo_uso_habilidade_gemini = -coletaveis_modulo.COOLDOWN_HABILIDADE_GEMINI
                mensagem_instrucao = None
                mensagem_andar = TEXTOS_ANDARES[andar_atual]
                tempo_inicio_mensagem_andar = pygame.time.get_ticks()
                transicao_andar = {
                    "fase": None,
                    "inicio": 0,
                    "andar_destino": 0,
                    "tipo_spawn": None,
                    "alpha": 0
                }
        
        # --- estado: jogador ganhou ---
        elif jogo_ganho:
            tela.fill((0, 0, 0))

            texto_ganhou = fonte.render("VOCÊ GANHOU!", True, (0, 255, 0))
            texto_sub = fonte2.render("Você encontrou a IA no CIN!", True, (255, 255, 255))
            texto_sair = fonte3.render("Pressione ESPAÇO para sair", True, (255, 255, 255))

            tela.blit(texto_ganhou, (largura // 2 - texto_ganhou.get_width() // 2, altura // 2 - 100))
            tela.blit(texto_sub, (largura // 2 - texto_sub.get_width() // 2, altura // 2))
            tela.blit(texto_sair, (largura // 2 - texto_sair.get_width() // 2, altura // 2 + 80))

            pygame.display.flip()

            for evento in eventos:
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    rodando = False

        # --- estado: jogo normal ---
        else:
            if estado_jogo == "transicao_fernanda":
                tempo_passado = pygame.time.get_ticks() - transicao_fernanda["inicio"]
                progresso = tempo_passado / DURACAO_TRANSICAO_FERNANDA

                if progresso > 1:
                    progresso = 1

                tela.fill((0, 0, 0))

                if progresso < 0.5:
                    alpha_texto = int(255 * (progresso / 0.5))
                else:
                    alpha_texto = int(255 * ((1 - progresso) / 0.5))

                if alpha_texto < 0:
                    alpha_texto = 0

                texto_transicao = fonte.render(
                    transicao_fernanda["texto"],
                    True,
                    (255, 255, 255)
                )

                texto_transicao.set_alpha(alpha_texto)

                rect_texto = texto_transicao.get_rect(
                    center=(largura // 2, altura // 2)
                )

                tela.blit(texto_transicao, rect_texto)

                pygame.display.flip()
                clock.tick(45)

                if tempo_passado >= DURACAO_TRANSICAO_FERNANDA:
                    if transicao_fernanda["acao"] == "iniciar_quiz":
                        boss_fernanda.marcar_dialogo_inicial_mostrado()
                        boss_fernanda.iniciar_quiz()

                    elif transicao_fernanda["acao"] == "iniciar_recompensa":
                        boss_fernanda.iniciar_recompensa()

                    estado_jogo = transicao_fernanda["proximo_estado"]

                continue
            elif estado_jogo == "quiz_fernanda":
                for evento in eventos:
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_1 or evento.key == pygame.K_KP1:
                            boss_fernanda.responder_quiz(0, sistema_vida)

                        elif evento.key == pygame.K_2 or evento.key == pygame.K_KP2:
                            boss_fernanda.responder_quiz(1, sistema_vida)

                        elif evento.key == pygame.K_3 or evento.key == pygame.K_KP3:
                            boss_fernanda.responder_quiz(2, sistema_vida)

                        elif evento.key == pygame.K_4 or evento.key == pygame.K_KP4:
                            boss_fernanda.responder_quiz(3, sistema_vida)

                        elif evento.key == pygame.K_SPACE:
                            resultado_quiz = boss_fernanda.avancar_feedback_quiz()

                            if resultado_quiz == "aprovado":
                                iniciar_transicao_fernanda(
                                    "TESTE CONCLUIDO!",
                                    "recompensa_fernanda",
                                    "iniciar_recompensa"
                                )

                                estado_jogo = "transicao_fernanda"

                boss_fernanda.desenhar_tela_quiz(tela, sistema_vida)

                pygame.display.flip()
                clock.tick(45)
                continue

            elif estado_jogo == "recompensa_fernanda":
                for evento in eventos:
                    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                        acao_recompensa = boss_fernanda.avancar_recompensa()

                        if acao_recompensa == "coletar_claude":
                            if not inventario.tem_item("logo_claude"):
                                inventario.adicionar_item("logo_claude")
                                coletaveis_modulo.aplicar_buff("logo_claude", jogador, sistema_vida)

                            boss_fernanda.marcar_como_derrotada()
                            estado_jogo = "normal"
                            tempo_inicio_visao = pygame.time.get_ticks()

                boss_fernanda.desenhar_tela_recompensa(tela)

                pygame.display.flip()
                clock.tick(45)
                continue

            elif estado_jogo == "dialogo_ricardo":
                for evento in eventos:
                    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                        resultado_dialogo = professor_ricardo.avancar_dialogo()

                        if resultado_dialogo == "vitoria":
                            jogo_ganho = True
                            estado_jogo = "normal"

                        elif resultado_dialogo == "normal":
                            estado_jogo = "normal"
                            tempo_inicio_visao = pygame.time.get_ticks()

                professor_ricardo.desenhar_tela_dialogo(tela)

                pygame.display.flip()
                clock.tick(45)
                continue
            elif estado_jogo == "transicao_andar":
                tempo_atual_transicao = pygame.time.get_ticks()
                tempo_passado_transicao = tempo_atual_transicao - transicao_andar["inicio"]

                progresso_transicao = tempo_passado_transicao / DURACAO_TRANSICAO_ANDAR

                if progresso_transicao > 1:
                    progresso_transicao = 1

                if transicao_andar["fase"] == "saida":
                    transicao_andar["alpha"] = int(255 * progresso_transicao)

                    if progresso_transicao >= 1:
                        andar_atual = transicao_andar["andar_destino"]
                        mapa_atual = mapas[andar_atual]

                        if transicao_andar["tipo_spawn"] == "subida":
                            jogador.x, jogador.y = encontrar_posicao_inicial(mapa_atual)
                        else:
                            jogador.x, jogador.y = encontrar_posicao_spawn_descida(mapa_atual)

                        patrulhas_atuais = patrulhas_por_andar[andar_atual]
                        vigias_atuais = vigias_por_andar[andar_atual]

                        tempo_ultima_escada = pygame.time.get_ticks()
                        tempo_inicio_visao = pygame.time.get_ticks()

                        mensagem_andar = TEXTOS_ANDARES[andar_atual]
                        tempo_inicio_mensagem_andar = pygame.time.get_ticks()

                        transicao_andar["fase"] = "entrada"
                        transicao_andar["inicio"] = pygame.time.get_ticks()
                        transicao_andar["alpha"] = 255

                elif transicao_andar["fase"] == "entrada":
                    transicao_andar["alpha"] = int(255 * (1 - progresso_transicao))

                    if progresso_transicao >= 1:
                        transicao_andar["fase"] = None
                        transicao_andar["alpha"] = 0
                        estado_jogo = "normal"

            if estado_jogo == "normal":
                jogador.mover(
                    teclas,
                    largura,
                    altura,
                    mapa_atual,
                    lambda mapa, personagem: (
                        jogador_colide_com_mapa(mapa, personagem, inventario)
                        or boss_fernanda.bloqueia_passagem(personagem, andar_atual)
                    )
                )

                if boss_fernanda.esta_perto_do_jogador(jogador, andar_atual):
                    if not boss_fernanda.dialogo_inicial_mostrado:
                        iniciar_transicao_fernanda(
                            "PROF. FERNANDA",
                            "dialogo_fernanda"
                        )

                        estado_jogo = "transicao_fernanda"

                for evento in eventos:
                    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_f:
                        if professor_ricardo.esta_perto_do_jogador(jogador, andar_atual):
                            professor_ricardo.iniciar_dialogo(inventario.completo())
                            estado_jogo = "dialogo_ricardo"

                    if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_1, pygame.K_KP1):
                        if inventario.tem_item("logo_claude") and not habilidade_claude_usada and sistema_vida.vidas < vidas_maximas:
                            sistema_vida.ganhar_vida()
                            habilidade_claude_usada = True

                    if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_2, pygame.K_KP2):
                        agora = pygame.time.get_ticks()
                        cooldown_liberado = agora - tempo_ultimo_uso_habilidade_gpt >= coletaveis_modulo.COOLDOWN_HABILIDADE_GPT

                        if inventario.tem_item("logo_gpt") and cooldown_liberado:
                            tempo_ultimo_uso_habilidade_gpt = agora
                            tempo_fim_habilidade_gpt = agora + coletaveis_modulo.DURACAO_HABILIDADE_GPT

                    if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_3, pygame.K_KP3):
                        agora = pygame.time.get_ticks()
                        cooldown_liberado_gemini = agora - tempo_ultimo_uso_habilidade_gemini >= coletaveis_modulo.COOLDOWN_HABILIDADE_GEMINI

                        if inventario.tem_item("logo_gemini") and cooldown_liberado_gemini:
                            tempo_ultimo_uso_habilidade_gemini = agora
                            sistema_vida.ativar_invencibilidade_buff(coletaveis_modulo.DURACAO_HABILIDADE_GEMINI)

                for patrulha in patrulhas_atuais:
                    patrulha.mover(mapa_atual, jogador_colide_com_mapa)

                    if verificar_colisao(jogador, patrulha):
                        sistema_vida.receber_dano()

                for vigia in vigias_atuais:
                    vigia.atualizar(mapa_atual, jogador, jogador_colide_com_mapa)

                    if verificar_colisao(jogador, vigia):
                        sistema_vida.receber_dano()

                tempo_atual = pygame.time.get_ticks()

                if tempo_atual - tempo_ultima_escada > COOLDOWN_ESCADA:

                    if jogador_esta_na_escada_subida(mapa_atual, jogador):
                        if andar_atual == boss_fernanda.andar and not boss_fernanda.derrotada:
                            estado_jogo = "dialogo_fernanda"
                            tempo_ultima_escada = tempo_atual

                        elif andar_atual < len(mapas) - 1:
                            transicao_andar["fase"] = "saida"
                            transicao_andar["inicio"] = pygame.time.get_ticks()
                            transicao_andar["andar_destino"] = andar_atual + 1
                            transicao_andar["tipo_spawn"] = "subida"
                            transicao_andar["alpha"] = 0

                            estado_jogo = "transicao_andar"
                            tempo_ultima_escada = tempo_atual

                    elif jogador_esta_na_escada_descida(mapa_atual, jogador):
                        if andar_atual > 0:
                            transicao_andar["fase"] = "saida"
                            transicao_andar["inicio"] = pygame.time.get_ticks()
                            transicao_andar["andar_destino"] = andar_atual - 1
                            transicao_andar["tipo_spawn"] = "descida"
                            transicao_andar["alpha"] = 0

                            estado_jogo = "transicao_andar"
                            tempo_ultima_escada = tempo_atual

            elif estado_jogo == "dialogo_fernanda":
                for evento in eventos:
                    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                        iniciar_transicao_fernanda(
                            "PROVA DE IP",
                            "quiz_fernanda",
                            "iniciar_quiz"
                        )

                        estado_jogo = "transicao_fernanda"
            tela.fill((0, 0, 0))

            desenhar_mapa(tela, mapa_atual)

            for item in lista_coletaveis:
                if item.andar == andar_atual and not item.coletado:
                    tela.blit(item.image, item.rect)

            for patrulha in patrulhas_atuais:
                patrulha.desenhar(tela)
            for vigia in vigias_atuais:
                vigia.desenhar_campo_visao(tela)

            for vigia in vigias_atuais:
                vigia.desenhar(tela)
            boss_fernanda.desenhar(tela, andar_atual)
            professor_ricardo.desenhar(tela, andar_atual)

            aplicar_visao(
                tela,
                jogador,
                mapa_atual,
                tempo_inicio_visao,
                inventario,
                animacoes_revelacao_portas,
                revelar_tudo=pygame.time.get_ticks() < tempo_fim_habilidade_gpt
            )
            if estado_jogo == "normal":
                professor_ricardo.desenhar_mensagem_interacao(tela, jogador, andar_atual)

            if estado_jogo == "dialogo_fernanda":
                boss_fernanda.desenhar_dialogo(tela)

            jogador.desenhar(tela)
            sistema_vida.desenhar(tela)
            item_coletado = None

            if estado_jogo == "normal":
                item_coletado = coletaveis_modulo.atualizar_coletaveis(
                                                                tela,
                                                                jogador,
                                                                lista_coletaveis,
                                                                andar_atual,
                                                                eventos,
                                                                inventario,
                                                                sistema_vida
                                                            )

            if item_coletado is not None:
                if item_coletado.tipo in ["chave_azul", "chave_verde", "chave_vermelha"]:
                    animacao = criar_animacao_revelacao_portas(mapa_atual, item_coletado.tipo)

                    if animacao is not None:
                        animacoes_revelacao_portas.append(animacao)

                if item_coletado.tipo in TEXTOS_INSTRUCAO_HABILIDADE:
                    mensagem_instrucao = TEXTOS_INSTRUCAO_HABILIDADE[item_coletado.tipo]
                    tempo_inicio_mensagem_instrucao = pygame.time.get_ticks()

            if mensagem_instrucao is not None:
                if pygame.time.get_ticks() - tempo_inicio_mensagem_instrucao < DURACAO_MENSAGEM_INSTRUCAO:
                    texto_instrucao = fonte2.render(mensagem_instrucao, True, (255, 255, 255))
                    rect_instrucao = texto_instrucao.get_rect(center=(largura // 2, 40))
                    pygame.draw.rect(tela, (0, 0, 0), rect_instrucao.inflate(20, 12))
                    tela.blit(texto_instrucao, rect_instrucao)
                else:
                    mensagem_instrucao = None

            if mensagem_andar is not None:
                tempo_passado_andar = pygame.time.get_ticks() - tempo_inicio_mensagem_andar

                if tempo_passado_andar < DURACAO_MENSAGEM_ANDAR:
                    if tempo_passado_andar <= TEMPO_MAPA_VISIVEL:
                        alpha_andar = 255
                    else:
                        tempo_fade = tempo_passado_andar - TEMPO_MAPA_VISIVEL
                        progresso_fade = tempo_fade / TEMPO_FECHAMENTO_VISAO

                        if progresso_fade > 1:
                            progresso_fade = 1

                        alpha_andar = int(255 * (1 - progresso_fade))

                    texto_andar = fonte.render(mensagem_andar, True, (255, 255, 255))
                    rect_andar = texto_andar.get_rect(center=(largura // 2, altura // 2))

                    caixa_andar = rect_andar.inflate(30, 18)

                    superficie_andar = pygame.Surface(caixa_andar.size, pygame.SRCALPHA)

                    pygame.draw.rect(
                        superficie_andar,
                        (0, 0, 0, alpha_andar),
                        superficie_andar.get_rect()
                    )

                    pygame.draw.rect(
                        superficie_andar,
                        (255, 255, 255, alpha_andar),
                        superficie_andar.get_rect(),
                        3
                    )

                    texto_andar.set_alpha(alpha_andar)

                    tela.blit(superficie_andar, caixa_andar)
                    tela.blit(texto_andar, rect_andar)

                else:
                    mensagem_andar = None

            progresso_recarga_gpt = min(1.0, (pygame.time.get_ticks() - tempo_ultimo_uso_habilidade_gpt) / coletaveis_modulo.COOLDOWN_HABILIDADE_GPT)
            progresso_recarga_gemini = min(1.0, (pygame.time.get_ticks() - tempo_ultimo_uso_habilidade_gemini) / coletaveis_modulo.COOLDOWN_HABILIDADE_GEMINI)
            
            inventario_modulo.desenhar_hud(tela, inventario, {
                "logo_gpt": progresso_recarga_gpt,
                "logo_gemini": progresso_recarga_gemini,
            })

            if estado_jogo == "transicao_andar":
                camada_transicao = pygame.Surface((largura, altura))
                camada_transicao.fill((0, 0, 0))
                camada_transicao.set_alpha(transicao_andar["alpha"])
                tela.blit(camada_transicao, (0, 0))

            pygame.display.flip()

    clock.tick(45)
