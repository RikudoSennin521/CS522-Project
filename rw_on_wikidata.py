# ROHAN KUMAR 
# 2020MCB1247 

# Importing all the libraries
import bz2 
import re 
import xml.etree.ElementTree as ET
from collections import defaultdict
import random

# We divide the XML data into pages using start and stop defined by us
start = '<page>'
stop = '</page>'

# This is going to be our WikiGraph as an adjacency list
G = defaultdict(list)


# Function to remove brackets from a string
def rem_bracket(ss): 
    s = ''
    for x in ss:
        if x != '[' and x != ']':
            s += x
    return s


# Function to extract desired links from a single webpage (using RegEx and ElementTree)
def get_links(node): 
    outlinks = []
    direct_links = []
    for ch in node: 
        if ch.tag == 'revision':
            for gch in ch:
                if gch.tag == 'text': 
                    link_text = gch.text
                    direct_links_brackets = re.findall(r'\[[- |\w]*?\]', link_text)
                    direct_links = [rem_bracket(x) for x in direct_links_brackets]
    outlinks = outlinks + direct_links
    for i in range(len(outlinks)):
        if '|' in outlinks[i]: 
            splits = list(outlinks[i].split('|'))
            outlinks[i] = splits[0]
    return outlinks


# Function to take a random walk on the given graph 
def random_walk(G): 
    freq = defaultdict(int)
    start = random.choices(list(G.keys()),k = 1)[0]
    cur = start
    steps = 0 
    while(steps < 100000):
        freq[cur] += 1
        if len(G[cur]) != 0:
            next = random.choices(G[cur],k = 1)[0]
        else:
            next = random.choices(list(G.keys()),k = 1)[0]
        cur = next
        steps += 1
        if steps%10000 == 0:
            print('steps',steps)
    return freq



# Reading the wikidata bz2 file line by line. 
pages = []
ct = 0 
page = ''
for line in  bz2.open('wiki1.bz2',mode = 'rt', encoding = 'utf-8'):
    text = line.rstrip('\n')

    # Splitting the XML file at each page
    if start in text: page = '' + start;ct += 1; continue
    if stop in text: page += stop ;pages.append(page); page = ''
    page += text
    

# Extracting links from each page. We convert the page to an element tree. Then links are read using RegEx
ct_page = 0
for page in pages:
    ct_page += 1; 
    root = ET.fromstring(page)
    page_links = get_links(root)

    # Adding the links to our graph 
    G[root[0].text] = page_links


# Calling the Random Walk Function on our WikiGraph 
rw = random_walk(G)

# Printing the top 15 most frequently visited webpages
print(sorted(rw.items(), key=lambda x:-x[1])[:15])

