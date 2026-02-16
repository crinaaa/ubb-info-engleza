class GameRepository:
    def __init__(self, filename="savegame.txt"):
        self._filename = filename

    def save(self, board_matrix):
        """Saves the 6x6 matrix to a file."""
        with open(self._filename, "w") as f:
            for row in board_matrix:
                # Store as comma-separated integers
                f.write(",".join(map(str, row)) + "\n")

    def load(self):
        """Reads the file and returns a 2D list."""
        matrix = []
        try:
            with open(self._filename, "r") as f:
                for line in f:
                    row = [int(x) for x in line.strip().split(",")]
                    matrix.append(row)
            return matrix
        except FileNotFoundError:
            return None