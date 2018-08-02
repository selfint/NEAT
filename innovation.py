# innovation.py
# Description : Innovation object, represents connections between nodes.
# ----------------------------------------------------------------------
from typing import Union


class Innovation:

    def __init__(self, number: Union[int, None], src_number: Union[int, None], dst_number: Union[int, None],
                 weight: float, enabled: bool, forward: bool):
        super(Innovation, self).__init__()
        self.number = number
        self.src_number = src_number
        self.dst_number = dst_number
        self.weight = weight
        self.enabled = enabled
        self.forward = forward

    def __str__(self) -> str:
        string = "Innovation {}: ({} -> {}) {}"
        return string.format(self.number, self.src_number, self.dst_number,
                             "Enabled" * self.enabled or "Disabled")

    def __repr__(self) -> str:
        return str(self)

if __name__ == '__main__':
    print("Testing Innovation")
    test_innovation = Innovation(number=0, src_number=1, dst_number=4, weight=1.3, enabled=True, forward=True)

    # Test repr function
    print(test_innovation)
