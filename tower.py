from glob import GlobalState


class Tower:

    def __init__(self):
        self._blocks = []

    @property
    def size(self):
        return len(self._blocks)

    def is_empty(self):
        return True if self.size == 0 else False

    def __len__(self):
        return len(self._blocks)

    def __getitem__(self, index):
        return self._blocks[index]

    def __setitem__(self, index, value):
        self._blocks[index] = value

    def push(self, value):
        self._blocks.append(value)
        GlobalState().score += 1

    def pop(self):
        self._blocks.pop(0)

    @property
    def sustainable(self):
        tower_height = len(self)
        if GlobalState().falling or tower_height < 2:
            return True

        width = self._blocks[0].rect.right - self._blocks[0].rect.left
        counter = 1
        sum_center = self._blocks[-1].rect.centerx
        for i in range(tower_height - 2, -1, -1):  # up -> down
            block_x = self._blocks[i].rect.centerx
            if abs(block_x - sum_center) > width / 2:
                return False

            sum_center = (block_x + counter * sum_center) / (counter + 1)
            counter += 1
        return True
