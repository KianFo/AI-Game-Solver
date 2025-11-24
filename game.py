class Game:
    def __init__(self, game_map_string):
        self.game_map = []
        lines = game_map_string.split('\n')
        for i in range(len(lines)):
            line = [cell.split("/") for cell in lines[i].strip().split()]
            self.game_map.append(line)
            
        self.height = len(self.game_map)
        self.width = len(self.game_map[0])
        number_of_boxes = game_map_string.count('B')
        number_of_portals = game_map_string.count('P')
        self.boxes = [0] * number_of_boxes
        self.goals = [0] * number_of_boxes
        self.portals = [[] for _ in range(number_of_portals // 2)]
        self.map_size = len(lines)
        self.num_boxes = number_of_boxes
        self.most_left_accessible_column = self.width
        self.most_right_accessible_column = 0
        self.most_top_accessible_row = self.height
        self.most_bottom_accessible_row = 0
        
        for i in range(len(self.game_map)):
            for j in range(len(self.game_map[i])):
                static_element = '.'
                for k in range(len(self.game_map[i][j])):
                    if self.game_map[i][j][k][0] == 'H':
                        self.player_pos = (i, j)
                    elif self.game_map[i][j][k][0] == 'B':
                        idx = int(self.game_map[i][j][k][1:]) - 1
                        self.boxes[idx] = (i, j)
                    elif self.game_map[i][j][k][0] == 'G':
                        idx = int(self.game_map[i][j][k][1:]) - 1
                        self.goals[idx] = (i, j)
                        static_element = self.game_map[i][j][k]
                    elif self.game_map[i][j][k][0] == 'P':
                        idx = int(self.game_map[i][j][k][1:]) - 1
                        self.portals[idx].append((i, j))
                        static_element = self.game_map[i][j][k]
                    elif self.game_map[i][j][k][0] == 'W':
                        static_element = 'W'
                        
                # we only save the static element in the map array for optimization
                self.game_map[i][j] = static_element  
        
    def set_player_position(self, pos):
        self.player_pos = pos
    
    def set_box_positions(self, boxes):
        self.boxes = [box for box in boxes]
        
    def get_map_size(self):
        return [self.height, self.width]

    def get_box_locations(self):
        return [box for box in self.boxes]
    
    def get_goal_locations(self):
        return [goal for goal in self.goals]
    
    def get_portal_locations(self):
        return self.portals
    
    def get_player_position(self):
        return self.player_pos
    
    def is_wall(self, pos):
        return self.__is_pos_out_of_bounds(pos)
    
    # It's time consuming
    def get_elements_in_position(self, pos):
        if self.__is_pos_out_of_bounds(pos):
            return ["W"]
        elements = []
        if self.game_map[pos[0]][pos[1]] != '.':
            elements.append(self.game_map[pos[0]][pos[1]])
        for i in range(len(self.boxes)):
            if self.boxes[i] == pos:
                elements.append(f'B{i + 1}')
        if self.player_pos == pos:
            elements.append('H')
        if len(elements) == 0:
            elements.append('.')
        return elements

    # It's time consuming
    def get_map(self):
        game_map_copy = [[[cell] for cell in row] for row in self.game_map]
        for i in range(len(self.boxes)):
            box = self.boxes[i]
            game_map_copy[box[0]][box[1]].append(f'B{i + 1}')
        game_map_copy[self.player_pos[0]][self.player_pos[1]].append('H')
        
        result = []
        for i in range(len(game_map_copy)):
            row = []
            for j in range(len(game_map_copy[i])):
                cell = game_map_copy[i][j]
                if len(cell) > 1 and cell[0] == '.':
                    cell = cell[1:]
                row.append('/'.join(cell))
            result.append('\t'.join(row))
        return '\n'.join(result) 
    
    def display_map(self):
        print(self.get_map())   
                      
    def apply_move(self, direction):
        direction_map = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
        direction = direction_map[direction]
        human_new_pos = self.__calculate_new_pos(self.player_pos, direction)
        
        if self.__is_pos_out_of_bounds(human_new_pos):
            return False
        
        box_id = self.__get_element_id_in_cell(human_new_pos, 'B')
        if box_id is not None:
            box_new_pos = self.__calculate_new_pos(self.boxes[box_id - 1], direction)
            if not self.__validate_box_new_pos(box_new_pos):
                return False
            self.boxes[box_id - 1] = box_new_pos
        self.player_pos = human_new_pos
        return True
        
    def apply_moves(self, moves):
        try:
            for move in moves:
                self.apply_move(move)  # Raises ValueError on invalid move
            return True  # All moves succeeded
        except ValueError:
            return False  # At least one move failed
    

    def is_move_valid(self, direction):
        """
        Check if a move is valid without changing the game state.
        :param direction: A string representing the direction ('U', 'D', 'L', 'R').
        :return: True if the move is valid, False otherwise.
        """
        direction_map = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
        
        # Handle input as a single string (not a list)
        if isinstance(direction, list):
            direction = direction[0]
            
        try:
            direction_vector = direction_map[direction]
        except KeyError:
            return False  # Invalid direction

        # Calculate new player position (with portal handling)
        human_new_pos = self.__calculate_new_pos(self.player_pos, direction_vector)
        
        # Check if new position is out of bounds or a wall
        if self.__is_pos_out_of_bounds(human_new_pos):
            return False
        
        # Check if there's a box at the new player position
        box_id = self.__get_element_id_in_cell(human_new_pos, 'B')
        
        if box_id is not None:
            # Calculate new box position (with portal handling)
            box_current_pos = self.boxes[box_id - 1]
            box_new_pos = self.__calculate_new_pos(box_current_pos, direction_vector)
            
            # Validate box's new position
            if not self.__validate_box_new_pos(box_new_pos):
                return False
        
        return True

    def reset_state(self, current_state):
        """
        Reset the game state to a specific configuration.
        :param current_state: Tuple of (player_pos, boxes_positions)
                            Example: ((3,3), [(1,3), (3,1), (5,3), (3,5)])
        """
        player_pos, boxes = current_state
        
        # Reset player position
        self.player_pos = player_pos
        
        # Reset box positions (make sure they're in the same order as initial boxes)
        for i in range(len(boxes)):
            if i < len(self.boxes):  # Ensure we don't exceed original box count
                self.boxes[i] = boxes[i]
        
    def is_game_won(self):
        for i in range(len(self.boxes)):
            if self.boxes[i] != self.goals[i]:
                return False
        return True
    
    def is_solution_valid(self, solution):
        self.apply_moves(solution)
        return self.is_game_won()
        
    def __calculate_new_pos(self, current_pos, direction):
        dy, dx = direction
        new_pos = (current_pos[0] + dy, current_pos[1] + dx)
        portal_id = self.__get_element_id_in_cell(new_pos, 'P')
        if portal_id is not None:
            portal_idx = portal_id - 1
            if new_pos == self.portals[portal_idx][0]:
                return (self.portals[portal_idx][1][0] + dy, self.portals[portal_idx][1][1] + dx)
            return (self.portals[portal_idx][0][0] + dy, self.portals[portal_idx][0][1] + dx)
        return new_pos
            
    def __is_pos_out_of_bounds(self, pos):
        return (pos[0] < 0 or pos[0] >= self.height or 
                pos[1] < 0 or pos[1] >= self.width or 
                self.game_map[pos[0]][pos[1]][0] == 'W')
    
    def __validate_box_new_pos(self, pos):
        if self.__is_pos_out_of_bounds(pos) or self.__get_element_id_in_cell(pos, 'B') is not None:
            return False
        return True
    
    def __get_element_id_in_cell(self, pos, element):
        if pos[0] < 0 or pos[0] >= self.height or pos[1] < 0 or pos[1] >= self.width:
            return None
        if element == "B":
            for i in range(len(self.boxes)):
                if self.boxes[i] == pos:
                    return i + 1
        if element == self.game_map[pos[0]][pos[1]][0]:
            return int(self.game_map[pos[0]][pos[1]][1:])
        return None                