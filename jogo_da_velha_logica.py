from typing import Optional

class JogoDaVelha_Logica:
    def __init__(self):
        self.tabuleiro = ['' for _ in range(9)]
        self.jogador_atual = 'X'

    def fazer_jogada(self, posicao: int) -> bool:
        if 0 <= posicao < 9 and self.tabuleiro[posicao] == '':
            self.tabuleiro[posicao] = self.jogador_atual
            return True
        return False

    def verificar_vencedor(self) -> Optional[str]:
        combos = [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]
        for a,b,c in combos:
            if self.tabuleiro[a] == self.tabuleiro[b] == self.tabuleiro[c] != '':
                return self.tabuleiro[a]
        if '' not in self.tabuleiro:
            return 'Empate'
        return None

    def alternar_jogador(self):
        self.jogador_atual = 'O' if self.jogador_atual == 'X' else 'X'

    def resetar(self):
        self.tabuleiro = ['' for _ in range(9)]
        self.jogador_atual = 'X'
