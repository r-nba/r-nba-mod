from data import data
from markdown import markdown
from pprint import pprint
D = data()
M = markdown()
pprint(D.playoffs())
print(M.playoffs(D.playoffs()))
