from googlesearch import search
import bs4 as bs

query = 'geeksforgeeks'

resp = search(query, tld="com", num=10, stop=5, pause=2)

for i in resp:
    print(i)