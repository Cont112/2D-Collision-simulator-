#Importa bibliotecas necessárias
import pygame, sys
from pygame.locals import *
from random import randint
import math


FPS = 60
fpsClock = pygame.time.Clock()

N = 50

V_MAX = 5
V_MIN = -5

MASS_MIN = 20
MASS_MAX = 40
RATIO = 1


COLOR = 0x00F08F


window = pygame.display.set_mode((1600, 960), pygame.RESIZABLE)
WIDTH, LENGTH = pygame.display.get_surface().get_size()
pygame.display.set_caption("Simulador de Colisões")


#classe das bolas
class bola:
   #Incializa as propriedades dos objetos da classe 
   def __init__(self,screen):
       
      self.screen = screen
      self.color = COLOR #Macro para cor das bolas

      self.mass = randint(MASS_MIN, MASS_MAX) #Massa aleatória num intervalo predeterminado
      self.radius = int(RATIO * self.mass) #Raio em função da massa 

      self.x = 0
      self.y = 0
      self.pos = pygame.math.Vector2(self.x,self.y) #Vetor posição

      self.vx = randint(V_MIN,V_MAX) #Velocidade no eixo X aleatória num intervalo predeterminado
      self.vy = randint(V_MIN,V_MAX) #Velocidaae no eixo Y aleatória num intervalo predeterminado
      self.v = pygame.math.Vector2(self.vx,self.vy) #Vetor velocidade

   #Funcao que desenha as bolas na tela
   def draw(self):
      pygame.draw.circle(self.screen,self.color,self.pos,self.radius)

   #Funcao de movimento
   def move(self):
      self.pos += self.v
      

   #Funcao que controla a colisao com as paredes
   def manageWallCollision(self):
      WIDTH, LENGTH = pygame.display.get_surface().get_size()

      if self.pos[0] + self.radius >= WIDTH and self.v[0] > 0:
         self.v[0] *= -1
      if self.pos[0] - self.radius <= 0 and self.v[0] < 0:
         self.v[0] *= -1
      if self.pos[1] + self.radius >= LENGTH and self.v[1] > 0:
         self.v[1] *= -1 
      if self.pos[1] - self.radius <= 0 and self.v[1] < 0:
         self.v[1] *= -1

#Funcao que retorna um vetor de posicao aleatoria 
def rPos(obj):
   x = randint(0 + obj.radius, WIDTH - obj.radius)
   y = randint(0 + obj.radius, LENGTH - obj.radius)
   pos = pygame.math.Vector2(x,y)
   return (pos)

#Inicializa os objetos e coloca numa lista
list = []  
for i in range(N):
   list.append(bola(window))


#Spawna as bolas em posicoes aleatorias diferentes das bolas anteriores e não muito próximas umas das outras
i = 0
while i < N:
   list[i].pos = rPos(list[i])
   for j in range(0,i,1):
      distance = math.hypot(list[i].pos[0] - list[j].pos[0], list[i].pos[1] - list[j].pos[1])
      if distance + 10 <= list[i].radius + list[j].radius:
         i = i - 1
         break
   i += 1


#Nao deixa as bolas entrarem uma na outra durante a colisao
def separaBolas(obj1,obj2):
   distance = math.hypot(obj1.pos[0] - obj2.pos[0], obj1.pos[1] - obj2.pos[1])

   offset = obj1.radius + obj2.radius - distance

   dx = (obj1.pos[0] - obj2.pos[0]) / distance * offset
   dy = (obj1.pos[1] - obj2.pos[1]) / distance * offset

   obj1.pos[0] += dx/2
   obj1.pos[1] += dy/2

   obj2.pos[0] -= dx/2
   obj2.pos[1] -= dy/2

#Checa a colisao e calcula os vetores velocidade resultante
#com base na formula em:
# www.wikipedia.org/wiki/Elastic_collision
def checkBallCollision(obj1, obj2):
   distance = math.hypot(obj1.pos[0] - obj2.pos[0], obj1.pos[1] - obj2.pos[1])
   if distance <= obj1.radius + obj2.radius:
      
      v1 = obj1.v
      v2 = obj2.v
      x1 = obj1.pos
      x2 = obj2.pos
      m1 = obj1.mass
      m2 = obj2.mass

      obj1.v = v1 - (2*m2/(m1+m2)) * pygame.math.Vector2.project((v1 - v2), (x1 - x2)) 
      obj2.v = v2 - (2*m1/(m1+m2)) * pygame.math.Vector2.project((v2 - v1), (x2 - x1))
 
      separaBolas(obj1,obj2) #Chama afunção que separa as bolas durante a colisão
            


#loop que executa as ações e roda as imagens
run = True
while run:

   fpsClock.tick(FPS)

   #Checa colisao com as bolas sem ter que fazer as comparações 2 vezes 
   for i in range(0,N-1,1):
      for j in range(i+1,N,1):
         checkBallCollision(list[i],list[j])

   #Desenha as bolas, controla o movimento e checa por colisões na parede
   for i in range(0,N,1):
      list[i].draw()
      list[i].move()
      list[i].manageWallCollision()
            
   #Atualiza a janela a cada loop e apaga a bola na posição anterior 
   pygame.display.update()
   window.fill(0x000000)

 
   #Fecha a janela
   for event in pygame.event.get():
      if event.type == QUIT:
         pygame.quit()
         sys.exit()
      elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                     pygame.quit()
                     sys.exit()
               

