from pygame.sprite import groupcollide

from bubble import *

from time import *

# level bubbles
bubbles = pygame.sprite.Group()

# explosions when bubble dies
projectiles = pygame.sprite.Group()

rowNr = 6
colNr = 5
windowWidth = 100*colNr
windowHeight = 100*rowNr
center = (windowWidth/2, windowHeight/2)
scoreVerticalSpace = 80
win = pygame.display.set_mode((windowWidth, windowHeight + scoreVerticalSpace))

#function for AI to generate moves
def clickBubble(grid, pos):
    row = pos[0]
    col = pos[1]

    grid[row][col] -= 1

    if grid[row][col] > 0:
        return grid

    else:
        #burst bubble above
        for i in range(row-1, -1, -1):
            if grid[i][col] > 0:
                #explode next bubble
                grid = clickBubble(grid, (i, col))
                break

        # burst bubble below
        for i in range(row, rowNr):
            if grid[i][col] > 0:
                # explode next bubble
                grid = clickBubble(grid, (i, col))
                break

        #burst bubble left
        for i in range(col-1, -1, -1):
            if grid[row][i] > 0:
                # explode next bubble
                grid = clickBubble(grid, (row, i))
                break

        # burst bubble right
        for i in range(col, colNr):
            if grid[row][i] > 0:
                # explode next bubble
                grid = clickBubble(grid, (row, i))
                break

        return grid

#currently just for testing, makes a predefined move
def BFS(grid):
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for row in grid]))

    print("\n")

    grid = clickBubble(grid, (1, 3))

    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for row in grid]))

#write text in the screen
def writeToScreen(pos, text, clearScreen):
    if clearScreen:
        win.fill((0, 0, 0))

    smallfont = pygame.font.SysFont("Arial", 25)
    textSurf = smallfont.render(text, True, (255, 255, 255))
    textRect = textSurf.get_rect()
    textRect.center = pos
    win.blit(textSurf, textRect)

#checks collision between sprites, removes projectiles which hit balls
def checkCollisions():
    # dictionary with bubbles and projectiles which collided
    ballsHit = groupcollide(bubbles, projectiles, False, True)
    scoreAddition = 0

    for bubble in ballsHit.keys():

        #fix case when bubble is hit multiple times simultaneously
        for hit in range (0, len(ballsHit[bubble])-1):
            bubble.hit()

        newExplosion = bubble.hit()

        if newExplosion != None:
            scoreAddition += bubble.score*len(ballsHit[bubble])
            bubbles.remove(bubble)
            projectiles.add(newExplosion[0][0])
            projectiles.add(newExplosion[0][1])
            projectiles.add(newExplosion[0][2])
            projectiles.add(newExplosion[0][3])

    #remove projectiles that leave screen
    for projectile in projectiles:
        if projectile.x < 0 or projectile.y < 0 or projectile.x > windowWidth or projectile.y > windowHeight:
            projectiles.remove(projectile)

    return scoreAddition


#animate a move
def makeMove(bubble, score):
    # if bubble is clicked, make it get hit and decrement touchesLeft
    newExplosion = bubble.hit()

    # if bubble dies, add explosions
    if newExplosion != None:
        score += bubble.score
        bubbles.remove(bubble)

        projectiles.add(newExplosion[0][0])
        projectiles.add(newExplosion[0][1])
        projectiles.add(newExplosion[0][2])
        projectiles.add(newExplosion[0][3])


# Project main loop
def game(startGrid, touchesLeft):
    pygame.init()
    pygame.display.set_caption("Bubble blast")

    score = 0
    gameOver = False

    # create bubble list
    for i in range(0, len(startGrid[0])):
        for j in range(0, len(startGrid)):
            #dont create level 0 balls
            if startGrid[j][i] > 0:
                bubbles.add(Bubble((100 * i + 50, 100 * j + scoreVerticalSpace), startGrid[j][i]))

    intro = run = True
    computer = human = False

    while run:
        writeToScreen(center, "Press H to play in human mode. ", True)
        writeToScreen((center[0], center[1] + 30), "Press C to play in computer mode. ", False)
        pygame.display.flip()

        #MAIN MENU
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        human = True
                        intro = False
                    if event.key == pygame.K_c:
                        computer = True
                        intro = False


        #HUMAN MODE
        while(not gameOver and human):

            # update bubbles, projectiles
            bubbles.update()
            projectiles.update()

            # check collisions between projectiles and bubbles. update score
            score += checkCollisions()

            # draw all entities
            writeToScreen((center[0], 20), "Score: " + str(score), False)
            writeToScreen((center[0], windowHeight + 50), "Touches left: " + str(touchesLeft), False)
            bubbles.draw(win)
            projectiles.draw(win)

            # check mouse events
            for event in pygame.event.get():

                # check mouse click on exit button
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # check mouse click on bubble
                if event.type == pygame.MOUSEBUTTONUP:
                    for bubble in bubbles:
                        if bubble.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):

                            makeMove(bubble, score)
                            touchesLeft -= 1

                if touchesLeft <= 0:
                    break


            if touchesLeft <= 0 and len(projectiles) <= 0:
                if len(bubbles) > 0:
                    writeToScreen(center, "Game over :(", True)

                else:
                    writeToScreen(center, "You won!", True)

                gameOver = True





            if len(bubbles) == 0:
                writeToScreen(center, "You won! :D", True)
                gameOver = True
                run = False


            # update whole screen
            pygame.display.flip()

            # fill background
            win.fill((0, 0, 0))


        #COMPUTER MODE
        while(computer):

            writeToScreen(center, "Press A to BFS algorithm", True)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        startGrid = BFS(startGrid)

            # update whole screen
            pygame.display.flip()



        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()





touchesLeft = 3
startGrid = []

startGrid.append([1, 1, 1, 1, 1])
startGrid.append([4, 2, 3, 1, 2])
startGrid.append([2, 1, 4, 1, 2])
startGrid.append([3, 0, 1, 3, 0])
startGrid.append([2, 1, 0, 4, 3])
startGrid.append([0, 3, 2, 3, 1])

# startGrid.append([0, 0, 0, 0, 0])
# startGrid.append([0, 0, 1, 1, 0])
# startGrid.append([0, 0, 2, 1, 0])
# startGrid.append([0, 0, 0, 0, 0])
# startGrid.append([0, 0, 0, 0, 0])
# startGrid.append([0, 0, 0, 0, 0])


game(startGrid, touchesLeft)
