import re

# string = '## 1. 简介'
# pattern = r"^#+\s+(.+)$"

# string = "<a name='1'></a>"
# string = '<a name="2"></a>'
string = '   <a   name="2">  </a>'

pattern = r"^\s*<a\s+name=[\"|\'](.+?)[\"|\']>.*</a>"

results = re.findall(pattern, string)
print(results)