import mysql.connector
from mysql.connector import Error
import json


class BancoDeDados:
    def __init__(self, config):
        self.config = config
        self.conexao = None
        self.cursor = None

    def conectar(self):
        try:
            self.conexao = mysql.connector.connect(
                user=self.config['user'],
                password=self.config['password'],
                host=self.config['host']
            )
            if self.conexao.is_connected():
                self.cursor = self.conexao.cursor()
                self.criar_database()
                self.conexao.database = 'db_tictactoe'
                self.criar_tabela()
            else:
                raise Error("Falha ao conectar ao MySQL")
        except Error as e:
            print(f"Erro na conexão: {e}")
            self.conexao = None
            self.cursor = None
            raise

    def criar_database(self):
        try:
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS db_tictactoe")
        except Error as e:
            print(f"Erro ao criar DB: {e}")

    def criar_tabela(self):
        sql = """
        CREATE TABLE IF NOT EXISTS tb_resultados (
            id INT AUTO_INCREMENT PRIMARY KEY,
            jogador_x VARCHAR(50) NOT NULL,
            jogador_o VARCHAR(50) NOT NULL,
            vencedor VARCHAR(50) NOT NULL,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.cursor.execute(sql)
        self.conexao.commit()

    def salvar_resultado(self, jogador_x, jogador_o, vencedor):
        try:
            
            sql = "INSERT INTO tb_resultados (jogador_x, jogador_o, vencedor) VALUES (%s, %s, %s)"
            self.cursor.execute(sql, (jogador_x, jogador_o, vencedor))
            self.conexao.commit()
            return True
        except Error as e:
            print(f"Erro ao salvar resultado: {e}")
            return False
    
    
    def criar_tabela_historico(self):
        sql = """
            CREATE TABLE IF NOT EXISTS historico_partidas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                jogador_x VARCHAR(100),
                jogador_o VARCHAR(100),
                vencedor VARCHAR(100),
                jogadas TEXT,
                data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        self.cursor.execute(sql)
        self.conexao.commit()

    def salvar_partida_no_historico(self, jogador_x, jogador_o, vencedor, jogadas):
        try:
            sql = " INSERT INTO historico_partidas (jogador_x, jogador_o, vencedor, jogadas) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(sql, (jogador_x, jogador_o, vencedor, json.dumps(jogadas)))
            self.conexao.commit()
            return True
        except Error as e:
            print(f"Erro ao salvar partida no histórico: {e}")
            return False

    def buscar_historico(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT jogador_x, jogador_o, vencedor, data_hora FROM historico_partidas ORDER BY data_hora DESC")
        historico = cursor.fetchall()
        return historico    
    
    def apagar_historico(self):
        try:
            sql = "DELETE FROM historico_partidas"
            self.cursor.execute(sql)
            self.conexao.commit()
            return True
        except Error as e:
            print(f"Erro ao apagar histórico: {e}")
            return False

    def fechar(self):
        if self.cursor:
            self.cursor.close()
        if self.conexao:
            self.conexao.close()
