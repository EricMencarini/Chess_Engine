#################################################################
#Verifica o estado atual do jogo e lida com os inputs do usuário#
#################################################################

import pygame as pg
import ChessEngine, IA


#Definindo as propriedades do tabuleiro
LARGURA = ALTURA = 512
DIMENSÃO = 8   # 8x8 (Tabuleiro padrão)
CASAS = ALTURA // DIMENSÃO
MAX_FPS = 15
IMAGENS = {}

'''
Carrega as imagens das peças no tabuleiro
'''

def carrega_imagens():
    peças = ['Pb','Tb','Bb','Cb','Db','Rb',  #Peças Brancas
             'Pp','Tp','Bp','Cp','Dp','Rp']  #Peças Pretas
    for peça in peças:
        IMAGENS[peça] = pg.transform.scale(pg.image.load("imagens_peças/" + peça + ".png"), (CASAS, CASAS)) 


'''
Verifica os inputs do usuário e atualiza as imagens.
'''   
def main():
    pg.init()
    tela = pg.display.set_mode((LARGURA, ALTURA))
    relógio = pg.time.Clock()
    tela.fill(pg.Color("white"))
    estado_do_jogo = ChessEngine.Estado_Atual_do_Jogo()
    valida_jogadas = estado_do_jogo.valida_todas_jogadas()
    jogada_realizada = False
    animação = False
    carrega_imagens()
    execução = True
    casa_selecionada = ()  #Nenhuma casa foi selecionada. Irá rastrear o último click do usuário
    clicks_jogador = [] #Rastreia os clicks do player.
    game_over = False
    jogador_um = True   #True = Pessoa / False = I.A
    jogador_dois = False #True = Pessoa / False = I.A

    while execução:
        turno_jogador = (estado_do_jogo.branco_joga and jogador_um) or (not estado_do_jogo.branco_joga and jogador_dois)

        for e in pg.event.get():
            if e.type == pg.QUIT:
                execução = False

            ##MOUSE##   
            elif e.type == pg.MOUSEBUTTONDOWN:
                if not game_over and turno_jogador:
                    coord = pg.mouse.get_pos() #(x,y))
                    coluna = coord[0] // CASAS
                    linha  = coord[1] // CASAS  
                    
                    if casa_selecionada == (linha,coluna):  #Verifica se o usuário clicou no mesmo lugar duas vezes.
                        casa_selecionada = () 
                        clicks_jogador = []                #Limpa os clicks
                    else:
                        casa_selecionada = (linha,coluna)
                        clicks_jogador.append(casa_selecionada)#Adicionamos para o primeiro e segundo click.
                    
                    if len(clicks_jogador) == 2:
                        jogada = ChessEngine.Jogadas(clicks_jogador[0], clicks_jogador[1], estado_do_jogo.tabuleiro)      
                        print(jogada.notacao_algebrica()) 
                        for i in range(len(valida_jogadas)):
                                if jogada == valida_jogadas[i]:
                                    estado_do_jogo.cria_jogada(valida_jogadas[i])
                                    jogada_realizada = True  
                                    animação = True    
                                    casa_selecionada = () # Reseta os clicks do usuário.
                                    clicks_jogador = []
                    if not jogada_realizada:
                            clicks_jogador = [casa_selecionada]

            ##TECLADO##
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_z:
                    estado_do_jogo.refaz_jogada()   #'Z'para refazer a jogada
                    jogada_realizada = True
                    animação = False
                if e.key == pg.K_r:
                    estado_do_jogo = ChessEngine.Estado_Atual_do_Jogo()
                    valida_jogadas = estado_do_jogo.valida_todas_jogadas()
                    casa_selecionada = ()
                    clicks_jogador = []
                    jogada_realizada = False
                    animação = False        
                    game_over = False

        if not game_over and not turno_jogador:
            jogada_ia = IA.encontra_melhor_jogada_min_max(estado_do_jogo, valida_jogadas)
            if jogada_ia is None:
                jogada_ia = IA.jogada_random(valida_jogadas)
            estado_do_jogo.cria_jogada(jogada_ia)
            jogada_realizada = True
            animação = True


        if jogada_realizada:
            if animação:
                anima_movimentação_peças(estado_do_jogo.log_jogadas[-1], tela, estado_do_jogo.tabuleiro, relógio)
            valida_jogadas = estado_do_jogo.valida_todas_jogadas()
            jogada_realizada = False
            animação = False


        cria_estado_do_jogo(tela, estado_do_jogo, valida_jogadas, casa_selecionada)
        
        if estado_do_jogo.checkmate:
            game_over = True
            if estado_do_jogo.branco_joga:
                texto_fim_de_jogo(tela,"Pretas ganham por Check-Mate")
            else:
                texto_fim_de_jogo(tela,"Brancas ganham por Check-Mate")    
        elif estado_do_jogo.afogamento:
            game_over = True
            texto_fim_de_jogo(tela, "Empate por afogamento")

        relógio.tick(MAX_FPS)
        pg.display.flip()


