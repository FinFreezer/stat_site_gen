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
		self.block_type = None
		self.tag = None
		self.parts = [ ]

	def __repr__(self):
		return f"Block({self.text}, {self.block_type.value}, {self.tag})"
	
	def get_text(self):
		return self.text
	
	def get_tag(self):
		return self.tag
		
	def block_to_block_type(self):
		if self.text[0] == "#" and self.text[6] != "#":
			self.block_type = BlockType.HEADING
			return self.block_type.value
		
		if self.text.find("```") != -1:
			self.text = self.text.replace("```\n", "```")
			self.block_type = BlockType.CODE
			return self.block_type.value
		
		if self.text[:2] == "> ":
			self.block_type = BlockType.QUOTE
			return self.block_type.value
		
		if self.text[:2] == "- ":
			self.block_type = BlockType.UNORDERED_LIST
			return self.block_type.value

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
				self.block_type = BlockType.ORDERED_LIST
				return self.block_type.value

		self.block_type = BlockType.PARAGRAPH
		self.text = self.text.replace("\n", " ")
		return self.block_type.value
	
	def add_tag(self):
		if self.block_type.value == "quote":
			self.text = self.text.replace("> ", "")
			self.text = self.text.replace("\n", " ")
			self.text = (f"<p>{self.text}</p>")
			self.tag = "blockquote"
			return 

		if self.block_type.value == "unordered_list":
			self.helper_add_list_tags_ul()
			self.tag = "ul"
			return

		if self.block_type.value == "ordered_list":
			self.helper_add_list_tags_ol()
			self.tag = "ol"
			return

		if self.block_type.value == "code":
			self.tag = "code"
			return
		
		if self.block_type.value == "heading":
			num_heading = self.helper_count_repeating_instances("#")
			replace = ""
			for i in range(num_heading):
				replace += "#"
			self.text = self.text.replace(replace, "", 1)
			self.text = self.text[1:]
			self.tag = f"h{num_heading}"
			return
		
		if self.block_type.value == "paragraph":
			self.tag = "p"
			return
		
		return

	def helper_count_repeating_instances(self, instance):
		num_instances = 0
		start = self.text.find(instance)
		if start != -1:
			num_instances += 1
			while self.text[start + num_instances] == instance:
				num_instances += 1
		return num_instances
		
	def helper_add_list_tags_ul(self):
		self.text = self.text.replace("- ", "")
		parts = self.text.split("\n")
		wrapped_parts = []
		for part in parts:
			wrapped_parts.append(f"<li>{part}</li>")
		self.text = "\n".join(wrapped_parts)
		self.text = self.text.replace("\n", "")
		return

	def helper_add_list_tags_ol(self):
		parts = self.text.split("\n")
		fixed_parts = []
		
		for part in parts:
			index = 0
			for char in part:
				if char.isdigit():
					index += 1
				else:
					fixed_parts.append(part[index+2:])
					break

		wrapped_parts = []
		for part in fixed_parts:
			wrapped_parts.append(f"<li>{part}</li>")
		self.text = "\n".join(wrapped_parts)
		self.text = self.text.replace("\n", "")
		return

	def to_html(self):
		if self.tag == "code":
			full_html = f"<pre>"
		else:
			full_html = f"<{self.tag}>"

		for part in self.parts:
			full_html += part.to_html()

		if self.tag == "code":
			return full_html + f"</pre>"
		else:
			return full_html + f"</{self.tag}>"