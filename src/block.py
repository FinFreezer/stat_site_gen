from enum import Enum

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered_list"
	ORDERED_LIST = "ordered_list"

class Block():
	def __init__(self, text):
		self.text = text
		self.block_type = BlockType
	
	def block_to_block_type(self):
		if self.text[0] == "#" and self.text[6] != "#":
			self.block_type = "heading"
			return self.block_type
		
		if self.text[:4] == "```\n":
			self.block_type = "code"
			return self.block_type
		
		if self.text[:2] == "> ":
			self.block_type = "quote"
			return self.block_type
		
		if self.text[:2] == "- ":
			self.block_type = "unordered_list"
			return self.block_type

		if self.text[0].isdigit() and self.text[1:3] == ". ":
			lines = self.text.split("\n")
			bad_format_flag = False
			initial_index = int(self.text[0])
			for i in range(len(lines)):
				if int(lines[i][0]) == initial_index:
					initial_index += 1
					continue
				else:
					bad_format_flag = True

			if not bad_format_flag:
				self.block_type = "ordered_list"
				return self.block_type

		self.block_type = "paragraph"
		return self.block_type