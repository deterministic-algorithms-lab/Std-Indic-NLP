import os

def execute(command) :
    x = os.system(command)
    if x>>8!=0 : 
        exit(1)

#Shuffle a monolingual file
def shuf_mono(filename) :
    assert os.path.isfile(filename)

#Shuffle parallel language data files
def shuf_pll(lg_pair: str, para_folder) :
    lgs = lg_pair.split('-')
    assert os.path.isfile(os.path.join(para_folder, lg_pair+'.'+lgs[0])) and os.path.isfile(os.path.join(para_folder, lg_pair+'.'+lgs[1]))     

#Get language from filename
def get_lang(filename) :
    if len(filename)>=8 and bool(re.match('..-..\...',filename[-8:])) :
        return filename[-2]+filename[-1]
    elif len(filename)>=7 and bool(re.match('..\.mono', filename[-7:])) :
        return filename[-7]+filename[-6]
    else :
        raise ValueError('Filename '+filename+' should end with a string of form \'lg.mono\' or \'lg-lg.lg\' to be processed.')