import pygame
import pygame.mixer
from jogo_da_velha_logica import JogoDaVelha_Logica
import tela_historico
from pathlib import Path
CAMINHO = Path(__file__).parent.resolve()
# Adicione o caminho do diretório atual ao sys.path


class JogoDaVelhaComBanco(JogoDaVelha_Logica):
    def __init__(self, banco):
        super().__init__()
        self.banco = banco
        self.tela = None
        self.largura = 500
        self.altura = 600
        self.fonte_grande = None
        self.fonte_media = None
        self.fonte_pequena = None
        self.executando = True
        self.jogador1 = ""
        self.jogador2 = ""
        self.texto_jogador1 = ""
        self.texto_jogador2 = ""
        self.entrada_ativa = None
        self.mostrar_historico = False 
        self.tela_historico = None

    def inicializar_pygame(self):
        pygame.init()

        pygame.mixer.init()

        # Música de fundo
        pygame.mixer.music.load(f"{CAMINHO}/sounds/musica_fundo.mp3")
        pygame.mixer.music.set_volume(0.3)  # Volume entre 0.0 e 1.0
        pygame.mixer.music.play(-1)  # -1 = loop infinito

        # Sons
        self.som_clique = pygame.mixer.Sound(f"{CAMINHO}/sounds/clique.wav")
        self.som_vitoria = pygame.mixer.Sound(f"{CAMINHO}/sounds/vitoria.wav")
        self.som_empate = pygame.mixer.Sound(f"{CAMINHO}/sounds/empate.wav")

        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Jogo da Velha")
        self.fonte_grande = pygame.font.Font(None, 60)
        self.fonte_media = pygame.font.Font(None, 36)
        self.fonte_pequena = pygame.font.Font(None, 24)

        self.tela_historico = tela_historico.TelaHistorico(self.largura, self.altura, self.som_clique, self.fonte_pequena)

    def tela_inicial(self):
        clock = pygame.time.Clock()
        while True:
            mouse_clicado = False
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_clicado = True
                    mouse_pos = event.pos
                if event.type == pygame.KEYDOWN:
                    if self.entrada_ativa == "jogador1":
                        if event.key == pygame.K_BACKSPACE:
                            self.texto_jogador1 = self.texto_jogador1[:-1]
                        elif len(self.texto_jogador1) < 15 and event.unicode.isprintable():
                            self.texto_jogador1 += event.unicode
                    elif self.entrada_ativa == "jogador2":
                        if event.key == pygame.K_BACKSPACE:
                            self.texto_jogador2 = self.texto_jogador2[:-1]
                        elif len(self.texto_jogador2) < 15 and event.unicode.isprintable():
                            self.texto_jogador2 += event.unicode
                    elif event.key == pygame.K_h:  # Tecla H para abrir histórico
                        self.som_clique.play()
                        self.mostrar_tela_historico()


            self.tela.fill((240, 240, 240))
            titulo = self.fonte_grande.render("Jogo da Velha", True, (0, 0, 0))
            self.tela.blit(titulo, (self.largura // 2 - titulo.get_width() // 2, 50))

            caixa1 = pygame.Rect(self.largura // 2 - 100, 150, 200, 40)
            caixa2 = pygame.Rect(self.largura // 2 - 100, 230, 200, 40)
            pygame.draw.rect(self.tela, (255, 255, 255), caixa1)
            pygame.draw.rect(self.tela, (255, 255, 255), caixa2)
            pygame.draw.rect(self.tela, (0, 0, 0), caixa1, 2)
            pygame.draw.rect(self.tela, (0, 0, 0), caixa2, 2)

            txt1 = self.fonte_media.render(self.texto_jogador1 or "Jogador 1 (X)", True, (100, 100, 100) if self.entrada_ativa != "jogador1" else (0, 0, 0))
            txt2 = self.fonte_media.render(self.texto_jogador2 or "Jogador 2 (O)", True, (100, 100, 100) if self.entrada_ativa != "jogador2" else (0, 0, 0))
            self.tela.blit(txt1, (caixa1.x + 5, caixa1.y + 8))
            self.tela.blit(txt2, (caixa2.x + 5, caixa2.y + 8))

            btn_iniciar = pygame.Rect(self.largura // 2 - 75, 310, 150, 50)
            cor_iniciar = (0, 150, 0) if self.texto_jogador1.strip() and self.texto_jogador2.strip() else (150, 150, 150)
            pygame.draw.rect(self.tela, cor_iniciar, btn_iniciar, border_radius=5)
            txt_btn = self.fonte_media.render("Jogar", True, (255, 255, 255))
            self.tela.blit(txt_btn, (btn_iniciar.x + (btn_iniciar.width - txt_btn.get_width()) // 2, btn_iniciar.y + 10))

            if btn_iniciar.collidepoint(mouse_pos):
                texto_tooltip = "Iniciar jogo"
                tooltip = self.fonte_pequena.render(texto_tooltip, True, (0, 0, 0))
                
                # Calcula posição (centralizado acima do botão)
                tooltip_x = btn_iniciar.centerx - tooltip.get_width() // 2
                tooltip_y = btn_iniciar.y - 30
                
                # Ajusta para não sair da tela
                tooltip_x = max(10, min(tooltip_x, self.largura - tooltip.get_width() - 10))
                
                # Fundo do tooltip com borda (mesmo estilo do botão Voltar)
                pygame.draw.rect(self.tela, (255, 255, 200), 
                            (tooltip_x - 5, tooltip_y, 
                                tooltip.get_width() + 10, 25))
                pygame.draw.rect(self.tela, (200, 200, 150), 
                            (tooltip_x - 5, tooltip_y, 
                                tooltip.get_width() + 10, 25), 1)
                # Texto do tooltip
                self.tela.blit(tooltip, (tooltip_x, tooltip_y + 5))

            btn_historico = pygame.Rect(self.largura // 2 - 75, 380, 150, 40)
            hover_historico = btn_historico.collidepoint(mouse_pos)
            cor_historico = (90, 90, 220) if hover_historico else (70, 70, 200)
            pygame.draw.rect(self.tela, cor_historico, btn_historico, border_radius=5)
            txt_historico = self.fonte_pequena.render("Histórico (H)", True, (255, 255, 255))
            self.tela.blit(txt_historico, (btn_historico.x + (btn_historico.width - txt_historico.get_width()) // 2, btn_historico.y + 10))

            if hover_historico:
                texto_tooltip = "Ver histórico de partidas"
                tooltip = self.fonte_pequena.render(texto_tooltip, True, (0, 0, 0))
                
                # Calcula posição (centralizado acima do botão)
                tooltip_x = btn_historico.centerx - tooltip.get_width() // 2
                tooltip_y = btn_historico.y - 30
                
                # Ajusta para não sair da tela
                tooltip_x = max(10, min(tooltip_x, self.largura - tooltip.get_width() - 10))
                
                # Fundo do tooltip com borda (mesmo estilo do botão Voltar)
                pygame.draw.rect(self.tela, (255, 255, 200), 
                            (tooltip_x - 5, tooltip_y, 
                                tooltip.get_width() + 10, 25))
                pygame.draw.rect(self.tela, (200, 200, 150), 
                            (tooltip_x - 5, tooltip_y, 
                                tooltip.get_width() + 10, 25), 1)  # Borda
                
                # Texto do tooltip
                self.tela.blit(tooltip, (tooltip_x, tooltip_y + 5))

            # desenhar botão de apagar historico ao lado do botão de histórico
            btn_apagar_historico = pygame.Rect(self.largura // 2 + 85, 380, 150, 40)
            hover_apagar_historico = btn_apagar_historico.collidepoint(mouse_pos)
            cor_apagar_historico = (200, 50, 50) if hover_apagar_historico else (150, 30, 30)
            pygame.draw.rect(self.tela, cor_apagar_historico, btn_apagar_historico, border_radius=5)
            txt_apagar_historico = self.fonte_pequena.render("Apagar histórico", True, (255, 255, 255))
            self.tela.blit(txt_apagar_historico, (btn_apagar_historico.x + (btn_apagar_historico.width - txt_apagar_historico.get_width()) // 2, btn_apagar_historico.y + 10))
            if hover_apagar_historico:
                texto_tooltip = "Apagar histórico de partidas"
                tooltip = self.fonte_pequena.render(texto_tooltip, True, (0, 0, 0))
                
                # Calcula posição (centralizado acima do botão)
                tooltip_x = btn_apagar_historico.centerx - tooltip.get_width() // 2
                tooltip_y = btn_apagar_historico.y - 30
                
                # Ajusta para não sair da tela
                tooltip_x = max(10, min(tooltip_x, self.largura - tooltip.get_width() - 10))
                
                # Fundo do tooltip com borda (mesmo estilo do botão Voltar)
                pygame.draw.rect(self.tela, (255, 255, 200), 
                            (tooltip_x - 5, tooltip_y, 
                                tooltip.get_width() + 10, 25))
                pygame.draw.rect(self.tela, (200, 200, 150), 
                            (tooltip_x - 5, tooltip_y, 
                                tooltip.get_width() + 10, 25), 1)
                # Texto do tooltip
                self.tela.blit(tooltip, (tooltip_x, tooltip_y + 5))
            if hover_apagar_historico and mouse_clicado:
                self.som_clique.play()
                self.banco.apagar_historico()
                self.tela_historico.atualizar_historico([])
                # Atualizar o histórico antes de mostrar
                historico = self.banco.buscar_historico()
                self.tela_historico.atualizar_historico(historico)
                self.mostrar_tela_historico()
                # Atualizar o histórico antes de mostrar

            # Desenhar botão de sair
            btn_sair = pygame.Rect(self.largura // 2 - 75, 450, 150, 40)
            pygame.draw.rect(self.tela, (200, 50, 50), btn_sair, border_radius=5)
            txt_sair = self.fonte_pequena.render("Sair", True, (255, 255, 255))
            self.tela.blit(txt_sair, (btn_sair.x + (btn_sair.width - txt_sair.get_width()) // 2, btn_sair.y + 10))
            if btn_sair.collidepoint(mouse_pos):
                texto_tooltip = "Sair do jogo"
                tooltip = self.fonte_pequena.render(texto_tooltip, True, (0, 0, 0))
                # Desenha tooltip se hover
                
                # Calcula posição (centralizado acima do botão)
                tooltip_x = btn_sair.centerx - tooltip.get_width() // 2
                tooltip_y = btn_sair.y - 30
                
                # Ajusta para não sair da tela
                tooltip_x = max(10, min(tooltip_x, self.largura - tooltip.get_width() - 10))
                
                # Fundo do tooltip com borda (mesmo estilo do botão Voltar)
                pygame.draw.rect(self.tela, (255, 255, 200), 
                            (tooltip_x - 5, tooltip_y, 
                                tooltip.get_width() + 10, 25))
                pygame.draw.rect(self.tela, (200, 200, 150), 
                            (tooltip_x - 5, tooltip_y, 
                                tooltip.get_width() + 10, 25), 1)
                # Blit the tooltip text
                self.tela.blit(tooltip, (tooltip_x, tooltip_y + 5))


            pygame.display.flip()
            clock.tick(30)

            if mouse_clicado:
                if caixa1.collidepoint(mouse_pos) or caixa2.collidepoint(mouse_pos):
                    if caixa1.collidepoint(mouse_pos):
                        self.entrada_ativa = "jogador1"
                    else:
                        self.entrada_ativa = "jogador2"
                else:
                    self.entrada_ativa = None
                if btn_iniciar.collidepoint(mouse_pos) and self.texto_jogador1.strip() and self.texto_jogador2.strip():
                    self.jogador1 = self.texto_jogador1.strip()
                    self.jogador2 = self.texto_jogador2.strip()
                    return True
                elif btn_historico.collidepoint(mouse_pos):
                    self.som_clique.play()
                    self.mostrar_tela_historico()
                    # Atualizar o histórico antes de mostrar
                    historico = self.banco.buscar_historico()
                    self.tela_historico.atualizar_historico(historico)
                elif btn_sair.collidepoint(mouse_pos):
                    self.som_clique.play()
                    raise SystemExit("Saindo do jogo...")
                    

    def desenhar_tabuleiro(self):
        self.tela.fill((240, 240, 240))
        tamanho = 300
        margem_x = self.largura // 2 - tamanho // 2
        margem_y = 150

        for i in range(1, 3):
            pygame.draw.line(self.tela, (0, 0, 0), (margem_x + i * 100, margem_y), (margem_x + i * 100, margem_y + tamanho), 3)
            pygame.draw.line(self.tela, (0, 0, 0), (margem_x, margem_y + i * 100), (margem_x + tamanho, margem_y + i * 100), 3)

        for i, val in enumerate(self.tabuleiro):
            if val:
                x = margem_x + (i % 3) * 100 + 50
                y = margem_y + (i // 3) * 100 + 50
                cor = (255, 0, 0) if val == 'X' else (0, 0, 255)
                texto = self.fonte_grande.render(val, True, cor)
                ret = texto.get_rect(center=(x, y))
                self.tela.blit(texto, ret)

        texto = self.fonte_media.render(f"Vez de: {self.jogador1 if self.jogador_atual == 'X' else self.jogador2}", True, (0, 0, 0))
        self.tela.blit(texto, (20, self.altura - 40))

        pygame.display.flip()

    def tratar_clique_tabuleiro(self, pos):
        tamanho = 300
        margem_x = self.largura // 2 - tamanho // 2
        margem_y = 150
        if margem_x <= pos[0] <= margem_x + tamanho and margem_y <= pos[1] <= margem_y + tamanho:
            col = (pos[0] - margem_x) // 100
            lin = (pos[1] - margem_y) // 100
            idx = lin * 3 + col
            self.som_clique.play()
            if self.fazer_jogada(idx):
                vencedor = self.verificar_vencedor()
                if vencedor:
                    self.finalizar_jogo(vencedor)
                else:
                    self.alternar_jogador()

    def finalizar_jogo(self, vencedor):
        if vencedor == 'Empate':
            msg = "Deu empate!"
            self.som_empate.play()
            vencedor_db = 'EMPATE'
        else:
            vencedor_db = vencedor
            nome = self.jogador1 if vencedor == 'X' else self.jogador2
            msg = f"{nome} venceu!"
            self.som_vitoria.play()
        try:
            self.banco.salvar_resultado(self.jogador1, self.jogador2, vencedor_db)

            vencedor_nome = 'EMPATE' if vencedor_db == 'EMPATE' else nome
            self.banco.salvar_partida_no_historico(self.jogador1, self.jogador2, vencedor_nome, self.tabuleiro)
        except Exception as e:
            print(f"Erro ao salvar resultado: {e}")
        self.mostrar_resultado(msg)
        self.tela_historico.atualizar_historico(self.banco.buscar_historico())

    def mostrar_resultado(self, mensagem):
        rodando = True
        while rodando:
            self.tela.fill((255, 255, 255))
            texto = self.fonte_grande.render(mensagem, True, (0, 0, 0))
            rect_texto = texto.get_rect(center=(self.largura // 2, self.altura // 2 - 50))
            self.tela.blit(texto, rect_texto)

            botao_continuar = pygame.Rect(self.largura // 2 - 160, self.altura // 2 + 30, 140, 50)
            texto_sair_menu = self.fonte_media.render("Voltar ao menu", True, (255, 255, 255))
            largura_botao_sair = texto_sair_menu.get_width() + 40
            botao_voltar_menu = pygame.Rect(self.largura // 2 + 20, self.altura // 2 + 30, largura_botao_sair, 50)

            pygame.draw.rect(self.tela, (0, 128, 0), botao_continuar)
            pygame.draw.rect(self.tela, (200, 0, 0), botao_voltar_menu)

            texto_continuar = self.fonte_media.render("Continuar", True, (255, 255, 255))
            texto_sair_menu = self.fonte_media.render("Voltar ao menu", True, (255, 255, 255))

            self.tela.blit(texto_continuar, texto_continuar.get_rect(center=botao_continuar.center))
            self.tela.blit(texto_sair_menu, texto_sair_menu.get_rect(center=botao_voltar_menu.center))

            pygame.display.flip()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    rodando = False
                    self.executando = False
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if botao_continuar.collidepoint(e.pos):
                        rodando = False
                    elif botao_voltar_menu.collidepoint(e.pos):
                        JogoDaVelhaComBanco.tela_inicial(self)
                        

        if self.executando:
            self.resetar_jogo()

    def resetar_jogo(self):
        self.tabuleiro = ['' for _ in range(9)]
        self.jogador_atual = 'X'
        self.executando = True
    
    def mostrar_tela_historico(self):
        rodando = True
        clock = pygame.time.Clock()
        
        # Atualizar o histórico antes de mostrar
        historico = self.banco.buscar_historico()
        self.tela_historico.atualizar_historico(historico)

        while rodando:
            eventos = pygame.event.get()
            
            # Lidar com eventos na tela de histórico
            resultado = self.tela_historico.lidar_eventos(eventos)
            
            if resultado == "sair":
                rodando = False
                self.executando = False
            elif resultado == "menu":
                rodando = False
                self.tela_historico.atualizar_historico(historico)
            # Desenhar a tela de histórico
            self.tela_historico.desenhar(self.tela)
            pygame.display.flip()
            clock.tick(60)

    def executar(self):
        self.executando = True
        clock = pygame.time.Clock()
        while self.executando:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.executando = False
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    self.tratar_clique_tabuleiro(e.pos)
            self.desenhar_tabuleiro()
            clock.tick(60)
        return False
