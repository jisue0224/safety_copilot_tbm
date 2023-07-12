from konlpy.tag import Mecab
import pandas as pd

def get_morphs_cnt(txt, 중복개수, risk_words, 조회구분):
    # hannanum = Hannanum()
    mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")
    word_dict = {}
    risk_words = risk_words
    lines = txt.split("\n")
    for line in lines:
        malist = mecab.pos(line)
        for word in malist:
            if word[1] == "NNG" or word[1] == "NNP":
                if not (word[0] in word_dict):
                    word_dict[word[0]]=0
                word_dict[word[0]] +=1 

    if 조회구분:   # 안전단어만 볼건지.. 전체 단어 다 볼건지
        for word in word_dict.copy():
            if word not in risk_words:
                del word_dict[word]
    
    
    keys = sorted(word_dict.items(), key=lambda x:x[1], reverse=True)
    df = pd.DataFrame(keys, columns=['Word', 'Count'])
    r_df = df[df["Count"]>=중복개수]
    return r_df

def get_safety_keywords(txt, risk_words):
    # hannanum = Hannanum()
    mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")
    word_dict = {}
    risk_words = risk_words
    lines = txt.split("\n")
    for line in lines:
        malist = mecab.pos(line)
        for word in malist:
            if word[1] == "NNG" or word[1] == "NNP":
                if not (word[0] in word_dict):
                    word_dict[word[0]]=0
                word_dict[word[0]] +=1 

    for word in word_dict.copy():
        if word not in risk_words:
            del word_dict[word]
    
    
    keys = sorted(word_dict.items(), key=lambda x:x[1], reverse=True)
    df = pd.DataFrame(keys, columns=['Word', 'Count'])
    r_df = df[df["Count"]>=1]
    return r_df


def get_mecab_nouns(txt):
    mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")
    result = mecab.pos(txt)
    print(result)               

if __name__ == "__main__":
    
    mywords = pd.read_excel("./my_words/mywords.xlsx")
    risk_words_list = mywords["mywords"].values
    조회구분 = False
    
    sentence1 = '''그리고 블록 들면서 샤클 체결할 때도.. 샤클에 가용접만 된 상태가 아닌지 잘 확인해주세요.
    얼마전에 대조립9부에서 블록들다가 샤클 터져서 큰 사고날뻔한 것 다들 잘 알고 있을 것 입니다.
    비슷한 사고가 반복되지 않도록 모든 작업자들이 샤클 체결시 집중해주길 바랍니다..'''
    
    # print(get_hannanum_morphs(sentence1))
    print(get_morphs_cnt(sentence1, 1, risk_words_list, 조회구분))
    
    # print(get_mecab_nouns(sentence1))
    
