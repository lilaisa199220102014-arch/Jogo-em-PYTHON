import random
import sys
import pygame

# ============================================================
# JOGO DA FORCA - PYGAME
# Tema: ANIMAIS
# ============================================================

pygame.init()

LARGURA, ALTURA = 1100, 700
MAX_ERROS = 6
FPS = 60

# Paleta de cores
FUNDO = (238, 244, 233)
VERDE_ESCURO = (49, 84, 52)
VERDE = (84, 129, 82)
VERDE_CLARO = (171, 198, 151)
BRANCO = (255, 255, 255)
PRETO = (35, 40, 34)
CINZA = (112, 118, 111)
CINZA_CLARO = (215, 220, 211)
DOURADO = (211, 178, 92)
VERMELHO = (182, 79, 72)
VERDE_SUCESSO = (67, 132, 86)
MARROM = (126, 87, 56)

# Fontes e janela
FONTE_TITULO = pygame.font.SysFont("segoeui", 46, bold=True)
FONTE_SUBTITULO = pygame.font.SysFont("segoeui", 26, bold=True)
FONTE_NORMAL = pygame.font.SysFont("segoeui", 22)
FONTE_PEQUENA = pygame.font.SysFont("segoeui", 18)
FONTE_PALAVRA = pygame.font.SysFont("segoeui", 42, bold=True)
FONTE_FINAL = pygame.font.SysFont("segoeui", 40, bold=True)
FONTE_TECLADO = pygame.font.SysFont("segoeui", 24, bold=True)

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo da Forca")
relogio = pygame.time.Clock()

# Pelo menos 15 palavras do tema escolhido.
PALAVRAS = [
    "ELEFANTE", "GIRAFA", "CACHORRO", "TARTARUGA", "BORBOLETA",
    "COELHO", "PINGUIM", "GOLFINHO", "CANGURU", "MACACO",
    "LEOPARDO", "JACARE", "TIGRE", "ZEBRA", "CAPIVARA",
    "RINOCERONTE", "PAPAGAIO", "HAMSTER", "CROCODILO", "HIPOPOTAMO",
    "URSO", "RAPOSA", "CAVALO", "PANDA", "CORUJA"
]

LETRAS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def escolher_palavra():
    """Escolhe uma palavra aleatória."""
    return random.choice(PALAVRAS)


def verificar_letra(palavra, letra):
    """Retorna True quando a letra está na palavra."""
    return letra in palavra


def verificar_vitoria(palavra, acertadas):
    """Retorna True quando todas as letras da palavra foram reveladas."""
    return all(letra in acertadas for letra in palavra)


def verificar_derrota(erros):
    """Retorna True quando o jogador chega aos 6 erros."""
    return erros >= MAX_ERROS


def mostrar_palavra(palavra, acertadas):
    """Monta a palavra com letras descobertas e espaços ocultos."""
    return " ".join(letra if letra in acertadas else "_" for letra in palavra)


def criar_teclado():
    """Cria os 26 botões do teclado virtual."""
    botoes = []
    linhas = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

    largura = 52
    altura = 48
    espacamento = 8
    centro_x = 770
    inicio_y = 470

    for linha_num, linha in enumerate(linhas):
        total = len(linha) * largura + (len(linha) - 1) * espacamento
        inicio_x = centro_x - total // 2
        y = inicio_y + linha_num * 58

        for coluna, letra in enumerate(linha):
            x = inicio_x + coluna * (largura + espacamento)
            botoes.append({"letra": letra, "rect": pygame.Rect(x, y, largura, altura)})

    return botoes


def desenhar_forca(surface, erros):
    """Desenha a forca progressivamente conforme os erros."""
    # Base e poste
    pygame.draw.line(surface, MARROM, (85, 390), (350, 390), 8)
    if erros >= 1:
        pygame.draw.line(surface, MARROM, (135, 390), (135, 120), 8)
    if erros >= 2:
        pygame.draw.line(surface, MARROM, (135, 120), (295, 120), 8)
        pygame.draw.line(surface, MARROM, (135, 155), (170, 120), 6)
        pygame.draw.line(surface, DOURADO, (295, 120), (295, 178), 5)
    if erros >= 3:
        pygame.draw.circle(surface, VERDE_ESCURO, (295, 208), 30, 5)
    if erros >= 4:
        pygame.draw.line(surface, VERDE_ESCURO, (295, 238), (295, 318), 7)
    if erros >= 5:
        pygame.draw.line(surface, VERDE_ESCURO, (295, 258), (250, 300), 7)
        pygame.draw.line(surface, VERDE_ESCURO, (295, 258), (340, 300), 7)
    if erros >= 6:
        pygame.draw.line(surface, VERDE_ESCURO, (295, 318), (255, 365), 7)
        pygame.draw.line(surface, VERDE_ESCURO, (295, 318), (335, 365), 7)


