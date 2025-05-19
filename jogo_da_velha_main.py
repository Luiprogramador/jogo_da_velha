import pygame
from banco_de_dados import BancoDeDados
from jogo_da_velha_ui import JogoDaVelhaComBanco

def carregar_config_db():
    import os
    return {
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', 'ceub123456'),
        'host': os.getenv('DB_HOST', 'localhost')
    }

def main():
    config = carregar_config_db()
    banco = BancoDeDados(config)
    try:
        banco.conectar()
        banco.criar_database()
        banco.criar_tabela()
        banco.criar_tabela_historico()    
        pygame.init()
        jogo = JogoDaVelhaComBanco(banco)
        jogo.inicializar_pygame()

        if jogo.tela_inicial():
            jogo.executar()
    except Exception as e:
        print(f"Erro crítico: {e}")
    finally:
        banco.fechar()
        pygame.quit()
        print("Banco de dados fechado e pygame encerrado.")

if __name__ == "__main__":
    main()
