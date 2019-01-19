# conll09-preprocess
Python code for pre-processing conll09 data.


## convert conll05 gold parses to universal dependencies 
```
export STANFORD_PARSER=/path/to/stanford/parser
```

**Train**
```
java -cp "$STANFORD_PARSER/*" -mx1g edu.stanford.nlp.trees.ud.UniversalDependenciesConverter -treeFile ~/canvas/data/conll05st-release-new/train-set.gz.parse > conll09/conll2005-train-universal.txt 
```

## align datasets

**Train**
```
python align.py --input_file_ptb ~/canvas/data/conll09/conll2005-train-universal.txt --input_file_conll ~/canvas/data/2009_conll_p2/data/CoNLL2009-ST-English/CoNLL2009-ST-English-train.txt --output_file ~/canvas/data/conll09/conll2009-train-universal.txt
Loaded 39832 sentences from ptb file
Loaded 39279 sentences from conll file
Aligned 30122 sents
Approximately aligned 9157 sents
Align collisions: 235
Total: 39279 sents
```

**Dev**
```
python align.py --input_file_ptb ~/canvas/data/conll09/conll2005-dev-universal.txt --input_file_conll ~/canvas/data/2009_conll_p2/data/CoNLL2009-ST-English/CoNLL2009-ST-English-development.txt --output_file ~/canvas/data/conll09/conll2009-dev-universal.txt
Loaded 1346 sentences from ptb file
Loaded 1334 sentences from conll file
Aligned 983 sents
Approximately aligned 351 sents
Align collisions: 9
Total: 1334 sents
```

**WSJ test**
```
python align.py --input_file_ptb ~/canvas/data/conll09/conll2005-test-wsj-universal.txt --input_file_conll ~/canvas/data/2009_conll_p2/data/CoNLL2009-ST-English/CoNLL2009-ST-evaluation-English.txt --output_file ~/canvas/data/conll09/conll2009-test-universal.txt
Loaded 2416 sentences from ptb file
Loaded 2399 sentences from conll file
Aligned 1832 sents
Approximately aligned 567 sents
Align collisions: 10
Total: 2399 sents
```

**Brown test**
```
python align.py --input_file_ptb ~/canvas/data/conll09/conll2005-test-brown-universal.txt --input_file_conll ~/canvas/data/2009_conll_p2/data/CoNLL2009-ST-English/CoNLL2009-ST-evaluation-English-ood.txt --output_file ~/canvas/data/conll09/conll2009-test-ood-universal.txt
Loaded 426 sentences from ptb file
Loaded 425 sentences from conll file
Aligned 395 sents
Approximately aligned 30 sents
Align collisions: 0
Total: 425 sents
```

