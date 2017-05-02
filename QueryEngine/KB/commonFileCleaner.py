import re
kb = open('CommonKB.txt')
kb_filtered = open('CommonKBFiltered.txt', 'w')
patt = re.compile('[^\x00-\x7F]')
ruleEncountered = set()
for line in kb.readlines():
    if patt.search(line) is None:
        ll = line.replace('http://', '').replace('https://', '').replace('nodeID://', '')
        ll = 'isa("' + ll.split(' , ')[0].split('(')[1].strip() + '","' + ll.split(' , ')[1].split(')')[0].strip() + '")\n'
        if ll not in ruleEncountered:
            kb_filtered.write(ll)
            ruleEncountered.add(ll)

kb_filtered.close()
kb.close()
