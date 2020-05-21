import pygame
import sys
import random

pygame.init()

CELL_SIZE = 25

HEIGHT = 30
WIDTH = 30

SCREEN_COLOR = (12, 12, 12)
SCREEN_SIZE =  pygame.display.Info().current_w, pygame.display.Info().current_h
LINE_COLOR = (20, 20, 20)
BORDER_COLOR = (255, 255, 255)
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR =  (255, 0, 0)
SCORE = 0
TICK = 15
LIVES = 3

SNAKE = [
  [2, 4],
  [2, 3],
  [2, 2]
]

SNAKE_DEFAULT = SNAKE

DIRECTION = 'RIGHT'


class Game():

	def __init__(self, snake_direction, food_color, cell_size, width, height, start_score, snake_color, snake, line_color, border_color, screen_color, screen_size, tick, lives):
		self.lives = int(lives)
		self.snake_direction = snake_direction
		self.food_color = food_color
		self.cell_size = cell_size
		self.width = width
		self.height = height
		self.start_score = start_score
		self.snake_color = snake_color
		self.snake = snake
		self.line_color = line_color
		self.border_color = border_color
		self.screen_color = screen_color
		self.screen_size = screen_size
		self.tick = int(tick)
		self.tick_default = int(tick)
		self.fail_sound = pygame.mixer.Sound('fail.ogg')
		self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.FULLSCREEN)
		pygame.display.set_caption('SNAKE')
		self.fps = pygame.time.Clock()
		self.surf = pygame.Surface(((self.width * self.cell_size), (self.height * self.cell_size)))


	def game_over(self):
		self.fail_sound.play()
		self.c.reset()
		self.c.minus_life()
		self.snake.reset()
		self.food.create_food()
		self.tick = self.tick_default


	def run_game(self):

		self.food = Food(self.surf, self.food_color, self.cell_size, self.width, self.height)
		self.snake = Snake(self, self.surf, self.snake_color, self.cell_size, self.snake, self.food, self.snake_direction)
		self.lines = Lines(self.surf, self.height, self.width, self.cell_size, self.line_color, self.border_color)

		self.c = Counter(self.screen, self.start_score, self.lives)

		self.food.create_food()

	def draw_screen(self):
		self.screen.fill(self.screen_color)
		self.c.write_text()
		self.c.draw_hearts(self.screen_color)
		self.snake.move()
		self.snake.check_collisions()
		self.snake.draw()
		self.food.draw()
		self.lines.draw_lines()
		self.screen.blit(self.surf, (((self.screen_size[0] - self.width * self.cell_size) / 2), ((self.screen_size[1] - self.height * self.cell_size) / 2)))
		self.surf.fill((0, 0, 0))
		pygame.display.flip()
		self.fps.tick(self.tick)

	def draw_game_over(self):
		self.screen.fill(self.screen_color)
		game_over_font = pygame.font.Font('RobotoMono-Bold.ttf', 144)
		game_over_text = game_over_font.render('GAME OVER', 1, (255, 255, 255))
		text_rect = game_over_text.get_rect()
		press_esc_font = pygame.font.Font('RobotoMono-Bold.ttf', 48)
		press_esc_text = press_esc_font.render('Press ESC to quit the game', 1, (255, 255, 255))
		esc_rect = press_esc_text.get_rect()
		press_return_font = pygame.font.Font('RobotoMono-Bold.ttf', 48)
		press_return_text = press_return_font.render('Or press RETURN to start again', 1, (255, 255, 255))
		return_rect = press_return_text.get_rect()

		self.screen.blit(game_over_text, ((self.screen_size[0] - text_rect[2])/2, (self.screen_size[1] - text_rect[3])/2))
		self.screen.blit(press_esc_text, ((self.screen_size[0] - esc_rect[2])/2, 700))
		self.screen.blit(press_return_text, ((self.screen_size[0] - return_rect[2])/2, 800))
		pygame.display.flip()

	def reset_game(self):
		pass

	def speed_increase(self):
		self.tick = self.tick + 0.5


	def game_mainloop(self):
		self.run_game()
		while True:
			if self.c.lives > 0:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit()
					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_RIGHT and self.snake.direction != 'LEFT':
							self.snake.direction = 'RIGHT'
						elif event.key == pygame.K_LEFT and self.snake.direction != 'RIGHT':
							self.snake.direction = 'LEFT'
						elif event.key == pygame.K_DOWN and self.snake.direction != 'UP':
							self.snake.direction = 'DOWN'
						elif event.key == pygame.K_UP and self.snake.direction != 'DOWN':
							self.snake.direction = 'UP'
						elif event.key == pygame.K_ESCAPE:
							sys.exit()

				self.draw_screen()
			else:
				self.draw_game_over()
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE:
							sys.exit()
						elif event.key == pygame.K_RETURN:
							self.c.lives = 3




