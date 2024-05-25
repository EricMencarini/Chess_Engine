# '''
# Greedy
# '''
# def encontra_melhor_jogada_guloso(estado_do_jogo, valida_jogadas):
#     turnMultiplier = 1 if estado_do_jogo.branco_joga else -1
#     oponente_min_max_score = checkmate
#     melhor_jogada = None
#     random.shuffle(valida_jogadas)

#     for jogada_jogador in valida_jogadas:
#         estado_do_jogo.cria_jogada(jogada_jogador)
#         jogada_oponente = estado_do_jogo.valida_todas_jogadas()
        
#         if estado_do_jogo.afogamento:
#             oponente_max_score = afogamento
#         elif estado_do_jogo.checkmate:
#             oponente_max_score = -checkmate
#         else:
#             oponente_max_score = -checkmate

#             for jogada in jogada_oponente:
#                 estado_do_jogo.cria_jogada(jogada_oponente)
#                 estado_do_jogo.valida_todas_jogadas()
#                 if estado_do_jogo.checkmate:
#                     score = checkmate
#                 elif estado_do_jogo.afogamento:
#                     score = afogamento
#                 else: 
#                     score = -turnMultiplier * valor_material(estado_do_jogo.tabuleiro)
#                 if score > oponente_max_score:
#                     oponente_max_score = score
#                 estado_do_jogo.refaz_jogada()
       
#         if  oponente_max_score < oponente_min_max_score:
#             oponente_min_max_score = oponente_max_score
#             melhor_jogada = jogada_jogador

#         estado_do_jogo.refaz_jogada()    

#     return melhor_jogada