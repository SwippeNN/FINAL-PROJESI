
import pygame, sys

from pygame import display
from pygame import sprite




class StartAnimation(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y):
		super().__init__()
		self.attack_animation = False
		self.sprites = []
		self.sprites.append(pygame.image.load('1.png'))
		self.sprites.append(pygame.image.load('2.png'))
		self.sprites.append(pygame.image.load('3.png'))
		self.sprites.append(pygame.image.load('4.png'))
		self.sprites.append(pygame.image.load('5.png'))
		self.sprites.append(pygame.image.load('6.png'))
		self.sprites.append(pygame.image.load('7.png'))
		self.sprites.append(pygame.image.load('8.png'))
		self.sprites.append(pygame.image.load('9.png'))
		self.sprites.append(pygame.image.load('10.png'))
		pass
		self.sprites.append(pygame.image.load('11.png'))
		self.sprites.append(pygame.image.load('12.png'))
		self.sprites.append(pygame.image.load('13.png'))
		self.sprites.append(pygame.image.load('14.png'))
		self.sprites.append(pygame.image.load('15.png'))
		self.sprites.append(pygame.image.load('16.png'))
		self.sprites.append(pygame.image.load('17.png'))
		self.sprites.append(pygame.image.load('18.png'))
		self.sprites.append(pygame.image.load('19.png'))
		self.sprites.append(pygame.image.load('20.png'))
		self.sprites.append(pygame.image.load('21.png'))
		self.sprites.append(pygame.image.load('22.png'))
		self.sprites.append(pygame.image.load('23.png'))
		self.sprites.append(pygame.image.load('24.png'))
		self.sprites.append(pygame.image.load('25.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
		self.sprites.append(pygame.image.load('26.png'))
	

		
		
		self.current_sprite = 0
		self.image = self.sprites[self.current_sprite]

		self.rect = self.image.get_rect()
		self.rect.topleft = [pos_x,pos_y]
		
	def attack(self):
		self.attack_animation = True

	

		

	def update(self,speed):
		if self.attack_animation == True:
			self.current_sprite += speed
			if int(self.current_sprite) >= len(self.sprites):
				self.current_sprite = 26
				self.attack_animation = False

		self.image = self.sprites[int(self.current_sprite)]
	



pygame.init()
clock = pygame.time.Clock()


screen_width = 1900
screen_height = 1080
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Game Start Animation")


moving_sprites = pygame.sprite.Group()
StartAnimation = StartAnimation(100,100)
moving_sprites.add(StartAnimation)
StartAnimation.attack()
pygame.init()
m = "giris.wav"
pygame.mixer.music.load(m)
pygame.mixer.music.play()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			import main
			pygame.quit() and sys.exit() and main()
			
			
		
		
	
	screen.fill((0,0,0))
	moving_sprites.draw(screen)

	moving_sprites.update(0.16)
	pygame.display.update()
	
	clock.tick(60)

	