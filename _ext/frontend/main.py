import argparse, pickle, glob, os, re
from TreeProcessor import TreeProcessor
from lark import Lark, Transformer, Tree



class Preprocessor:
    def __init__(self, debug = False):
        self.in_generate = False
        self.block_count = 0
        self.debug = debug
    
    def detect_generate(self, l):
        if self.in_generate:
            if "endgenerate" in l:
                self.in_generate = False
        if "generate" and not "endgenerate" in l:
            self.in_generate = True
        return self.in_generate

    def detect_blocks(self, l):
        if "generate"in l: 
            return True
        if "endgenerate"in l: 
            return True
        if "case" in l:
            return True
        if "begin" in l:
            if re.match(r'(end |[^a-zA-Z-0-9_-]end\n)', l):
                return True
            self.block_count += 1
        if re.match(r'(end |end\n)', l) and self.block_count > 0:
            self.block_count -= 1
            return True
        return self.block_count > 0

    def preprocess(self, content):
        processed_data = []

        self.block_count = 0
        self.in_generate  = False
        
        for line in content:
            lstripped_line = line.lstrip()
            if not self.detect_blocks(lstripped_line):
                processed_data.append(lstripped_line)
        
        merged_data = ''
        for line in processed_data:
            merged_data += line
        
        if self.debug:
            with open('debug.txt', 'w') as fp:
                fp.write(merged_data)

        return merged_data

class FileParser:
    def __init__(self,debug = False):
        self.preproc = Preprocessor(debug=debug)
        self.tree_proc = TreeProcessor()
        with open('/home/fils/git/uscope_doc/_ext/frontend/grammar.lark') as f:
            grammar = f.read()

        self.parser = Lark(grammar, parser='earley', start='start',)

        # Remove indentation as it's useless and  a major PITA to work with
        
        self.files_content = {}
        self.debug = debug

    def parse_file(self, file):
        
        with open(file) as f:
            if self.debug:
                print(file)
            content = f.readlines()
            processed_content = self.preproc.preprocess(content)
            if self.debug:
                print("DONE PREPROCESSING")

            
            try:
                raw_content = self.parser.parse(processed_content)
            except Exception as e:
                print(f'\nParsing error in file: {file}')
                print(e)
                exit(1)

            self.files_content[file] = self.tree_proc.transform(raw_content)

if __name__ == "__main__":



    parser = FileParser(True)
    #files = glob.glob('/home/fils/git/sicdrive-hdl/Components/RTCU/rtl/*')
    files = glob.glob('/home/fils/git/sicdrive-hdl/Components/AdcProcessing/rtl/*')
    #files = ['/home/fils/git/sicdrive-hdl/Components/AdcProcessing/rtl/AdcProcessing.sv']
    for f in files:
        parser.parse_file(f)
    
    a = 0