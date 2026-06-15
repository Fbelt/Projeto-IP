import pygame
class personagem:
    def __init__(self, nome):
        self.nome = nome
    def falar(self, frase):
        print(f"{self.nome} diz: {frase}")
class heroi(personagem):
    def __init__(self, nome, poder):
        super().__init__(nome)
        self.poder = poder
    def usar_poder(self):
        print(f"{self.nome} usa seu poder: {self.poder}")

mario = heroi("Mario", "Super Força")
mario.falar("Vamos salvar a princesa!")