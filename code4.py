# extracts all links -> includes | and - 
import bz2 
import re 
import xml.etree.ElementTree as ET
from collections import defaultdict


start = '<page>'
stop = '</page>'

G = defaultdict(list)

def get_links(node): 
    outlinks = []
    direct_links = []
    for ch in node: 
        #if ch.tag == 'redirect': 
        #    outlinks.append(ch.attrib['title'])
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

#27000

def rem_bracket(ss): 
    s = ''
    for x in ss:
        if x != '[' and x != ']':
            s += x
    return s


pages = []
ct = 0 
page = ''
for line in  bz2.open('wiki1.bz2',mode = 'rt', encoding = 'utf-8'):
    if ct > 10: break
    text = line.rstrip('\n')
    #print(text)
    if start in text: page = '' + start;ct += 1; print(ct); continue
    if stop in text: page += stop ;pages.append(page); page = ''
    page += text
    #print(ct)
    #ct += 1

#print(pages)

ct_page = 0
for page in pages:
    ct_page += 1; print('page', ct_page)
    root = ET.fromstring(page)
    page_links = get_links(root)
    G[root[0].text] = page_links

print(G)


# with open("adjacency.txt", 'w','utf-8') as f: 
#     for key, value in G.items(): 
#         f.write('%s:%s\n' % (key, value))






