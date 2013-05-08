import sys
from optparse import OptionParser

def main():
    
    optparser = OptionParser(usage="""
            %prog TOKENS_FILE TRAIN_FILE""")
    opts, args = optparser.parse_args()
    
    tokens_dict = dict()
    
    token_file = open(args[0])
    train_file = open(args[1])
    
    index = 1
    for tok in token_file:
        tokens_dict[int(tok.strip())] = index
        index = index + 1
    
    columns_with_tokens = [8, 10, 12, 14]
    
    index = 0
    for line in train_file:
        
        if not line.strip():
            continue
        
        features = line.strip().split('\t')
        
        tokens_in_line = []
        
        for col in columns_with_tokens:
            tokens_in_col = features[col].strip().split('|')
            for tok in tokens_in_col:
                tokens_in_line.append(int(tok))
        
        unical_tokens_in_line = dict()
            
        for tok in tokens_in_line:
            if tok not in unical_tokens_in_line:
                unical_tokens_in_line[tok] = 1
            else:
                unical_tokens_in_line[tok] = unical_tokens_in_line[tok] + 1
        
        s = ""
        for tok in unical_tokens_in_line:
            s += " %s:%s" % (tokens_dict[tok], unical_tokens_in_line[tok])
        
        if features[0] == "0":
            features[0] = -1
        else:
            features[0] = 1
        
        print "%s |%s" % (int(features[0]), s)
        
        index = index + 1

if __name__ == "__main__":
    main()