'''
Adiciona brilho nas casas selecionadas e possiveis movimentos
'''
def brilho_casas(tela, estado_do_jogo, valida_jogadas, casa_selecionada):
    if casa_selecionada != ():
        l, c = casa_selecionada
        if estado_do_jogo.tabuleiro[l][c][1] == ("b" if estado_do_jogo.branco_joga else 'p'):
            #brilho casa selecionada    
            s = pg.Surface((CASAS, CASAS))
            s.set_alpha(100) #transparente em 0 // Opaco em 255
            s.fill(pg.Color('blue'))
            tela.blit(s, (c *CASAS, l*CASAS))
            #brilho das casas de possiveis movimentos
            s.fill(pg.Color('yellow'))
            for jogada in valida_jogadas:
                if jogada.linha_ini == l and jogada.coluna_ini == c:
                    tela.blit(s,(jogada.coluna_fim*CASAS, jogada.linha_fim*CASAS))



'''
Responsável pela parte gráfica de peças e casas no tabuleiro.
'''
def cria_estado_do_jogo(tela, estado_do_jogo, valida_jogadas, casa_selecionada):
    cria_casas(tela)                           #Cria as casas no tabuleiro
    brilho_casas(tela, estado_do_jogo, valida_jogadas, casa_selecionada)
    cria_peças(tela, estado_do_jogo.tabuleiro) #Cria as peças no tabuleiro

'''
Cria as casas no tabuleiro
'''
def cria_casas(tela):
    global cores
    cores = [pg.Color("white"), pg.Color("gray")]
    for l in range(DIMENSÃO):
        for c in range(DIMENSÃO):
            cor = cores[((l+c) % 2)]
            pg.draw.rect(tela, cor, pg.Rect(c*CASAS, l*CASAS, CASAS, CASAS))

'''
Cria as peças no tabuleiro
'''
def cria_peças(tela, tabuleiro):
    for l in range(DIMENSÃO):
        for c in range(DIMENSÃO):
            peça = tabuleiro[l][c]
            if peça != "--":
                tela.blit(IMAGENS[peça], pg.Rect(c*CASAS, l*CASAS, CASAS, CASAS))


'''
Anima a movimentação das peças
'''
def anima_movimentação_peças(jogada, tela, tabuleiro, relógio):
    global cores
    dr = jogada.linha_fim  - jogada.linha_ini
    dc = jogada.coluna_fim - jogada.coluna_ini
    frames = 2
    conta_frames = (abs(dr) + abs(dc)) * frames
    for frame in range(conta_frames + 1):
        l, c =((jogada.linha_ini + dr*frame/conta_frames, jogada.coluna_ini + dc*frame/conta_frames))
        cria_casas(tela)
        cria_peças(tela, tabuleiro)
        cor = cores[(jogada.linha_fim + jogada.coluna_fim) % 2]
        casa_fim = pg.Rect(jogada.coluna_fim*CASAS, jogada.linha_fim*CASAS, CASAS, CASAS)
        pg.draw.rect(tela, cor, casa_fim)
        if jogada.peça_capturada != "--":
           tela.blit(IMAGENS[jogada.peça_capturada], casa_fim)
           
        tela.blit(IMAGENS[jogada.peça_jogada], pg.Rect(c*CASAS, l*CASAS, CASAS, CASAS)) 
        pg.display.flip()
        relógio.tick(60)


def texto_fim_de_jogo(tela, texto):
    font = pg.font.SysFont("Helvitca", 32, True, False)
    texto_tela = font.render(texto, 0, pg.Color('Gray'))
    texto_posição = pg.Rect(0,0, LARGURA, ALTURA).move(LARGURA/2 - texto_tela.get_width()/2, ALTURA/2 - texto_tela.get_height()/2)
    tela.blit(texto_tela, texto_posição)
    texto_tela = font.render(texto, 0, pg.Color("Black"))
    tela.blit(texto_tela, texto_posição.move(2,2))

if __name__ == "__main__":
    main()

