import random

valor_peças = {'R': 0, 'D': 10, 'T': 5, 'B': 3, 'C':3, 'P': 1}
checkmate = 1000
afogamento = 0
profundidade = 2

'''
'''
def jogada_random(valida_jogadas):
    return valida_jogadas[random.randint(0, len(valida_jogadas)-1)]


def encontra_melhor_jogada(estado_do_jogo, valida_jogadas):
    pass


def encontra_melhor_jogada_min_max(estado_do_jogo, valida_jogadas):
    global proxima_jogada
    proxima_jogada = None
    encontra_jogada_min_max(estado_do_jogo, valida_jogadas, profundidade, estado_do_jogo.branco_joga)
    return proxima_jogada

def encontra_jogada_min_max(estado_do_jogo, valida_jogadas, profundidade, branco_joga):
    global proxima_jogada
    if profundidade == 0:
        return valor_material(estado_do_jogo.tabuleiro)
    
    if branco_joga:
        maxScore = -checkmate
        for jogada in valida_jogadas:
            estado_do_jogo.cria_jogada(jogada)
            proxima_jogada = estado_do_jogo.valida_todas_jogadas()
            score = encontra_jogada_min_max(estado_do_jogo, proxima_jogada, profundidade-1, False)
            if score > maxScore:
                maxScore = score
                if profundidade == profundidade:
                    proxima_jogada = jogada
            estado_do_jogo.refaz_jogada()
        return maxScore

    else:
        minScore = checkmate
        for jogada in valida_jogadas:
            estado_do_jogo.cria_jogada(jogada)
            proxima_jogada = estado_do_jogo.valida_todas_jogadas()
            score = encontra_jogada_min_max(estado_do_jogo, proxima_jogada, profundidade -1, True)
            if score < minScore:
                minScore = score
                if profundidade == profundidade:
                    proxima_jogada = jogada
                estado_do_jogo.refaz_jogada()
            return minScore



def valor_tabuleiro(estado_do_jogo):
    if estado_do_jogo.checkmate:
        if estado_do_jogo.branco_joga:
            return -checkmate
        else:
            return checkmate
    elif estado_do_jogo.afogamento:
        return afogamento

    score = 0
    for linha in estado_do_jogo.tabuleiro:
        for casa in linha:
            if casa[1] == 'b':
                score += valor_peças[casa[0]]
            elif casa[1] == 'p':
                score -= valor_peças[casa[0]]
    
    return score







'''
'''
def valor_material(tabuleiro):
    score = 0
    for linha in tabuleiro:
        for casa in linha:
            if casa[1] == 'b':
                score += valor_peças[casa[0]]
            elif casa[1] == 'p':
                score -= valor_peças[casa[0]]
    
    return score