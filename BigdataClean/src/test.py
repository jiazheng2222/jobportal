import re

str = "0 | 0"

print re.split(r"\|", str)[1]