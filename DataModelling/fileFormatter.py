#The aim of this file is to create a nice cleaned version of the research papers so that the openie
#information extractor works better.
'''
openie command:
sbt "runMain edu.knowitall.openie.OpenIECli --input-file /Users/shashankbhushan/Documents/Github/cse579/DataModelling/PixelRecurrentNeuralNetworks_formatted_reduced.txt --ouput-file /Users/shashankbhushan/Documents/Github/cse579/DataModelling/PixelInformationExtraction_test.txt"
'''
import re
import os
import time

def process_paragraph(para):
    para = para.replace('\n', ' ').replace('- ', '')
    return (removingFigureDef(para))

def removingFigureDef(line):
    patt = "Figure \d+\..*?\."
    return re.sub(patt,'', line)

def lineFilter(line):
    line = line.lower()
    interestingLines = [' we ', ' our ']
    startingTerms = ['we', 'our']
    if len(line) < 3:
        return False
    return any(line.startswith(startingTerm) for startingTerm in startingTerms) or any(interestingTerm in line for interestingTerm in interestingLines)



#We need to reorder paragraphs if it is detected that the consecutive para in the list is not logically consecutive
def reOrderParagraphs(paragraphs):
    for i in range(len(paragraphs)):
        #Basically if the paragraph change without line change
        #Find more instance where there was no paragraph change but the text was represented as such
        if (paragraphs[i].endswith('-')) and i < len(paragraphs) - 1:
            for j in range(i+1, len(paragraphs)):
                if len(paragraphs[j]) > 0 and paragraphs[j][0].islower():
                    paragraphs.insert(i+1, paragraphs[j])
                    del paragraphs[j+1]
                    break
    return paragraphs

DIR = "/Users/shashankbhushan/Documents/Github/cse579"
inFolder = "DataGrabber/data/txt"
outFolder = "DataModelling/FormattedFiles"
folders = os.listdir(os.path.join(DIR, inFolder))
for j,dire in enumerate(folders):
    files = os.listdir(os.path.join(DIR, inFolder, dire))
    for i,f in enumerate(files):
        print 'Formatting file', f
        input_file_path = os.path.join(DIR, inFolder, dire, f)
        output_file_path = os.path.join(DIR, outFolder,f)
        inFile = open(input_file_path)
        fileData = inFile.read()
        paragraphs = map(process_paragraph, filter(lambda x: len(x.split(' ')) > 4, fileData.split('\n\n')))
        reOrderP = reOrderParagraphs(paragraphs)
        totalText = (' '.join(reOrderP)).replace('- ', '')
        #Filtering out small and useless lines
        formattedLines = '.\n'.join(filter(lineFilter , totalText.split('. ')))
        outFile = open(output_file_path, 'w')
        #Considering only those lines whose length is more than 4
        outFile.writelines(formattedLines)
        outFile.close()
        time.sleep(0.01) # silly way for allowing for ctrl+c termination
