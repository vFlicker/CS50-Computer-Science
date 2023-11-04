from enum import Enum


class Operation(Enum):
    """Operations"""

    DELETED = 1
    INSERTED = 2
    SUBSTITUTED = 3

    def __str__(self):
        return str(self.name.lower())


def distances(a, b):
    """Calculate edit distance from a to b"""

    row_length = len(a) + 1
    column_length = len(b) + 1

    # Initialize table
    table = [
        [(0, None) for column in range(column_length)]
        for row in range(row_length)
    ]

    # Base cases
    for row_index in range(1, row_length):
        table[row_index][0] = (row_index, Operation.DELETED)

    for cell_index in range(1, column_length):
        table[0][cell_index] = (cell_index, Operation.INSERTED)

    # Fill the table
    for row_index in range(1, row_length):
        for cell_index in range(1, column_length):
            insertCost, _ = table[row_index][cell_index - 1]
            deleteCost, _ = table[row_index - 1][cell_index]
            substituteCost, _ = table[row_index - 1][cell_index - 1]

            insertCost += 1
            deleteCost += 1

            if a[row_index - 1] != b[cell_index - 1]:
                substituteCost += 1

            minCost = min(insertCost, deleteCost, substituteCost)

            if minCost == insertCost:
                table[row_index][cell_index] = (insertCost, Operation['INSERTED'])
            elif minCost == deleteCost:
                table[row_index][cell_index] = (deleteCost, Operation['DELETED'])
            else:
                table[row_index][cell_index] = (substituteCost, Operation['SUBSTITUTED'])

    return table
