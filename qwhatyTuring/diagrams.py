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

    def _on_click(self, coords: tuple[int, int], nodes_placed, nodes_index, all_placed, state_to_node, node_moving=None, node_placing=None):
        for node in self.nodes:
            if node == node_moving:
                break
            coordsXInNode = coords[0] in range(node.coords[0] - node.RADIUS, node.coords[0] + node.RADIUS + 1)
            coordsYInNode = coords[1] in range(node.coords[1] - node.RADIUS, node.coords[1] + node.RADIUS + 1)
            if coordsXInNode and coordsYInNode:
                if node_moving:
                    return nodes_placed, node_moving, nodes_index, state_to_node
                nodes_placed[node.state] = False
                state_to_node[node.state] = None

                return nodes_placed, node, nodes_index, state_to_node

        if all_placed:
            return nodes_placed, None, nodes_index, state_to_node

        if node_moving:
            nodes_placed[node_moving.state] = True
            state_to_node[node_moving.state] = node_moving
            return nodes_placed, None, nodes_index, state_to_node
        
        nodeToBePlaced = StateNode(coords, node_placing)
        self.nodes.append(nodeToBePlaced)
        nodes_placed[node_placing] = True
        state_to_node[node_placing] = nodeToBePlaced
        return nodes_placed, None, nodes_index + 1, state_to_node

    def _draw_node_connections(self, state_to_node, node_moving):
        for node in self.nodes:
            if node == node_moving:
                continue
            for read in enumerate(self.delta_function[node.state]):
                connection = self.delta_function[node.state][read[1]]
                if connection[0] not in state_to_node:
                    pass
                elif state_to_node[connection[0]] == node and read[0] < node.MAX_SELF_CONNECTIONS:
                    match read[0]:
                        case 0:
                            # Ellipse to the left
                            left = node.coords[0] - node.RADIUS*2
                            top = node.coords[1] - node.RADIUS/2
                            width = node.RADIUS*2
                            height = node.RADIUS
                        case 1:
                            # Ellipse up
                            left = node.coords[0] - node.RADIUS/2
                            top = node.coords[1] - node.RADIUS*2
                            width = node.RADIUS
                            height = node.RADIUS*2
                        case 2:
                            # Ellipse down
                            left = node.coords[0] - node.RADIUS/2
                            top = node.coords[1] + node.RADIUS*2
                            width = node.RADIUS
                            height = node.RADIUS*2
                    ellipse_rect = pygame.Rect(left,top,width,height)
                    pygame.draw.ellipse(self.display, self.CONNECTION_COLOR, ellipse_rect, width=1)
                elif state_to_node[connection[0]]:
                    midpoint_x = (node.coords[0] + state_to_node[connection[0]].coords[0])/2
                    midpoint_y = (node.coords[1] + state_to_node[connection[0]].coords[1])/2
                    text = f"{read[1]}/{connection[1]}/{connection[2]}"
                    text_surf = self.font.render(text, False, self.TEXT_COLOR)
                    pygame.draw.line(self.display, self.CONNECTION_COLOR, node.coords, state_to_node[connection[0]].coords)
                    self.display.blit(text_surf, (midpoint_x - len(text)*self.TEXT_PLACEMENT_MULTIPLIER, midpoint_y))
                    
    def _update_nodes(self):
        for node in self.nodes:
            pygame.draw.circle(self.display, node.COLOR, node.coords, node.RADIUS)
            pygame.draw.circle(self.display, node.BORDER_COLOR, node.coords, node.RADIUS, width=1)
            if node.state == self.halting_state:
                pygame.draw.circle(self.display, node.BORDER_COLOR, node.coords, node.RADIUS/1.1, width=1)
            state_text = self.font.render(node.state, False, self.STATE_TEXT_COLOR)
            self.display.blit(state_text, (node.coords[0] - node.RADIUS*(2**0.5)/2, node.coords[1] - node.RADIUS*(2**0.5)/2))
    
    def _initPygame(self):
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", StateNode.RADIUS*self.TEXT_SCALING_FACTOR)
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Turing Machine Diagram")
        self.clock = pygame.time.Clock()
        self.nodes = []

    def __init__(self, delta_function: dict, halting_state: str):
        self.delta_function = delta_function
        self.halting_state = halting_state
        self.states = [i for i in delta_function]
        self._initPygame()
    
    def run(self):
        running = True
        nodes_placed = {i:False for i in self.states}
        state_to_node = {}
        node_moving = None
        all_placed = False
        mouse_click_handled = False
        node = 0

        while running:
            self.display.fill(self.BG_COLOR)

            if node_moving:
                node_moving.coords = pygame.mouse.get_pos()

            node_placing = self.states[node] if not (node_moving or all_placed) else None

            if pygame.mouse.get_pressed()[0] and not mouse_click_handled:
                nodes_placed, node_moving, node, state_to_node = self._on_click(
                    pygame.mouse.get_pos(), 
                    nodes_placed,
                    node,
                    all_placed,
                    state_to_node,
                    node_moving=node_moving,
                    node_placing=node_placing
                )

                all_placed = True
                for state in nodes_placed:
                    if not nodes_placed[state]:
                        all_placed = False
                
                mouse_click_handled = True
            
            self._draw_node_connections(state_to_node, node_moving)
            self._update_nodes()

            if all_placed:
                # Take screenshot here and save as file?
                pass
            
            pygame.display.update()
            self.clock.tick(30)
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        running = False
                    case pygame.MOUSEBUTTONUP:
                        mouse_click_handled = False

        pygame.quit()

class MoveableDiagram(Diagram):
    pass