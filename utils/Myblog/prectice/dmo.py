import re
txt = '''ad  hla   hfh  qhwf
asic   haiwc
askb   lbwcfoq
awkdjqwjic
aSKjcwqichias
asc'''
# count = 0
# for index, line in enumerate(txt):
#     count += 1
# print(count)
# # a = txt.split(" ")[0]
# # print(a)
# a = txt.split("\n")
# print(a)
# c = len(a)
# print(c)
d = 0
for i in txt:
    # print(i, end="")
    if i == "\n":
        d += 1
if txt[-1] != "\n":
    d+=1
print(d)

f = len(txt.splitlines(keepends=False))
h = txt.splitlines(keepends=False)
print(f)
for eachLine in h:
    print(re.split(r"\s\s+|\t", eachLine))






