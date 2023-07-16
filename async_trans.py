import asyncio
from aiogoogletrans import Translator
import time

async def trans(txt, input_lang, target_lang):
    trans = Translator()
    en_result = await trans.translate(txt, src=input_lang, dest="en")
    result = await trans.translate(en_result.text, src='en', dest=target_lang)
    print(result.text)
    return result.text

async def main(txt):
    
    # translations = await asyncio.gather(
    #     trans(txt, 'ko', 'en'),
    #     trans(txt, 'ko', 'ja'),
    #     trans(txt, 'ko', 'vi'),
    #     trans(txt, 'ko', 'th'),
    #     trans(txt, 'ko', 'uz')
    #     )
    
    
    input_lang = 'ko'
    target_langs = ['en', 'ja', 'vi', 'th', 'uz']
    
    translations = await asyncio.gather(*[trans(txt, input_lang, target_lang) for target_lang in target_langs])

    return translations
    


if __name__ == "__main__":
    start_time = time.time()
    
    txt = "내일 학교를 갑니다."
    results = asyncio.run(main(txt))
    print(results)
    end_time = time.time()
    print(end_time - start_time)
