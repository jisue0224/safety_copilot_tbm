# import googletrans
from googletrans import Translator


def trans(txt, target):
    trans = Translator()
    result = trans.translate(txt, dest=target)
    return result


if __name__ == "__main__":
    
    txt = "내일 학교를 갑니다."
    target= "ja"

    print(trans(txt, target))