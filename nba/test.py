from data import data
from markdown import markdown
D = data()
M = markdown()
print(D.schedule())

print(M.schedule(D.schedule()))