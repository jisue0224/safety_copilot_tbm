# import googletrans
from googletrans import Translator


def trans(txt, input_lang, traget_lang):
    trans = Translator()
    en_result = trans.translate(txt, src=input_lang, dest="en")
    print(en_result.text)
    result = trans.translate(en_result.text, src='en', dest=traget_lang)
    print(result.text)


    return result


if __name__ == "__main__":
    
    txt = "내일 학교를 갑니다."
    input_lang = 'ko'
    target_lang= "ja"

    trans(txt, input_lang, target_lang)