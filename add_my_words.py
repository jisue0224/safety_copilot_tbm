# pip install jamo  ## 종성 여부를 판단하기 위한 라이브러리
#############################
import pandas as pd
from jamo import h2j, j2hcj

def get_jongsung_TF(sample_text):
    sample_text_list = list(sample_text)
    last_word = sample_text_list[-1]
    last_word_jamo_list = list(j2hcj(h2j(last_word)))
    last_jamo = last_word_jamo_list[-1]
    jongsung_TF = "T"
    if last_jamo in ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅘ', 'ㅚ', 'ㅙ', 'ㅝ', 'ㅞ', 'ㅢ', 'ㅐ,ㅔ', 'ㅟ', 'ㅖ', 'ㅒ']:
        jongsung_TF = "F"
    return jongsung_TF


with open("C:/mecab/user-dic/nnp.csv", 'r', encoding='utf-8') as f:
    file_data = f.readlines()

## 추가할 단어는 mywords 폴더 내 mywords.xlsx 파일에 추가

myword = pd.read_excel("./my_words/mywords.xlsx")
word_list = myword["mywords"].tolist()
print(word_list)


for word in word_list:
    jongsung_TF = get_jongsung_TF(word)
    line = '{},,,,NNP,*,{},{},*,*,*,*,*\n'.format(word, jongsung_TF, word)

    file_data.append(line)

with open("C:/mecab/user-dic/nnp.csv", 'w', encoding='utf-8') as f:
    for line in file_data:
        f.write(line)
#
with open("C:/mecab/user-dic/nnp.csv", 'r', encoding='utf-8') as f:
    file_new = f.readlines()

print(file_new)


'''
컴파일
1. powershell 관리자 모드 열기
2. cd C:\mecab
3.  .\tools\add-userdic-win.ps1 


'''




