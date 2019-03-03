import Human_Player
import Slow_AI
import Fast_AI
import pygame

while True:
    gameDisplay = pygame.display.set_mode((600, 600))
    gameDisplay.fill((255, 255, 255))
    humanX, humanY, humanWidth, humanHeight = 20, 50, 500, 120
    gameDisplay.blit(pygame.image.load("HumanButton.png"), (humanX, humanY))
    fastX, fastY, fastWidth, fastHeight = 20, 220, 500, 120
    gameDisplay.blit(pygame.image.load("FastAIButton.png"), (fastX, fastY))
    slowX, slowY, slowWidth, slowHeight = 20, 390, 500, 120
    gameDisplay.blit(pygame.image.load("SlowAIButton.png"), (slowX, slowY))
    pygame.display.update()
    needsReset = False
    while not needsReset:
        #pygame.display.update()
        mousepos = pygame.mouse.get_pos()
        mousebuttons = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                if (humanX < mouseX < humanX + humanWidth)\
                        and (humanY < mouseY < humanY + humanHeight):
                    pygame.quit()
                    Human_Player.HumanPlayer().playGame()
                    needsReset = True
                elif (fastX < mouseX < fastX + fastWidth)\
                        and (fastY < mouseY < fastY + fastHeight):
                    pygame.quit()
                    Fast_AI.FastPlayer().playGame()
                    needsReset = True
                elif (slowX < mouseX < slowX + slowWidth)\
                        and (slowY < mouseY < slowY + slowHeight):
                    pygame.quit()
                    Slow_AI.SimplePlayer().playGame()
                    needsReset = True
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()