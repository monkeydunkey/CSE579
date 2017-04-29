import re
kb = open('CommonKB_archive.txt')
kb_filtered = open('CommonKBFiltered.txt', 'w')
patt = re.compile('[^\x00-\x7F]')
for line in kb.readlines():
    if patt.search(line) is None:
        ll = line.replace('http://', '').replace('https://', '').replace('nodeID://', '')
        ll = 'isa("' + ll.split(' , ')[0].split('(')[1].strip() + '","' + ll.split(' , ')[1].split(')')[0].strip() + '")\n'
        kb_filtered.write(ll)

kb_filtered.close()
kb.close()
