import re

BYTE_ORDER_MARK='\uFEFF'
BYTE_ORDER_MARK_2='\uFFFE'
WORD_JOINER='\u2060'
SOFT_HYPHEN='\u00AD'

ZERO_WIDTH_SPACE='\u200B'
NO_BREAK_SPACE='\u00A0'

ZERO_WIDTH_NON_JOINER='\u200C'
ZERO_WIDTH_JOINER='\u200D'


def clean_text(text):
    text = text.lower()
    text=text.replace(BYTE_ORDER_MARK,'')
    text=text.replace(BYTE_ORDER_MARK_2,'')
    text=text.replace(WORD_JOINER,'')
    text=text.replace(SOFT_HYPHEN,'')

    text=text.replace(ZERO_WIDTH_SPACE,' ') # ??
    text=text.replace(NO_BREAK_SPACE,' ')

    text=text.replace(ZERO_WIDTH_NON_JOINER, '')
    text=text.replace(ZERO_WIDTH_JOINER,'')
        
    text = re.sub(r"[-()\"#/@;:<>{}-=~|.?,]","",text)
    return text

def str_to_unicode(str):
    return chr(int(str[2:],16))

class resolve_cotractions(object):
    def __init__(self, lang):
        super().__init__()
        self.lang = lang
        self.contractions =  []
        with open('contractions/'+lang+'.txt', 'r') as f:
            text = f.readline().rstrip()
            text = re.sub(r'\s+', r'\s', text) 
            contractions.append(text.split(' ', 1))
        
    def resolve_contractions(self, text):
        for contraction in self.contractions:
            text = re.sub(re.compile(self.contraction[0]), re.compile(self.contraction[1]), text)
        return text

 
class resolve_chars(object):
    def __init__(self, lang):
        super().__init__()
        self.lang = lang
        self.normalizations = []
        with open('unicode_normalization/'+lang+'.txt', 'r') as f :
            content = f.read()
            replacements = re.findall(r'\[.+\]', content)
            for elem in replacements :
                elem = elem.strip('[]')
                elems = elem.split(' , ')
                self.normalizations.append( [str_to_unicode(elem[0]), str_to_unicode(elem[1])] )
    
    def normalize(self, text) :
        for norm in self.normalizations:
            text = re.sub( re.compile(norm[0]), re.compile(norm[1]), text)
        return text
    
class resolve_group_chars(object):
    def __init__(self, lang):
        super().__init__()
        self.lang = lang
        self.replaces = []
        with open('unicode_normalization/groups'+lang+'.txt', 'r') as f :
            for line in f.readlines():
                line = re.sub(r'\s+',r'\s',line.rstrip())
                original, replacement = line.split(' ')
                match_str = self.make_pattern(original)
                repl_str = self.make_pattern(replacement)
            self.replaces.append((match_str, repl_str)) 
    
    def make_pattern(self, original, is_replacement=False):
        original_parts = original.split(',')
        match_str = ''
        for part in original_parts:
            if not part.startswith('0x') and is_replacement:
                match_str += '\\'+part
            else :               
                if '-' not in part:
                    match_str += '('+str_to_unicode(part)+')'
                else:
                    match_str += '([' + str_to_unicode(part.split('-')[0]) + '-' + str_to_unicode(part.split('-')[1]) + '])'
       return match_str

    def normalize(self, text) :
        for norm in self.replaces:
            text = re.sub( re.compile(norm[0]), re.compile(norm[1]), text)
        return text
 

