# import googletrans
from googletrans import Translator


def trans(txt, target):
    trans = Translator()
    en_result = trans.translate(txt, dest="en")
    print(en_result.text)
    result = trans.translate(en_result.text, src='en', dest=target)
    print(result.text)


    return result


if __name__ == "__main__":
    
    txt = "내일 학교를 갑니다."
    target= "ja"

    trans(txt, target)