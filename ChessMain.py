#################################################################
#Verifica o estado atual do jogo e lida com os inputs do usuário#
#################################################################

import pygame as pg
import ChessEngine


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
    carrega_imagens()
    execução = True
    casa_selecionada = ()  #Nenhuma casa foi selecionada. Irá rastrear o último click do usuário
    clicks_jogador = [] #Rastreia os clicks do player.

    while execução:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                execução = False

            ##MOUSE##   
            elif e.type == pg.MOUSEBUTTONDOWN:
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
                   if jogada in valida_jogadas:
                        estado_do_jogo.cria_jogada(jogada)
                        jogada_realizada = True      
                        casa_selecionada = () # Reseta os clicks do usuário.
                        clicks_jogador = []
                   else:
                        clicks_jogador = [casa_selecionada]

            ##TECLADO##
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_z:
                    estado_do_jogo.refaz_jogada()
                    jogada_realizada = True

        if jogada_realizada:
            valida_jogadas = estado_do_jogo.valida_todas_jogadas()
            jogada_realizada = False

        cria_estado_do_jogo(tela, estado_do_jogo)
        relógio.tick(MAX_FPS)
        pg.display.flip()

'''
Responsável pela parte gráfica de peças e casas no tabuleiro.
'''
def cria_estado_do_jogo(tela, estado_do_jogo):
    cria_casas(tela)                           #Cria as casas no tabuleiro
    cria_peças(tela, estado_do_jogo.tabuleiro) #Cria as peças no tabuleiro

'''
Cria as casas no tabuleiro
'''
def cria_casas(tela):
    cores = [pg.Color("white"), pg.Color("gray")]
    for linha in range(DIMENSÃO):
        for coluna in range(DIMENSÃO):
            cor = cores[((linha+coluna)% 2)]
            pg.draw.rect(tela, cor, pg.Rect(coluna*CASAS, linha*CASAS, CASAS, CASAS))

'''
Cria as peças no tabuleiro
'''
def cria_peças(tela, tabuleiro):
    for linha in range(DIMENSÃO):
        for coluna in range(DIMENSÃO):
            peça = tabuleiro[linha][coluna]
            if peça != "--":
                tela.blit(IMAGENS[peça], pg.Rect(coluna*CASAS, linha*CASAS, CASAS, CASAS))


if __name__ == "__main__":
    main()