class Counter():

	def __init__(self, screen, score, lives):
		self.screen = screen
		self.score = score
		self.lives = lives
		self.heart_image = pygame.image.load('heart.png')
		self.heart_image_rect = self.heart_image.get_rect()

	def write_text(self):
		score_font = pygame.font.Font('RobotoMono-Bold.ttf', 24)
		score_text = score_font.render(('Score: ' + str(self.score)), 1, (255, 255, 255))
		self.screen.blit(score_text, (20 , 70))

	def draw_hearts(self, screen_color):
		hearts_bar = pygame.Surface((144, 48))
		hearts_bar.fill(screen_color)
		for i in range(self.lives):
			hearts_bar.blit(self.heart_image, ((i * 48),0))
		self.screen.blit(hearts_bar, (20, 20))

	def score_increase(self):
		self.score = self.score + 1

	def minus_life(self):
		self.lives = self.lives - 1

	def reset(self):
		self.score = 0


class Lines():

	def __init__(self, scr, h, w, cs, line_color, border_color):
		self.scr = scr
		self.h = h
		self.w = w
		self.cs = cs
		self.color = line_color
		self.border_color = border_color
	def draw_lines(self):
		for x in range(0, (self.w * self.cs), self.cs):
			pygame.draw.line(self.scr, self.color, [x, 0], [x, (self.cs * self.h)])
		for y in range(0, (self.h * self.cs), self.cs):
			pygame.draw.line(self.scr, self.color, [0, y],[(self.cs * self.w), y])
		pygame.draw.rect(self.scr, self.border_color, (0, 0, (self.h * self.cs),(self.w * self.cs)), 1)



class Food():

	def __init__(self, scr, color, cell_size, max_x, max_y):
		self.scr = scr
		self.color = color
		self.cell_size = cell_size
		self.max_x = max_x - 1
		self.max_y = max_y - 1
		self.x = 0
		self.y = 0

	def create_food(self):
		self.x = random.randint(1, self.max_x)
		self.y = random.randint(1, self.max_y)


	def	draw(self):
			food = pygame.draw.rect(
			self.scr,
			self.color,
			(
			(self.x * self.cell_size - self.cell_size), (self.y * self.cell_size - self.cell_size),
			self.cell_size, self.cell_size
			)
			)



class Snake():

	def __init__(self, game, scr, color, element_size, elements, food, direction):

		self.game = game
		self.scr = scr
		self.color = color
		self.element_size = element_size
		self.elements = elements
		self.body_elements_position = list(self.elements)
		self.head = list(self.body_elements_position[0])
		self.position = self.head
		self.food = food
		self.direction = direction
		self.eat_sound = pygame.mixer.Sound('has_eaten.ogg')

	def move(self):
		if self.direction == 'UP':
			self.head[1] = self.head[1] - 1
		elif self.direction == 'DOWN':
			self.head[1] = self.head[1] + 1
		elif self.direction == 'RIGHT':
			self.head[0] = self.head[0] + 1
		elif self.direction == 'LEFT':
			self.head[0] = self.head[0] - 1
		self.body_elements_position.insert(0, list(self.head))

		if self.head[0] == self.food.x and self.head[1] == self.food.y:

			self.eat_sound.play()
			self.food.create_food()
			self.game.c.score_increase()
			self.game.speed_increase()
		else:
			self.body_elements_position.pop()

	def check_collisions(self):
		for element in self.body_elements_position[1:]:
			if self.head == element:
				self.game.game_over()

		if self.head[0] > self.game.width:
			self.game.game_over()
		elif self.head[0] < 1:
			self.game.game_over()
		elif self.head[1] > self.game.height:
			self.game.game_over()
		elif self.head[1] < 1:
			self.game.game_over()


	def draw(self):
		for i in range(0, len(self.body_elements_position)):
			draw = pygame.draw.rect(
			self.scr, self.color,
			((self.body_elements_position[i][0] * self.element_size - self.element_size),
			 (self.body_elements_position[i][1] * self.element_size - self.element_size),
			 self.element_size, self.element_size))



	def reset(self):
		self.body_elements_position = list(self.elements)
		self.head = list(self.body_elements_position[0])
		self.direction = 'RIGHT'



class Menu():

	def create_menu(self):
		pass

if __name__ == '__main__':

	game = Game(DIRECTION, FOOD_COLOR, CELL_SIZE, WIDTH, HEIGHT, SCORE, SNAKE_COLOR, SNAKE, LINE_COLOR, BORDER_COLOR, SCREEN_COLOR, SCREEN_SIZE, TICK, LIVES)
	game.game_mainloop()