def desenhar_botao(surface, rect, legenda, cor_normal, cor_hover, fonte=FONTE_NORMAL):
    """Desenha um botão e retorna se o mouse está sobre ele."""
    mouse = pygame.mouse.get_pos()
    sobre = rect.collidepoint(mouse)
    cor = cor_hover if sobre else cor_normal
    pygame.draw.rect(surface, cor, rect, border_radius=10)
    pygame.draw.rect(surface, VERDE_ESCURO, rect, 2, border_radius=10)
    imagem = fonte.render(legenda, True, BRANCO)
    surface.blit(imagem, imagem.get_rect(center=rect.center))
    return sobre


def desenhar_teclado(surface, botoes, tentadas, palavra, ativo=True):
    """Desenha o teclado e desabilita letras já utilizadas."""
    mouse = pygame.mouse.get_pos()

    for botao in botoes:
        letra = botao["letra"]
        rect = botao["rect"]
        usada = letra in tentadas

        if usada:
            cor = VERDE_CLARO if letra in palavra else (234, 198, 194)
        elif ativo and rect.collidepoint(mouse):
            cor = DOURADO
        else:
            cor = BRANCO

        pygame.draw.rect(surface, cor, rect, border_radius=9)
        pygame.draw.rect(surface, VERDE_ESCURO, rect, 2, border_radius=9)

        imagem = FONTE_TECLADO.render(letra, True, CINZA if usada else PRETO)
        surface.blit(imagem, imagem.get_rect(center=rect.center))


def desenhar_tela_jogo(palavra, acertadas, tentadas, erros, botoes):
    """Desenha todos os elementos da rodada."""
    tela.fill(FUNDO)

    # Cabeçalho
    pygame.draw.rect(tela, VERDE_ESCURO, (0, 0, LARGURA, 82))
    pygame.draw.rect(tela, VERDE_CLARO, (0, 82, LARGURA, 6))
    titulo = FONTE_TITULO.render("Jogo da Forca", True, BRANCO)
    tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 41)))

    tema = FONTE_PEQUENA.render("Tema: Animais", True, VERDE_ESCURO)
    tela.blit(tema, (30, 105))

    # Painel da forca
    painel_forca = pygame.Rect(25, 135, 410, 290)
    pygame.draw.rect(tela, BRANCO, painel_forca, border_radius=16)
    pygame.draw.rect(tela, VERDE_ESCURO, painel_forca, 2, border_radius=16)
    rotulo = FONTE_SUBTITULO.render("Forca", True, VERDE_ESCURO)
    tela.blit(rotulo, (50, 157))
    desenhar_forca(tela, erros)

    # Painel da palavra
    painel_palavra = pygame.Rect(455, 135, 620, 185)
    pygame.draw.rect(tela, BRANCO, painel_palavra, border_radius=16)
    pygame.draw.rect(tela, VERDE_ESCURO, painel_palavra, 2, border_radius=16)
    rotulo = FONTE_SUBTITULO.render("Palavra", True, VERDE_ESCURO)
    tela.blit(rotulo, (480, 157))

    exibida = mostrar_palavra(palavra, acertadas)
    fonte = FONTE_PALAVRA if len(palavra) < 11 else pygame.font.SysFont("segoeui", 33, bold=True)
    imagem = fonte.render(exibida, True, PRETO)
    tela.blit(imagem, imagem.get_rect(center=(painel_palavra.centerx, 245)))

    # Status
    erros_restantes = MAX_ERROS - erros
    painel_status = pygame.Rect(455, 335, 620, 95)
    pygame.draw.rect(tela, BRANCO, painel_status, border_radius=16)
    pygame.draw.rect(tela, VERDE_ESCURO, painel_status, 2, border_radius=16)

    cor_erros = VERMELHO if erros >= 4 else VERDE_ESCURO
    tela.blit(FONTE_NORMAL.render(f"Erros: {erros}/{MAX_ERROS}", True, cor_erros), (480, 355))
    tela.blit(FONTE_NORMAL.render(f"Tentativas restantes: {erros_restantes}", True, VERDE_ESCURO), (480, 392))

    usadas = ", ".join(sorted(tentadas)) if tentadas else "nenhuma"
    tela.blit(FONTE_PEQUENA.render(f"Letras usadas: {usadas}", True, CINZA), (690, 355))

    tela.blit(FONTE_SUBTITULO.render("Teclado", True, VERDE_ESCURO), (480, 443))
    desenhar_teclado(tela, botoes, tentadas, palavra, True)

    ajuda = FONTE_PEQUENA.render("Clique nas letras ou use o teclado do computador.", True, CINZA)
    tela.blit(ajuda, (480, 652))


