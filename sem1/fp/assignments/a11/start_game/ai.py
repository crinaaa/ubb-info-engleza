# import random
# from typing import List, Tuple, Optional
#
#
# class MinimaxAI:
#     def __init__(self, board, symbol, opponent_symbol):
#         self.board = board
#         self.symbol = symbol
#         self.opponent_symbol = opponent_symbol
#
#     def get_all_empty_positions(self) -> List[int]:
#         """Get all empty positions on the board"""
#         empty_positions = []
#         for i in range(24):
#             if self.board.is_position_empty(i):
#                 empty_positions.append(i)
#         return empty_positions
#
#     def get_ai_pieces_positions(self) -> List[int]:
#         """Get all positions occupied by the computer player"""
#         ai_positions = []
#         for i in range(24):
#             if self.board.get_symbol(i) == self.symbol:
#                 ai_positions.append(i)
#         return ai_positions
#
#     def get_placement_move(self) -> int:
#         """Get computer placement move during Phase 1"""
#         empty_positions = self.get_all_empty_positions()
#
#         # strategy 1: try to form a mill
#         for pos in empty_positions:
#             # check if placing here would complete a mill
#             if self._would_form_mill(pos, self.symbol):
#                 return pos
#
#         # strategy 2: try to block opponent from forming mill
#         for pos in empty_positions:
#             if self._would_form_mill(pos, self.opponent_symbol):
#                 return pos
#
#         # strategy 3: place in strategic positions (intersections)
#         strategic_positions = [4, 10, 13, 19]  # center positions
#         for pos in strategic_positions:
#             if pos in empty_positions:
#                 return pos
#
#         # strategy 4: Random placement
#         return random.choice(empty_positions)
#
#     def get_move(self, can_fly: bool = False) -> Tuple[int, int]:
#         """Get computer move during Phases 2/3"""
#         ai_positions = self.get_ai_pieces_positions()
#
#         # strategy 1: try to form a mill
#         for from_pos in ai_positions:
#             possible_moves = self._get_possible_moves(from_pos, can_fly)
#             for to_pos in possible_moves:
#                 if self._would_form_mill(to_pos, self.symbol):
#                     return from_pos, to_pos
#
#         # strategy 2: block opponent mills
#         for from_pos in ai_positions:
#             possible_moves = self._get_possible_moves(from_pos, can_fly)
#             for to_pos in possible_moves:
#                 # check if moving here would block opponent
#                 self.board.place_piece(to_pos, self.symbol)
#                 self.board.remove_piece(from_pos)
#
#                 # check if this blocks opponent mill formation
#                 blocks = False
#                 for i in range(24):
#                     if self.board.is_position_empty(i):
#                         if self._would_form_mill(i, self.opponent_symbol):
#                             blocks = True
#                             break
#
#                 # undo move
#                 self.board.remove_piece(to_pos)
#                 self.board.place_piece(from_pos, self.symbol)
#
#                 if blocks:
#                     return from_pos, to_pos
#
#         # strategy 3: move randomly but legally
#         random.shuffle(ai_positions)
#         for from_pos in ai_positions:
#             possible_moves = self._get_possible_moves(from_pos, can_fly)
#             if possible_moves:
#                 return from_pos, random.choice(possible_moves)
#
#         # fallback (shouldn't reach here if game is valid)
#         return ai_positions[0], ai_positions[0]
#
#     def get_removal_move(self) -> int:
#         """Get position to remove opponent piece"""
#         opponent_positions = []
#         for i in range(24):
#             if self.board.get_symbol(i) == self.opponent_symbol:
#                 opponent_positions.append(i)
#
#         # strategy 1: remove from opponent's mill if possible
#         # strategy 2: prefer non-mill pieces
#         non_mill_positions = []
#         for pos in opponent_positions:
#             if not self.board.part_of_mill(pos, self.opponent_symbol):
#                 non_mill_positions.append(pos)
#
#         if non_mill_positions:
#             return random.choice(non_mill_positions)
#
#         # if all pieces are in mills, remove any
#         return random.choice(opponent_positions)
#
#     def _would_form_mill(self, position: int, symbol: str) -> bool:
#         """Check if placing symbol at position would form a mill"""
#         # temporarily place the piece
#         original = self.board.get_symbol(position)
#         self.board.place_piece(position, symbol)
#
#         # check for mill
#         forms_mill = self.board.check_mill(position, symbol)
#
#         # restore original state
#         if original == " ":
#             self.board.remove_piece(position)
#         else:
#             self.board.place_piece(position, original)
#
#         return forms_mill
#
#     def _get_possible_moves(self, from_pos: int, can_fly: bool) -> List[int]:
#         """Get all possible moves from a position"""
#         possible_moves = []
#
#         if can_fly:
#             # flying: can move to any empty position
#             for i in range(24):
#                 if self.board.is_position_empty(i):
#                     possible_moves.append(i)
#         else:
#             # normal movement: only adjacent positions
#             adjacent = self.board.get_adjacent_positions(from_pos)
#             for pos in adjacent:
#                 if self.board.is_position_empty(pos):
#                     possible_moves.append(pos)
#
#         return possible_moves