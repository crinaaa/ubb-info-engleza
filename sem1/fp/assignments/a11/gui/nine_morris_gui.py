import pygame
from domain.board import Board
from domain.player import Player
from service.game_service import GameService
from start_game.minmax import MinimaxAI
from exceptions.exception_module import RemovalException


class NineMensMorrisGUI:
    WIDTH, HEIGHT = 800, 800
    RADIUS = 16

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Nine Men's Morris")

        self.font = pygame.font.SysFont(None, 30)
        self.small_font = pygame.font.SysFont(None, 24)

        self.board = Board()
        self.human = Player("Human", "X")
        self.computer = Player("Computer", "0")
        self.game_service = GameService(self.human, self.computer, self.board)
        self.ai = MinimaxAI(self.board, "0", "X")

        self.selected = None
        self.removal_mode = False
        self.message = "Placement phase: place a piece"
        self.phase2_announced = False

        self.positions = self._compute_positions()

        self.exit_button = pygame.Rect(self.WIDTH - 160, 20, 140, 40)

    # board positions

    def _compute_positions(self):
        base = 150
        size = 500
        o1 = size // 6
        o2 = size // 3

        return {
            0: (base, base), 1: (base + size // 2, base), 2: (base + size, base),
            3: (base + o1, base + o1), 4: (base + size // 2, base + o1), 5: (base + size - o1, base + o1),
            6: (base + o2, base + o2), 7: (base + size // 2, base + o2), 8: (base + size - o2, base + o2),
            9: (base, base + size // 2), 10: (base + o1, base + size // 2), 11: (base + o2, base + size // 2),
            12: (base + size - o2, base + size // 2), 13: (base + size - o1, base + size // 2), 14: (base + size, base + size // 2),
            15: (base + o2, base + size - o2), 16: (base + size // 2, base + size - o2), 17: (base + size - o2, base + size - o2),
            18: (base + o1, base + size - o1), 19: (base + size // 2, base + size - o1), 20: (base + size - o1, base + size - o1),
            21: (base, base + size), 22: (base + size // 2, base + size), 23: (base + size, base + size),
        }

    # draw the pieces

    def draw(self):
        self.screen.fill((240, 217, 181))
        self._draw_board()
        self._draw_pieces()
        self._draw_message()
        self._draw_exit_button()
        pygame.display.flip()

    def _draw_board(self):
        base = 150
        size = 500
        o1 = size // 6
        o2 = size // 3

        pygame.draw.rect(self.screen, (0, 0, 0), (base, base, size, size), 3)
        pygame.draw.rect(self.screen, (0, 0, 0), (base + o1, base + o1, size - 2 * o1, size - 2 * o1), 3)
        pygame.draw.rect(self.screen, (0, 0, 0), (base + o2, base + o2, size - 2 * o2, size - 2 * o2), 3)

        pygame.draw.line(self.screen, (0, 0, 0), (base + size // 2, base), (base + size // 2, base + o2), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (base + size // 2, base + size - o2), (base + size // 2, base + size), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (base, base + size // 2), (base + o2, base + size // 2), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (base + size - o2, base + size // 2), (base + size, base + size // 2), 3)

    def _draw_pieces(self):
        for i, (x, y) in self.positions.items():
            symbol = self.board.get_symbol(i)
            if symbol == "X":
                pygame.draw.circle(self.screen, (200, 0, 0), (x, y), self.RADIUS)
            elif symbol == "0":
                pygame.draw.circle(self.screen, (0, 0, 200), (x, y), self.RADIUS)
            else:
                pygame.draw.circle(self.screen, (0, 0, 0), (x, y), 4)

            if self.selected == i:
                pygame.draw.circle(self.screen, (255, 215, 0), (x, y), self.RADIUS + 6, 2)

    def _draw_message(self):
        text = self.font.render(self.message, True, (0, 0, 0))
        self.screen.blit(text, (50, 50))

    def _draw_exit_button(self):
        pygame.draw.rect(self.screen, (180, 80, 80), self.exit_button, border_radius=6)
        text = self.small_font.render("Exit Game", True, (255, 255, 255))
        self.screen.blit(
            text,
            (self.exit_button.centerx - text.get_width() // 2,
             self.exit_button.centery - text.get_height() // 2)
        )

    #input (as clicks)

    def get_clicked_pos(self, mouse):
        for i, (x, y) in self.positions.items():
            if (mouse[0] - x) ** 2 + (mouse[1] - y) ** 2 < 20 ** 2:
                return i
        return None

    #game itself

    def human_turn(self, pos):
        try:
            state = self.game_service.get_game_state()

            if state["phase"] == 1:
                self.game_service.place_piece(pos)
                self.message = f"You placed at {pos}"
            else:
                if self.selected is None:
                    if self.board.get_symbol(pos) != "X":
                        self.message = "That is not your piece."
                        return
                    self.selected = pos
                    self.message = f"Selected {pos}"
                    return
                else:
                    self.game_service.move_piece(self.selected, pos)
                    self.message = f"You moved {self.selected} → {pos}"
                    self.selected = None

        except RemovalException:
            self.removal_mode = True
            self.message = "Mill formed! Remove a computer piece."
            return
        except Exception as e:
            self.message = str(e)
            self.selected = None
            return

        self._check_phase2()

    def _check_phase2(self):
        state = self.game_service.get_game_state()
        if state["phase"] == 2 and not self.phase2_announced:
            self.phase2_announced = True
            self.message = "Phase 2 started: movement phase!"

    def computer_turn(self):
        try:
            state = self.game_service.get_game_state()
            if state["phase"] == 1:
                pos = self.ai.get_placement_move()[0]
                self.game_service.place_piece(pos)
                self.message = f"Computer placed at {pos}"
            else:
                frm, to = self.ai.get_move(self.computer.is_flying())
                self.game_service.move_piece(frm, to)
                self.message = f"Computer moved {frm} → {to}"

        except RemovalException:
            pos = self.ai.get_removal_move()
            self.game_service.remove_opponent_piece(pos)
            self.game_service.clear_mill_state()
            self.message += f" and removed your piece at {pos}"


    #main loop

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.exit_button.collidepoint(event.pos):
                        pygame.quit()
                        return

                    pos = self.get_clicked_pos(event.pos)
                    if pos is None:
                        continue

                    if self.removal_mode:
                        if self.board.get_symbol(pos) == "0":
                            self.game_service.remove_opponent_piece(pos)
                            self.game_service.clear_mill_state()
                            self.removal_mode = False
                            self.message = "Piece removed."
                        else:
                            self.message = "You must remove a computer piece."
                        continue

                    if self.game_service.get_game_state()["current_player"] == self.human:
                        self.human_turn(pos)

            state = self.game_service.get_game_state()
            if not state["game_over"] and state["current_player"] == self.computer:
                pygame.time.delay(500)
                self.computer_turn()

            self.draw()
            clock.tick(60)

        pygame.quit()
