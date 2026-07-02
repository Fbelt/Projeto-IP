import pygame

from game_content.personagens import jogador as Jogador
from game_content.personagens import inimigo as Inimigo
from game_content.visao import aplicar_visao, criar_animacao_revelacao_portas
from game_content.batalha import verificar_colisao
from game_content.mapa import (
    mapas,
    desenhar_mapa,
    encontrar_posicao_inicial,
    encontrar_posicao_spawn_descida,
    encontrar_posicao_inimigo,
    jogador_colide_com_mapa,
    jogador_esta_na_escada_subida,
    jogador_esta_na_escada_descida,
    encontrar_posicoes_patrulhas
)

from game_content.sistema_vida import sistemavida
from game_content import coletaveis as coletaveis_modulo
from game_content import inventario as inventario_modulo

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

# inimigos -- um por andar
inimigos = []
for mapa in mapas:
    x_inimigo, y_inimigo = encontrar_posicao_inimigo(mapa)
    inimigos.append(Inimigo(x=x_inimigo, y=y_inimigo))


patrulhas_por_andar = []
for mapa in mapas:
    lista_do_andar = []
    posicoes_v = encontrar_posicoes_patrulhas(mapa)
    
    # Cria um inimigo de patrulha para cada 'V' encontrado
    # Alterna entre horizontal e vertical para dar variedade
    for i, (x_v, y_v) in enumerate(posicoes_v):
        eixo = "horizontal" if i % 2 == 0 else "vertical"
        # Importante: Se sua classe no personagens.py começar com maiúscula, use InimigoPatrulha
        from game_content.personagens import InimigoPatrulha 
        lista_do_andar.append(InimigoPatrulha(x=x_v, y=y_v, direcao=eixo))
        
    patrulhas_por_andar.append(lista_do_andar)

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

    else:
        teclas = pygame.key.get_pressed()
        inimigo_atual = inimigos[andar_atual]

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

            if teclas[pygame.K_SPACE]:
                rodando = False

        # --- estado: jogo normal ---
        else:
            jogador.mover(
                teclas,
                largura,
                altura,
                mapa_atual,
                lambda mapa, personagem: jogador_colide_com_mapa(mapa, personagem, inventario)
            )
            
            # a própria classe sistemavida já ignora dano repetido
            # durante a janela de invencibilidade (tempo_invencivel_pos_dano)
            if verificar_colisao(jogador, inimigo_atual):
                sistema_vida.receber_dano()

            patrulhas_atuais = patrulhas_por_andar[andar_atual]
            for patrulha in patrulhas_atuais:
                # Faz a patrulha andar e rebater nas paredes
                patrulha.mover(mapa_atual, jogador_colide_com_mapa)
                
                # Checa colisão com a patrulha (Usando os 2 argumentos originais)
                if verificar_colisao(jogador, patrulha):
                    sistema_vida.receber_dano()

            tempo_atual = pygame.time.get_ticks()

            if tempo_atual - tempo_ultima_escada > COOLDOWN_ESCADA:

                # sobe para o próximo andar usando S
                if jogador_esta_na_escada_subida(mapa_atual, jogador):
                    if andar_atual < len(mapas) - 1:
                        andar_atual += 1
                        mapa_atual = mapas[andar_atual]

                        # ao subir, nasce no P do novo andar
                        jogador.x, jogador.y = encontrar_posicao_inicial(mapa_atual)

                        tempo_ultima_escada = tempo_atual
                        tempo_inicio_visao = pygame.time.get_ticks()

                        if inventario.completo():
                            jogo_ganho = True

                # desce para o andar anterior usando B
                elif jogador_esta_na_escada_descida(mapa_atual, jogador):
                    if andar_atual > 0:
                        andar_atual -= 1
                        mapa_atual = mapas[andar_atual]

                        # ao descer, nasce no p do andar anterior
                        jogador.x, jogador.y = encontrar_posicao_spawn_descida(mapa_atual)

                        tempo_ultima_escada = tempo_atual
                        tempo_inicio_visao = pygame.time.get_ticks()

            tela.fill((0, 0, 0))

            desenhar_mapa(tela, mapa_atual)

            for item in lista_coletaveis:
                if item.andar == andar_atual and not item.coletado:
                    tela.blit(item.image, item.rect)

            inimigo_atual.desenhar(tela)

            aplicar_visao(
                        tela,
                        jogador,
                        mapa_atual,
                        tempo_inicio_visao,
                        inventario,
                        animacoes_revelacao_portas
                    )
            
            for patrulha in patrulhas_atuais:
                patrulha.desenhar(tela)

            
            jogador.desenhar(tela)
            sistema_vida.desenhar(tela)

            item_coletado = coletaveis_modulo.atualizar_coletaveis(
                                                                tela,
                                                                jogador,
                                                                lista_coletaveis,
                                                                andar_atual,
                                                                eventos,
                                                                inventario
                                                            )

            if item_coletado is not None:
                if item_coletado.tipo in ["chave_azul", "chave_verde", "chave_vermelha"]:
                    animacao = criar_animacao_revelacao_portas(mapa_atual, item_coletado.tipo)

                    if animacao is not None:
                        animacoes_revelacao_portas.append(animacao)

                        inventario_modulo.desenhar_hud(tela, inventario)

            pygame.display.flip()

    clock.tick(45)
