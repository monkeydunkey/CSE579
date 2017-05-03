import os
import sys

DIR = os.getcwd()
TMP_DIR = "output2"
KB_DIR = "KB"
filename = sys.argv[1]
queryTerms = [x.strip() for x in sys.argv[2].split(';')]

filePath = os.path.join(DIR, filename)
print DIR +filename
fileRulePath = os.path.join(DIR, KB_DIR, "ReducedRuleFiles", filename.replace('.db.mln', '').replace("output2/", ""))

ruleType = {'uses': 0, 'outputs': 1, 'solves': 2}
ruleTypeRev = ['uses', 'outputs', 'solves']
ruleFile = open(fileRulePath)
paperRules = ruleFile.readlines()
paperRule = [x.split(' | ')[1:] for x in paperRules]

ruleToWrite = []
for i, queryTerm in enumerate(queryTerms):
    if queryTerm.strip() == "":
        continue
    terms = [x.strip() for x in queryTerm.split(',')]
    ruleOfImp = filter(lambda y: ruleType[y[0].strip()]==i, paperRule)
    for term in terms:
        if any(term in x[1] for x in ruleOfImp):
            ruleToWrite.append('paper'+ ruleTypeRev[i] +'(P'+ filename.replace('.db.mln', '').replace("output2/", "").replace('.', '_') + ',"' + term + '"), 1\n')

fileToEdit = open(filePath, 'a')
fileToEdit.writelines(ruleToWrite)
