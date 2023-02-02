import pygame

class StateNode:

    COLOR = pygame.Color(255,255,255)
    RADIUS = 50
    BORDER_COLOR = pygame.Color(0,0,0)
    MAX_SELF_CONNECTIONS = 3

    def __init__(self, coords: tuple[int, int], state: str):
        self.coords = coords
        self.state = state

class MovableStateNode(StateNode):
    pass

class Diagram:

    WIDTH = 1000
    HEIGHT = 500
    BG_COLOR = pygame.Color(0,0,0)
    TEXT_SCALING_FACTOR = 1
    TEXT_COLOR = pygame.Color(255,255,255)
    STATE_TEXT_COLOR = pygame.Color(0,0,0)
    CONNECTION_COLOR = pygame.Color(255,255,255)
    TEXT_PLACEMENT_MULTIPLIER = 2.5

    def _onClick(self, coords: tuple[int, int], nodesPlaced, nodeIndex, allPlaced, stateToNode, nodeMoving=None, nodePlacing=None):
        for node in self.nodes:
            if node == nodeMoving:
                break
            coordsXInNode = coords[0] in range(node.coords[0] - node.RADIUS, node.coords[0] + node.RADIUS + 1)
            coordsYInNode = coords[1] in range(node.coords[1] - node.RADIUS, node.coords[1] + node.RADIUS + 1)
            if coordsXInNode and coordsYInNode:
                if nodeMoving:
                    return nodesPlaced, nodeMoving, nodeIndex, stateToNode
                nodesPlaced[node.state] = False
                stateToNode[node.state] = None

                return nodesPlaced, node, nodeIndex, stateToNode

        if allPlaced:
            return nodesPlaced, None, nodeIndex, stateToNode

        if nodeMoving:
            nodesPlaced[nodeMoving.state] = True
            stateToNode[nodeMoving.state] = nodeMoving
            return nodesPlaced, None, nodeIndex, stateToNode
        
        nodeToBePlaced = StateNode(coords, nodePlacing)
        self.nodes.append(nodeToBePlaced)
        nodesPlaced[nodePlacing] = True
        stateToNode[nodePlacing] = nodeToBePlaced
        return nodesPlaced, None, nodeIndex + 1, stateToNode

    def _drawNodeConnections(self, stateToNode, nodeMoving):
        for node in self.nodes:
            if node == nodeMoving:
                continue
            for read in enumerate(self.deltaFunction[node.state]):
                connection = self.deltaFunction[node.state][read[1]]
                if connection[0] not in stateToNode:
                    pass
                elif stateToNode[connection[0]] == node and read[0] < node.MAX_SELF_CONNECTIONS:
                    match read[0]:
                        case 0:
                            left = node.coords[0] - node.RADIUS*2
                            top = node.coords[1] - node.RADIUS/2
                            width = node.RADIUS*2
                            height = node.RADIUS
                        case 1:
                            left = node.coords[0] - node.RADIUS/2
                            top = node.coords[1] - node.RADIUS*2
                            width = node.RADIUS
                            height = node.RADIUS*2
                        case 2:
                            left = node.coords[0] - node.RADIUS/2
                            top = node.coords[1] + node.RADIUS*2
                            width = node.RADIUS
                            height = node.RADIUS*2
                    ellipseRect = pygame.Rect(left,top,width,height)
                    pygame.draw.ellipse(self.display, self.CONNECTION_COLOR, ellipseRect, width=1)
                elif stateToNode[connection[0]]:
                    midpointX = (node.coords[0] + stateToNode[connection[0]].coords[0])/2
                    midpointY = (node.coords[1] + stateToNode[connection[0]].coords[1])/2
                    text = f"{read[1]}/{connection[1]}/{connection[2]}"
                    textSurf = self.font.render(text, False, self.TEXT_COLOR)
                    pygame.draw.line(self.display, self.CONNECTION_COLOR, node.coords, stateToNode[connection[0]].coords)
                    self.display.blit(textSurf, (midpointX - len(text)*self.TEXT_PLACEMENT_MULTIPLIER, midpointY))
                    
    def _updateNodes(self):
        for node in self.nodes:
            pygame.draw.circle(self.display, node.COLOR, node.coords, node.RADIUS)
            pygame.draw.circle(self.display, node.BORDER_COLOR, node.coords, node.RADIUS, width=1)
            if node.state == self.haltingState:
                pygame.draw.circle(self.display, node.BORDER_COLOR, node.coords, node.RADIUS/1.1, width=1)
            stateText = self.font.render(node.state, False, self.STATE_TEXT_COLOR)
            self.display.blit(stateText, (node.coords[0] - node.RADIUS*(2**0.5)/2, node.coords[1] - node.RADIUS*(2**0.5)/2))
    
    def _initPygame(self):
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", StateNode.RADIUS*self.TEXT_SCALING_FACTOR)
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Turing Machine Diagram")
        self.clock = pygame.time.Clock()
        self.nodes = []

    def __init__(self, deltaFunction: dict, haltingState: str):
        self.deltaFunction = deltaFunction
        self.haltingState = haltingState
        self.states = [i for i in deltaFunction]
        self._initPygame()
    
    def run(self):
        running = True
        nodesPlaced = {i:False for i in self.states}
        stateToNode = {}
        nodeMoving = None
        allPlaced = False
        mouseClickHandled = False
        node = 0

        while running:
            self.display.fill(self.BG_COLOR)

            if nodeMoving:
                nodeMoving.coords = pygame.mouse.get_pos()

            nodePlacing = self.states[node] if not (nodeMoving or allPlaced) else None

            if pygame.mouse.get_pressed()[0] and not mouseClickHandled:
                nodesPlaced, nodeMoving, node, stateToNode = self._onClick(
                    pygame.mouse.get_pos(), 
                    nodesPlaced,
                    node,
                    allPlaced,
                    stateToNode,
                    nodeMoving=nodeMoving,
                    nodePlacing=nodePlacing
                )

                allPlaced = True
                for state in nodesPlaced:
                    if not nodesPlaced[state]:
                        allPlaced = False
                
                mouseClickHandled = True
            
            self._drawNodeConnections(stateToNode, nodeMoving)
            self._updateNodes()

            if allPlaced:
                # Take screenshot here and save as file?
                pass
            
            pygame.display.update()
            self.clock.tick(30)
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        running = False
                    case pygame.MOUSEBUTTONUP:
                        mouseClickHandled = False

        pygame.quit()

class MoveableDiagram(Diagram):
    pass