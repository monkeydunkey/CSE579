# Information Extraction

The aim of the Data Modelling module is to parse the texts obtained from the Data Grabber module and create 'Ground Truth' terms which would be used for MLN training. 

## Current Status
Right now I am trying to extract the Ground Truth terms from a single paper - "PixelRecurrentNeuralNetworks.pdf".
There are 3 relations that are extracted from the paper
1. Outputs: This describes what this the output of the paper as in the system it describes or the results it produces
2. Uses: This describes the tools and methods used in the paper
3. Solves: This describes the aim of the paper or the problem it is trying to solve

The file [PixelInformationExtraction_last.txt](https://github.com/monkeydunkey/CSE579/blob/master/DataModelling/PixelInformationExtraction_last.txt) contains the list of the above described relations found in the paper

## Process
1. Clean the text obtained from the pdf-to-text conversion (fileFormatter.py). Input file can be found [here](https://github.com/monkeydunkey/CSE579/blob/master/DataModelling/PixelRecurrentNeuralNetworks.txt). Following are the cleaning steps:
    * Remove single character lines
    * Logically regarrange the paragraphs as the text output from pdfminer might not be logically arranged
    * Remove line breaks introduced by pdfminer in text parsing
    * Filter out all the lines that don't have any mention of the paper. For this I am looking for terms like ['our', 'we', 'us'] in lines
   * The cleaned file can be found [here](https://github.com/monkeydunkey/CSE579/blob/master/DataModelling/PixelRecurrentNeuralNetworks_formatted_reduced.txt)
2. The cleaned file is now provided as an input to the openie information extractor you can read more about it [here](https://github.com/allenai/openie-standalone). The output of this process can be found in: "PixelInformationExtraction_reduced.txt"
3. Apply fileReducer.py to reduce the number of relations and keep only those that match to one of the 4 types of relation described above

## TODO
1. We need to make sense of the relationships as the phrase in the relationship can be a whole line for a single word. We can proabably use WordNET or Knowledge graph for some more reduction here
2. We need to establish "is a" sort of relationship as well. We can get this from WordNet as well as Knowledge Graph but if we can extract this from the text itself then we will have a much better understanding of our own domain
3. Come up with more relations if required
