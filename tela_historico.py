import pygame
class TelaHistorico:
    def __init__(self, largura, altura, som_clique, fonte=None,fonte_pequena = None):
        self.som_clique = som_clique
        self.largura = largura
        self.altura = altura
        self.scroll_y = 0
        self.historico = []
        self.fonte = fonte or pygame.font.SysFont(None, 28)
        self.fonte_pequena = fonte_pequena or pygame.font.SysFont(None, 20)
        self.espaco_linha = 40
        self.arrastando = False
        self.mouse_y_inicial = 0
        self.scroll_inicial = 0
        self.barra_scroll_rect = None

    def desenhar(self, tela):
        tela.fill((30, 30, 30))  # Fundo

        y = 50 - self.scroll_y

        for partida in self.historico:
            jogador_x, jogador_o, vencedor, data = partida
            # Determine the winner's name

        for partida in self.historico:
            jogador_x, jogador_o, vencedor, data = partida
            texto = f"{jogador_x} vs {jogador_o} | Vencedor: {vencedor} | {data.strftime('%d/%m/%Y %H:%M')}"
            render = self.fonte.render(texto, True, (255, 255, 255))
            tela.blit(render, (50, y))
            y += self.espaco_linha

        mouse_pos = pygame.mouse.get_pos()
        hover_voltar = (self.largura - 180 <= mouse_pos[0] <= self.largura - 180 + 130 and self.altura - 50 <= mouse_pos[1] <= self.altura - 50 + 30)

    # Desenha tooltip se hover
        if hover_voltar:
            texto_tooltip = "Voltar ao menu principal"
            tooltip = self.fonte.render(texto_tooltip, True, (0, 0, 0))
            
            # Calcula posição (evita sair da tela)
            tooltip_x = min(self.largura - 180, self.largura - tooltip.get_width() - 10)
            tooltip_y = self.altura - 80
            
            # Fundo do tooltip com borda
            pygame.draw.rect(tela, (255, 255, 200), 
                            (tooltip_x - 5, tooltip_y, 
                            tooltip.get_width() + 10, 25))
            pygame.draw.rect(tela, (200, 200, 150), 
                            (tooltip_x - 5, tooltip_y, 
                            tooltip.get_width() + 10, 25), 1)  # Borda
            
            # Texto do tooltip
            tela.blit(tooltip, (tooltip_x, tooltip_y + 5))

        # Desenha botão de voltar com efeito hover
        cor_botao = (220, 80, 80) if hover_voltar else (200, 50, 50)
        pygame.draw.rect(tela, cor_botao, (self.largura - 180, self.altura - 50, 130, 30), border_radius=5)
        voltar = self.fonte.render("Voltar (Esc)", True, (255, 255, 255))
        tela.blit(voltar, (self.largura - 180 + (130 - voltar.get_width()) // 2, self.altura - 45))
            

        if len(self.historico) * self.espaco_linha > self.altura - 100:
            altura_total = len(self.historico) * self.espaco_linha
            proporcao = (self.altura - 100) / altura_total
            altura_barra = max(20, (self.altura - 100) * proporcao)  # Altura mínima da barra
            posicao_barra = (self.scroll_y / altura_total) * (self.altura - 100)
            
            # Área da barra de scroll
            pygame.draw.rect(tela, (100, 100, 100), (self.largura - 20, 50, 10, self.altura - 100))
            self.barra_scroll_rect = pygame.Rect(self.largura - 20, 50 + posicao_barra, 10, altura_barra)
            pygame.draw.rect(tela, (150, 150, 150), self.barra_scroll_rect)

    def lidar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                return "sair"
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    if self.som_clique:
                        self.som_clique.play()
                    return "menu"
                elif evento.key == pygame.K_DOWN:
                    self.scroll_y += 20
                elif evento.key == pygame.K_UP:
                    self.scroll_y = max(0, self.scroll_y - 20)
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Botão esquerdo
                    # Verifica se clicou na barra de scroll
                    if (self.barra_scroll_rect and 
                        self.barra_scroll_rect.collidepoint(evento.pos)):
                        self.arrastando = True
                        self.mouse_y_inicial = evento.pos[1]
                        self.scroll_inicial = self.scroll_y
                    else:
                        # Verifica se clique foi no botão "Voltar"
                        if (self.largura - 180 <= evento.pos[0] <= self.largura - 180 + 130 and
                            self.altura - 50 <= evento.pos[1] <= self.altura - 50 + 30):
                            if self.som_clique:
                                self.som_clique.play()
                            return "menu"
                        # Clique fora da barra de scroll e botão voltar
                        self.arrastando = False
            elif evento.type == pygame.MOUSEWHEEL:
                # Scroll com roda do mouse
                self.scroll_y -= evento.y * 20  # evento.y é 1 (up) ou -1 (down)
                self.scroll_y = max(0, self.scroll_y)  # Impede scroll negativo

            elif evento.type == pygame.MOUSEMOTION:
                if self.arrastando:
                    delta_y = evento.pos[1] - self.mouse_y_inicial
                    self.scroll_y = self.scroll_inicial - delta_y
                    self.scroll_y = max(0, self.scroll_y)
        return None

    # No arquivo tela_historico.py, adicione no final da classe:

    def atualizar_historico(self, novo_historico):
        self.historico = novo_historico
        self.scroll_y = 0  # Resetar scroll ao atualizar