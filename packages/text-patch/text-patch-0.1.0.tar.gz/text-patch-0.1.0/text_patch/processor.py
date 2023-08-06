import re
import edit_distance
from typing import List
import os

class BaseProcessor():
    """
    處理器基礎類別
    """
    @classmethod
    def from_file(cls,*args,**kwargs):
        raise NotImplementedError
    
class NoChangeProcessor(BaseProcessor):
    """
    依據保留詞字典，回傳新的句子；將一些誤修正選項撤銷
    """
    def __init__(self,no_change_words:List[str]=[]) -> None:
        self.no_change_words = no_change_words
    
    @classmethod
    def from_file(cls,file_path):
        assert os.path.isfile(file_path)
        with open(file_path,'r',encoding='utf-8') as f:
            return cls(f.read().split())

    def __call__(self, sent_a,sent_b):
        """
        :parm sent_a: error correction *前*的句子
        :parm sent_b: error correction *後*的句子
        :return: 依據保留詞字典，回傳新的句子；將一些誤修正選項撤銷。
        """
        for no_change_word in self.no_change_words:
            matches = re.finditer(no_change_word,sent_a)
            
            sm = edit_distance.SequenceMatcher(a=sent_a, b=sent_b)
            opcodes = sm.get_opcodes()
            opcodes = list(filter(lambda x:x[0]=="replace",opcodes))
                        
            for match in matches:
                match_start,match_end = match.span()
                
                for opcode in opcodes:
                    op_name,sent_a_start,sent_a_end,sent_b_start,sent_b_end = opcode

                    for match_idx in range(match_start,match_end):

                        for sent_a_idx,sent_b_idx in zip(range(sent_a_start,sent_a_end),range(sent_b_start,sent_b_end)):
                            if match_idx == sent_a_idx:
                                sent_a = list(sent_a)
                                sent_b = list(sent_b)
                                sent_b[sent_b_idx] = sent_a[sent_a_idx]
                                sent_a = ''.join(sent_a)
                                sent_b = ''.join(sent_b)
        return sent_b
                                            

class NormalizeProcessor(BaseProcessor):
    def __init__(self,normalize_dict:dict={}):
        """
        :parm normalize_dict: 正規化映射字典 {"key":["pattern_1","pattern_2"]}
        """
        regexps = []
        for key,patterns in normalize_dict.items():
            patterns = [re.escape(p) for p in patterns]
            regexps.append(('|'.join(patterns),key))
        self.regs = regexps
    
    @classmethod
    def from_file(cls,file_path):
        """
        :parm file_path: 正規化映射字典路徑。key=pattern_1,pattern_2
        """
        assert os.path.isfile(file_path)
        with open(file_path,'r',encoding='utf-8') as f:
            data = f.read().strip().split("\n")
            
            normalize_dict = {}
            for line in data:
                try:
                    key,patterns = line.split("=")
                except:
                    print("error format: ->",line)
                patterns = patterns.strip().split(",")
                normalize_dict[key] = patterns    
            
            return cls(normalize_dict)

    def __call__(self, x):
        for reg,tgt_text in self.regs:
            x = re.sub(reg,tgt_text,x)           
        return x


