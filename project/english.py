import re
s = "a№sdf , adf6:-sadf, s45  fjklfj:-dsflk511 fakldfэkf ff   jj  j   ;ljkjj%!!("

words = s.split(" ")
# for word in words:

pattern ="\w+\S*\w+"

res = re.findall("\w+\S*\w+", s)

print(s)
print(words)
print(res)
