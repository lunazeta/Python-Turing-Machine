import pygame
from math import floor

class TapeDisplay:

    ONSCREEN = 7
    PADDING = 10
    WIDTH = 1000
    HEAD_SIZE = 100
    SQUARE_SIZE = ((WIDTH-2*PADDING)/ONSCREEN)
    HEIGHT = SQUARE_SIZE + HEAD_SIZE
    TEXTSPACINGY = SQUARE_SIZE/3.25
    BGCOLOR = pygame.Color(0,0,0)
    COLOR = pygame.Color(255,255,255)
    HALT_STATE_COLOR = pygame.Color(0,255,0)

    def _writeText(self, i: int, xCoord: tuple[float,float], tape: dict[str, int, int], currentState: str):
        tapeMin, tapeMax = tape[1], tape[2]
        if i < tapeMin or i > tapeMax:
            toDraw = "_"
        else:
            toDraw = tape[0][i - tapeMin]
        tapeText = self.font.render(toDraw, False, self.COLOR)
        stateText = self.font.render(currentState, False, self.COLOR)
        
        self.display.blit(stateText, (self.PADDING,0))
        self.display.blit(tapeText, (xCoord + self.SQUARE_SIZE/(2.5), self.HEAD_SIZE + self.TEXTSPACINGY))

    def _drawBoxes(self, xCoord: tuple[float,float]):
        rect = pygame.Rect(xCoord, self.HEAD_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE)
        pygame.draw.rect(self.display, self.COLOR, rect, width=3)

    def _drawHead(self):
        xCoord = self.PADDING + floor(self.ONSCREEN/2)*self.SQUARE_SIZE
        points = ((xCoord, 0), (xCoord + self.SQUARE_SIZE, 0), (xCoord + self.SQUARE_SIZE/2, self.HEAD_SIZE))
        pygame.draw.polygon(self.display, self.COLOR, points)

    def update(self, operations: list, t: int):
        self.display.fill(self.BGCOLOR)

        step = floor(t/60)
        currentOperations = operations[step]
        currentIndex = currentOperations[1]

        for i in range(currentIndex - floor(self.ONSCREEN/2), currentIndex + floor(self.ONSCREEN/2) + 1):
            rectNumber = i - currentIndex + floor(self.ONSCREEN/2)
            xCoord = self.PADDING + rectNumber*self.SQUARE_SIZE
            self._drawBoxes(xCoord)
            self._writeText(i, xCoord, currentOperations[2], currentOperations[0])
        
        self._drawHead()
            
        pygame.display.update()

    def __init__(self):
        pygame.font.init()
        pygame.display.set_caption("Turing Machine")
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        self.font = pygame.font.SysFont("Arial", 70)

    def run(self, operations: list):
        running = True
        waiting = False
        t = 0
        while running:
            if floor(t/60) < len(operations):
                self.update(operations, t)
                self.clock.tick(60)
                t += 1
            else:
                haltText = self.font.render(operations[-1][0], False, self.HALT_STATE_COLOR)
                self.display.blit(haltText, (self.PADDING, 0))
                print(f"Result: {operations[-1][2][0].strip('_')}")

                pygame.display.update()
                running = False
                waiting = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
        
        pygame.quit()