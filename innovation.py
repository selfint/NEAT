# innovation.py
# Description : Innovation object, represents connections between nodes.
# ----------------------------------------------------------------------

class Innovation:

	def __init__(self, number: int, src_number: int, dst_number: int, weight: float, enabled: bool, forward: bool):
		super(Innovation, self).__init__()
		self.number = None if number == -1 else number
		self.src_number = None if src_number == -1 else src_number
		self.dst_number = None if dst_number == -1 else dst_number
		self.weight = weight
		self.enabled = enabled
		self.forward = forward

	def __repr__(self) -> str:
		string = "Innovation {}: ({} -> {}) {}"
		return string.format(self.number, self.src_number, self.dst_number,
							 "Enabled" * self.enabled or "Disabled")


if __name__ == '__main__':
	print("Testing Innovation")
	test_innovation = Innovation(number=0, src_number=1, dst_number=4, weight=1.3, enabled=True, forward=True)

	# Test repr function
	print(test_innovation)
