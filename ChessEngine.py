#######################################################################
#Arquivo que irá resolver os dados armazenados do estado atual do jogo#
#Verifica também os movimentos validos e faz um track dos movimentos  #
#######################################################################


'''
Criando o tabuleiro do jogo.
'''
class Estado_Atual_do_Jogo():
    def __init__(self):
        #Indica a primeria letra da peça e a sua respectiva cor.
        #"--" Indica os espaços em branco no tabuleiro.
        self.tabuleiro = [
            ["Tp","Cp","Bp","Dp","Rp","Bp","Cp","Tp"],
            ["Pp","Pp","Pp","Pp","Pp","Pp","Pp","Pp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["Pb","Pb","Pb","Pb","Pb","Pb","Pb","Pb"],
            ["Tb","Cb","Bb","Db","Rb","Bb","Cb","Tb"]]
        self.jogadaFuncoes = {'P':self.jogada_peao,'T':self.jogada_torre,'C':self.jogada_cavalo,
                              'B':self.jogada_bispo,'D':self.jogada_dama,'R':self.jogada_rei, }
        
        self.branco_joga = True   ##Define que o branco começa jogando
        self.log_jogadas = []     ##Gera lista dos movimentos jogados
        self.posicao_rei_branco = (7,4)
        self.posicao_rei_preto  = (0,4)
        self.checkmate = False
        self.afogamento = False
        self.cravada= []
        self.checks = []
        self.enpassant = () #Verifica se o enpassant é possivel
        self.roque_pequeno = Roque_Pequeno_Atual(True, True, True, True)
        self.roque_pequeno_log = [Roque_Pequeno_Atual(self.roque_pequeno.rbs, self.roque_pequeno.rps, 
                                                      self.roque_pequeno.dbs, self.roque_pequeno.dps)]



    def cria_jogada(self, jogada):
        self.tabuleiro[jogada.linha_ini][jogada.coluna_ini] = "--"
        self.tabuleiro[jogada.linha_fim][jogada.coluna_fim] = jogada.peça_jogada 
        self.log_jogadas.append(jogada)                       #Lista de movimentos jogados
        self.branco_joga = not self.branco_joga
        if jogada.peça_jogada == "Rb":
            self.posicao_rei_branco = (jogada.linha_fim, jogada.coluna_fim)
        elif jogada.peça_jogada == "Rp":
            self.posicao_rei_preto = (jogada.linha_fim, jogada.coluna_fim)    

        #Promoção de Peões
        if jogada.promocao_peao:
            self.tabuleiro[jogada.linha_fim][jogada.coluna_fim] = 'D' + jogada.peça_jogada[1]

        #En passant
        if jogada.enpassant_jogada:
            self.tabuleiro[jogada.linha_ini][jogada.coluna_fim] = "--" #Capturando a peça

        if jogada.peça_jogada[0] == "P" and abs(jogada.linha_ini - jogada.linha_fim) == 2:
            self.enpassant = ((jogada.linha_ini + jogada.linha_fim)//2, jogada.coluna_ini)
        else:
            self.enpassant = ()

        #Roque

        if jogada.roque_jogada:
            if jogada.coluna_fim - jogada.coluna_ini == 2:
               self.tabuleiro[jogada.linha_fim][jogada.coluna_fim - 1] = self.tabuleiro[jogada.linha_fim][jogada.coluna_fim+1]
               self.tabuleiro[jogada.linha_fim][jogada.coluna_fim + 1] = "--"
            else:
               self.tabuleiro[jogada.linha_fim][jogada.coluna_fim + 1] = self.tabuleiro[jogada.linha_fim][jogada.coluna_fim-2]
               self.tabuleiro[jogada.linha_fim][jogada.coluna_fim - 2] = "--"    

        self.update_roque_pequeno(jogada)
        self.roque_pequeno_log.append(Roque_Pequeno_Atual(self.roque_pequeno.rbs, self.roque_pequeno.rps, 
                                                         self.roque_pequeno.dbs, self.roque_pequeno.dps))

    '''
    Refaz último movimento feito
    '''
    def refaz_jogada(self):
        if len(self.log_jogadas) != 0:
            jogada = self.log_jogadas.pop()
            self.tabuleiro[jogada.linha_ini][jogada.coluna_ini] = jogada.peça_jogada
            self.tabuleiro[jogada.linha_fim][jogada.coluna_fim] = jogada.peça_capturada
            self.branco_joga = not self.branco_joga 
            if jogada.peça_jogada == "Rb":
                self.posicao_rei_branco = (jogada.linha_ini, jogada.coluna_ini)
            elif jogada.peça_jogada == "Rp":
                self.posicao_rei_preto = (jogada.linha_ini, jogada.coluna_ini)   

            #Enpassant
            if jogada.enpassant_jogada:
                self.tabuleiro[jogada.linha_fim][jogada.coluna_fim] = "--"
                self.tabuleiro[jogada.linha_ini][jogada.coluna_fim] = jogada.peça_capturada
                self.enpassant = (jogada.linha_fim, jogada.coluna_fim)

            if jogada.peça_jogada[0] == "P" and abs(jogada.linha_ini - jogada.linha_fim) == 2:
                self.enpassant = ()

            #Roque_pequeno
            self.roque_pequeno_log.pop()
            novo_roque = self.roque_pequeno_log[-1]
            self.roque_pequeno = Roque_Pequeno_Atual(novo_roque.rbs,novo_roque.rps,novo_roque.dbs,novo_roque.dps)

            #Roque_grande
            if jogada.roque_jogada:
                if jogada.coluna_fim - jogada.coluna_ini == 2:
                    self.tabuleiro[jogada.linha_fim][jogada.coluna_fim+1] = self.tabuleiro[jogada.linha_fim][jogada.coluna_fim -1]
                    self.tabuleiro[jogada.linha_fim][jogada.coluna_fim-1] = "--"
                else:
                    self.tabuleiro[jogada.linha_fim][jogada.coluna_fim-2] = self.tabuleiro[jogada.linha_fim][jogada.coluna_fim +1]
                    self.tabuleiro[jogada.linha_fim][jogada.coluna_fim+1] = "--"
                    
            self.checkmate = False
            self.afogamento = False

    def update_roque_pequeno(self, jogada):
        if jogada.peça_jogada == 'Rb':
            self.roque_pequeno.rbs = False
            self.roque_pequeno.dbs = False
        elif jogada.peça_jogada == 'Rp':
            self.roque_pequeno.rps = False
            self.roque_pequeno.dps = False

        elif jogada.peça_jogada == 'Tb':
            if jogada.linha_ini == 7:
                if jogada.coluna_ini == 0:
                    self.roque_pequeno.dbs = False
                elif jogada.coluna_ini == 7:
                    self.roque_pequeno.rbs = False
        elif jogada.peça_jogada == 'Tp':
            if jogada.linha_ini == 0:
                if jogada.coluna_ini == 0:
                    self.roque_pequeno.dps = False
                elif jogada.coluna_ini == 7:
                    self.roque_pequeno.rps = False            



    '''
    Validação se as jogadas -> Considerando checks
    '''
    def valida_todas_jogadas(self):
        temp_enpassant = self.enpassant
        temp_roque_pequeno = Roque_Pequeno_Atual(self.roque_pequeno.rbs, self.roque_pequeno.rps,
                                                 self.roque_pequeno.dbs, self.roque_pequeno.dps)
        
        jogadas_possiveis = self.todas_as_jogadas_possiveis()

        for i in range(len(jogadas_possiveis)-1, -1, -1):
            self.cria_jogada(jogadas_possiveis[i])
            self.branco_joga = not self.branco_joga
            if self.Check():
                jogadas_possiveis.remove(jogadas_possiveis[i])
            self.branco_joga = not self.branco_joga
            self.refaz_jogada()

        if len(jogadas_possiveis) == 0:
            if self.Check():
                self.checkmate = True
            else:
                self.afogamento = True
        
        if self.branco_joga:
            self.jogada_roque(self.posicao_rei_branco[0], self.posicao_rei_branco[1], jogadas_possiveis)
        else:
            self.jogada_roque(self.posicao_rei_preto[0], self.posicao_rei_preto[1], jogadas_possiveis)    


        self.enpassant = temp_enpassant
        self.roque_pequeno = temp_roque_pequeno


        return jogadas_possiveis

    '''
    Verifica se o jogador está em check
    '''
    def Check(self):
        if self.branco_joga:
            return self.casa_sobre_ataque(self.posicao_rei_branco[0], self.posicao_rei_branco[1])
        else:
            return self.casa_sobre_ataque(self.posicao_rei_preto[0], self.posicao_rei_preto[1])

    '''
    Verifica se o inimigo pode atacar a casa(l,c)
    '''
    def casa_sobre_ataque(self, l, c):    
        self.branco_joga = not self.branco_joga
        adv_jogadas = self.todas_as_jogadas_possiveis()
        self.branco_joga = not self.branco_joga
        for jogada in adv_jogadas:
            if jogada.linha_fim == l and jogada.coluna_fim == c:
                return True
        return False    
    
    '''
    Validação de jogadas -> Sem considerar checks
    '''
    def todas_as_jogadas_possiveis(self):
        jogadas = []
        for l in range(len(self.tabuleiro)):      #Número de linhas
            for c in range(len(self.tabuleiro[l])): #Número de colunas naquela linha
                cor_jogador = self.tabuleiro[l][c][1]
                if (cor_jogador == 'b' and self.branco_joga) or (cor_jogador == 'p' and not self.branco_joga):
                    peça = self.tabuleiro[l][c][0]
                    self.jogadaFuncoes[peça](l,c, jogadas)
        return jogadas
    
    '''
    Retorna todas as jogadas para os peões.
    '''
    def jogada_peao(self, l, c, jogadas):
        if self.branco_joga:
            if self.tabuleiro[l-1][c] == "--":
                jogadas.append(Jogadas((l,c), (l-1,c), self.tabuleiro))
                if l == 6 and self.tabuleiro[l-2][c] == "--":
                    jogadas.append(Jogadas((l,c), (l-2,c), self.tabuleiro))
            if c-1 >= 0:                              #Verifica captura para a diagonal esquerda
                if self.tabuleiro[l-1][c-1][1] == "p": #Verifica se existe uma peça a ser capturada        
                    jogadas.append(Jogadas((l,c), (l-1,c-1), self.tabuleiro))
                elif (l-1, c-1 ) == self.enpassant:
                    jogadas.append(Jogadas((l,c), (l-1,c-1), self.tabuleiro, enpassant_jogada=True))
            if c+1 <= 7:                              #Verifica captura para a diagonal direita
                if self.tabuleiro[l-1][c+1][1] == "p": #Verifica se existe uma peça a ser capturada        
                    jogadas.append(Jogadas((l,c), (l-1,c+1), self.tabuleiro))       
                elif (l-1, c+1 ) == self.enpassant:
                    jogadas.append(Jogadas((l,c), (l-1,c+1), self.tabuleiro, enpassant_jogada=True))    
        
        else: #Peão preto
            if self.tabuleiro[l+1][c] == "--":
                jogadas.append(Jogadas((l,c), (l+1,c), self.tabuleiro))
                if l == 1 and self.tabuleiro[l+2][c] == "--":
                    jogadas.append(Jogadas((l,c), (l+2,c), self.tabuleiro))

            #Capturas        
            if c-1 >= 0:                              #Verifica captura para a diagonal esquerda
                if self.tabuleiro[l+1][c-1][1] == "b": #Verifica se existe uma peça a ser capturada        
                    jogadas.append(Jogadas((l,c), (l+1,c-1), self.tabuleiro))
                elif (l+1, c-1 ) == self.enpassant:
                    jogadas.append(Jogadas((l,c), (l+1,c-1), self.tabuleiro, enpassant_jogada=True))    

            if c+1 <= 7:                              #Verifica captura para a diagonal direita
                if self.tabuleiro[l+1][c+1][1] == "b": #Verifica se existe uma peça a ser capturada        
                    jogadas.append(Jogadas((l,c), (l+1,c+1), self.tabuleiro)) 
                elif (l+1, c+1 ) == self.enpassant:
                    jogadas.append(Jogadas((l,c), (l+1,c+1), self.tabuleiro, enpassant_jogada=True))


    ''' 
    Retorna todas as jogadas para as torres.
    ''' 
    def jogada_torre(self, l, c, jogadas):
        direção = ((-1,0), (0,-1), (1,0), (0,1)) #cima, esquerda, baixo, direita
        cor_adversário = "p" if self.branco_joga else "b"
        for d in direção:
            for i in range(1,8):
                linha_fim = l + d[0] * i
                coluna_fim = c + d[1] * i
                if 0 <= linha_fim < 8 and 0 <= coluna_fim < 8:
                    peça_fim = self.tabuleiro[linha_fim][coluna_fim]
                    if peça_fim == "--":
                        jogadas.append(Jogadas((l,c), (linha_fim, coluna_fim), self.tabuleiro))
                    elif peça_fim[1] == cor_adversário:
                        jogadas.append(Jogadas((l,c), (linha_fim, coluna_fim), self.tabuleiro))
                        break
                    else:
                        break
                else:
                    break    
    
    ''' 
    Retorna todas as jogadas para os cavalos.
    '''

    def jogada_cavalo(self, l, c, jogadas):
        direção = ((-2,-1), (-2,1), (-1,-2) ,(-1,2), (1,-2), (1,2) ,(2,-1), (2,1))
        cor_aliada = "b" if self.branco_joga else "p"
        for d in direção:
                linha_fim =  l + d[0] 
                coluna_fim = c + d[1]
                if 0 <= linha_fim < 8 and 0 <= coluna_fim < 8:
                    peça_fim = self.tabuleiro[linha_fim][coluna_fim]
                    if peça_fim[1] != cor_aliada:
                        jogadas.append(Jogadas((l,c), (linha_fim, coluna_fim), self.tabuleiro))

    ''' 
    Retorna todas as jogadas para os bispos.
    '''
    def jogada_bispo(self, l, c, jogadas):
        direção = ((-1,-1), (-1,1), (1,-1), (1,1)) #d.e esquerda, d.d direita, d.e esquerda, d.e direita
        cor_adversário = "p" if self.branco_joga else "b"
        for d in direção:
            for i in range(1,8):
                linha_fim = l + d[0] * i
                coluna_fim = c + d[1] * i
                if 0 <= linha_fim < 8 and 0 <= coluna_fim < 8:
                    peça_fim = self.tabuleiro[linha_fim][coluna_fim]
                    if peça_fim == "--":
                        jogadas.append(Jogadas((l,c), (linha_fim, coluna_fim), self.tabuleiro))
                    elif peça_fim[1] == cor_adversário:
                        jogadas.append(Jogadas((l,c), (linha_fim, coluna_fim), self.tabuleiro))
                        break
                    else:
                        break
                else:
                    break  
    
    ''' 
    Retorna todas as jogadas para as damas.
    '''
    def jogada_dama(self, l, c, jogadas):
        self.jogada_torre(l,c, jogadas)
        self.jogada_bispo(l,c, jogadas)
    

    ''' 
    Retorna todas as jogadas para os reis.
    '''
    def jogada_rei(self, l, c, jogadas):
        direção = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1, 0) ,(1,1)) 
        cor_aliada = "b" if self.branco_joga else "p"
        for i in range(8):
                linha_fim = l +  direção[i][0] 
                coluna_fim = c + direção[i][1]
                if 0 <= linha_fim < 8 and 0 <= coluna_fim < 8:
                    peça_fim = self.tabuleiro[linha_fim][coluna_fim]
                    if peça_fim[1] != cor_aliada:
                        jogadas.append(Jogadas((l,c), (linha_fim, coluna_fim), self.tabuleiro))

    '''
    Retorna todas as possibilidades de roque
    '''
    def jogada_roque(self, l, c, jogadas):
        if self.casa_sobre_ataque(l,c):
            return
        if (self.branco_joga and self.roque_pequeno.rbs) or (not self.branco_joga and self.roque_pequeno.rps):
            self.jogada_roque_pequeno(l, c, jogadas)
        if (self.branco_joga and self.roque_pequeno.dbs) or (not self.branco_joga and self.roque_pequeno.dps):
            self.jogada_roque_grande(l, c, jogadas)    

    def jogada_roque_pequeno(self,l,c,jogadas):
        if self.tabuleiro[l][c+1] == '--' and self.tabuleiro[l][c+2] == '--':
            if not self.casa_sobre_ataque(l, c+1) and not self.casa_sobre_ataque(l, c+2):
                jogadas.append(Jogadas((l, c), (l,c+2), self.tabuleiro, roque_jogada=True))

    def jogada_roque_grande(self,l,c,jogadas):             
        if self.tabuleiro[l][c-1] == '--' and self.tabuleiro[l][c-2] == "--" and self.tabuleiro[l][c-3]:
            if not self.casa_sobre_ataque(l, c-1) and not self.casa_sobre_ataque(l, c-2):
                jogadas.append(Jogadas((l, c), (l,c-2), self.tabuleiro, roque_jogada=True))


