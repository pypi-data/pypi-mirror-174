class Greedy:
    """
    A python class for the greedy algorithm
    """

    def __init__(self, items: list, capacity: int, by="value", criterion=None) -> None:
        """
        A class of the greedy algorithm
        :param items: a list of tuples (value, weight)
        :param capacity: The maximum weight allowed in a bag
        :param by: one of (value or weight)
        :param criterion: Optional parameter.
        """
        self._items = items
        self._capacity = capacity
        self.criterion = criterion
        self.by = by

        assert by in ["value", "weight"], "Arguments for by should be one of [value, weight]"
        if criterion is not None:
            assert criterion in ["small first", "large first"], "Criterion should be one of [small first, large first]"

            if by == "value":
                if criterion == "small first":
                    self._items.sort(reverse=False, key=lambda t: t[0])
                else:
                    self._items.sort(reverse=True, key=lambda t: t[0])
            else:
                if criterion == "large first":
                    self._items.sort(reverse=True, key=lambda t: t[1])
                else:
                    self._items.sort(reverse=False, key=lambda t: t[1])

    def __repr__(self) -> str:
        """
        A representation of the class
        :return:
        """
        return f"Items: {self.items()}"

    def capacity(self) -> int:
        """
        :return: The capacity of the knapsack
        """
        return self._capacity

    def solve(self) -> dict:
        """
        Provides a solution to the problem using the greedy approach
        :return: a dictionary of the solution
        """
        accumulator = 0  # To hold the current weight in the knapsack
        selected = []  # To hold the items selected by the greedy algorithm

        for item in self.items():
            if accumulator <= self.capacity() and accumulator + item[1] <= self.capacity():
                selected.append(item)
                accumulator += item[1]
            else:
                pass

        total_value = 0

        for item_ in selected:
            total_value += item_[0]

        solution = {
            "Optimal Value": total_value,
            "Selected Items": selected
        }

        return solution

    def items(self) -> None:
        """
        :return: The list of tuples of items in the problem
        """
        return self._items