def desenhar_tela_final(ganhou, palavra, botao):
    """Desenha a tela de vitória ou derrota."""
    tela.fill(FUNDO)
    pygame.draw.rect(tela, VERDE_ESCURO, (0, 0, LARGURA, 90))

    titulo = "Você venceu!" if ganhou else "Você perdeu!"
    imagem_titulo = FONTE_TITULO.render(titulo, True, BRANCO)
    tela.blit(imagem_titulo, imagem_titulo.get_rect(center=(LARGURA // 2, 45)))

    painel = pygame.Rect(280, 145, 540, 410)
    pygame.draw.rect(tela, BRANCO, painel, border_radius=18)
    pygame.draw.rect(tela, VERDE_ESCURO, painel, 2, border_radius=18)

    cor = VERDE_SUCESSO if ganhou else VERMELHO
    mensagem = "Parabéns! A palavra foi descoberta." if ganhou else "As 6 tentativas acabaram."
    tela.blit(FONTE_SUBTITULO.render(mensagem, True, cor),
              FONTE_SUBTITULO.render(mensagem, True, cor).get_rect(center=(painel.centerx, 225)))

    tela.blit(FONTE_NORMAL.render("A palavra era:", True, CINZA),
              FONTE_NORMAL.render("A palavra era:", True, CINZA).get_rect(center=(painel.centerx, 295)))

    fonte = FONTE_FINAL if len(palavra) <= 12 else pygame.font.SysFont("segoeui", 31, bold=True)
    imagem_palavra = fonte.render(palavra, True, VERDE_ESCURO)
    tela.blit(imagem_palavra, imagem_palavra.get_rect(center=(painel.centerx, 345)))

    desenhar_botao(tela, botao, "Jogar novamente", VERDE, VERDE_ESCURO)

    ajuda = FONTE_PEQUENA.render("Pressione ENTER ou ESPAÇO também para jogar novamente.", True, CINZA)
    tela.blit(ajuda, ajuda.get_rect(center=(painel.centerx, 505)))


def tentar_letra(letra, palavra, tentadas, acertadas, erros):
    """Registra a letra e aumenta os erros quando necessário."""
    letra = letra.upper()

    if letra not in LETRAS or letra in tentadas:
        return erros

    tentadas.add(letra)

    if verificar_letra(palavra, letra):
        acertadas.add(letra)
    else:
        erros += 1

    return erros


def nova_partida(botoes):
    """Cria uma nova rodada."""
    return {
        "palavra": escolher_palavra(),
        "acertadas": set(),
        "tentadas": set(),
        "erros": 0,
        "estado": "jogando",
        "botoes": botoes,
    }


def main():
    botoes = criar_teclado()
    jogo = nova_partida(botoes)
    botao_novamente = pygame.Rect(430, 430, 240, 56)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if jogo["estado"] == "jogando":
                # Entrada pelo teclado físico
                if evento.type == pygame.KEYDOWN:
                    if evento.unicode and evento.unicode.upper() in LETRAS:
                        jogo["erros"] = tentar_letra(
                            evento.unicode.upper(),
                            jogo["palavra"],
                            jogo["tentadas"],
                            jogo["acertadas"],
                            jogo["erros"],
                        )

                # Entrada pelo teclado virtual
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    for botao in botoes:
                        if botao["rect"].collidepoint(evento.pos):
                            jogo["erros"] = tentar_letra(
                                botao["letra"],
                                jogo["palavra"],
                                jogo["tentadas"],
                                jogo["acertadas"],
                                jogo["erros"],
                            )
                            break

                if verificar_vitoria(jogo["palavra"], jogo["acertadas"]):
                    jogo["estado"] = "venceu"
                elif verificar_derrota(jogo["erros"]):
                    jogo["estado"] = "perdeu"

            else:
                # Tela final: jogar novamente
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if botao_novamente.collidepoint(evento.pos):
                        jogo = nova_partida(botoes)

                if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    jogo = nova_partida(botoes)

        if jogo["estado"] == "jogando":
            desenhar_tela_jogo(
                jogo["palavra"],
                jogo["acertadas"],
                jogo["tentadas"],
                jogo["erros"],
                botoes,
            )
        else:
            desenhar_tela_final(
                jogo["estado"] == "venceu",
                jogo["palavra"],
                botao_novamente,
            )

        pygame.display.flip()
        relogio.tick(FPS)


if __name__ == "__main__":
    main()