class Roque_Pequeno_Atual():
    def __init__(self, rbs, rps, dbs, dps):
        self.rbs = rbs
        self.rps = rps
        self.dbs = dbs
        self.dps = dps



'''
Irá fazer o rastreio dos clicks do jogadores para verificar a movimentação das peças.
'''
class Jogadas():
        #Mapeando as posições por linha coluna de a1 a h8.
    fileiras_linhas = {"1": 7, "2": 6, "3": 5, "4": 4,
                       "5": 3, "6": 2, "7": 1, "8": 0}
    linhas_fileiras = {v: k for k, v in fileiras_linhas.items()}
    fileiras_colunas = {"a": 0, "b": 1, "c": 2, "d": 3, 
                        "e": 4, "f": 5, "g": 6, "h": 7}                     
    colunas_fileras = {v: k for k, v in fileiras_colunas.items()}
    
    def __init__(self, casa_ini, casa_fim, tabuleiro, enpassant_jogada=False, roque_jogada=False):
        self.linha_ini  = casa_ini[0]
        self.coluna_ini = casa_ini[1]
        self.linha_fim  = casa_fim[0]
        self.coluna_fim = casa_fim[1]
        self.peça_jogada = tabuleiro[self.linha_ini][self.coluna_ini]
        self.peça_capturada = tabuleiro[self.linha_fim][self.coluna_fim]

        #Promoção de Peões
        self.promocao_peao = (self.peça_jogada == 'Pb' and self.linha_fim == 0) or (self.peça_jogada == 'Pp' and self.linha_fim == 7)
        
        #En Passant
        self.enpassant_jogada = enpassant_jogada   
        if self.enpassant_jogada:
            self.peça_capturada = 'Pb' if self.peça_jogada == 'Pp' else 'Pp'
        
        #Roque
        self.roque_jogada = roque_jogada

        self.jogada_ID = self.linha_ini * 1000 + self.coluna_ini * 100 + self.linha_fim * 10 + self.coluna_fim

    '''
    Sobreescreve métodos iguais
    '''
    def __eq__(self, other):
        if isinstance(other, Jogadas):
            return self.jogada_ID == other.jogada_ID
        return False 
            

    '''
    Cria a notação algébrica para o Xadrez.
    '''
    def notacao_algebrica(self):
        return self.getRankFile(self.linha_ini, self.coluna_ini) + self.getRankFile(self.linha_fim, self.coluna_fim)

    def getRankFile(self, l, c):
        return  self.colunas_fileras[c] + self.linhas_fileiras[l]     
