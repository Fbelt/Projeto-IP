def verificar_colisao(jogador, inimigo):
    colidiu = (
        jogador.x < inimigo.x + inimigo.largura and
        jogador.x + jogador.largura > inimigo.x and
        jogador.y < inimigo.y + inimigo.altura and
        jogador.y + jogador.altura > inimigo.y
    )

    if colidiu:
        knockback = 0
        if jogador.x < inimigo.x:
            jogador.x -= knockback
        else:
            jogador.x += knockback

        if jogador.y < inimigo.y:
            jogador.y -= knockback
        else:
            jogador.y += knockback
        return True
    
    return False

