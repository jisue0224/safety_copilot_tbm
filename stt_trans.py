import os
import numpy as np
import streamlit as st
from io import BytesIO
import streamlit.components.v1 as components
import wave
import speech_recognition as sr
from async_trans import trans
from konlpy.tag import Hannanum
import pandas as pd
import asyncio
from notion_api_cnt import insert_data, get_pages


def st_audiorec():

    # get parent directory relative to current directory
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    # Custom REACT-based component for recording client audio in browser
    build_dir = os.path.join(parent_dir, "st_audiorec/frontend/build")
    # specify directory and initialize st_audiorec object functionality
    st_audiorec = components.declare_component("st_audiorec", path=build_dir)

    # Create an instance of the component: STREAMLIT AUDIO RECORDER
    raw_audio_data = st_audiorec()  # raw_audio_data: stores all the data returned from the streamlit frontend
    wav_bytes = None                # wav_bytes: contains the recorded audio in .WAV format after conversion

    # the frontend returns raw audio data in the form of arraybuffer
    # (this arraybuffer is derived from web-media API WAV-blob data)

    if isinstance(raw_audio_data, dict):  # retrieve audio data
        with st.spinner('retrieving audio-recording...'):
            ind, raw_audio_data = zip(*raw_audio_data['arr'].items())
            ind = np.array(ind, dtype=int)  # convert to np array
            raw_audio_data = np.array(raw_audio_data)  # convert to np array
            sorted_ints = raw_audio_data[ind]
            stream = BytesIO(b"".join([int(v).to_bytes(1, "big") for v in sorted_ints]))
            # wav_bytes contains audio data in byte format, ready to be processed further
            wav_bytes = stream.read()

    return wav_bytes

def audio_rec_demo():
    
    wav_audio_data = st_audiorec()
    
    if wav_audio_data is not None:
        # display audio data as received on the Python side
        col_playback, col_space = st.columns([0.58,0.42])
        with col_playback:
            # print(type(wav_audio_data))
            # st.info("녹음 완료")
            # st.audio(wav_audio_data, format='audio/wav')
            wave_file = wave.open("output.wav", "wb")
            
    return wav_audio_data

def save_wave_file(filename, data, sample_width, sample_rate, channels):
    try:
        with wave.open(filename, 'wb') as wave_file:
            wave_file.setnchannels(channels)
            wave_file.setsampwidth(sample_width)
            wave_file.setframerate(sample_rate)
            wave_file.writeframes(data)
        
    except:
        # print("뭐니")
        pass     
    

def wave_to_stt(input_lang):
    
    lang_dict = {
        '한국(KOR)': 'ko-KR', 
        '영어(ENG)': 'en-US',
        '베트남(VNM)': 'vi-VN',
        '태국(THA)': 'th-TH',
        '우즈베키스탄(UZB)': 'uz-UZ',
        '인도네시아(IDN)': 'id-ID',
        '중국(CHN)': 'zh',
        '일본(JPN)': 'ja-JP'   
        }
    
    target = lang_dict[input_lang]
    
    filename = "output.wav"

    # Create an instance of the Recognizer class
    recognizer = sr.Recognizer()

    # Load the wave file
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)  # Read the entire audio file

    response = {
        "success": True,
        "error": None,
        "transcription": None
        }
    
    # Perform speech recognition
    try:
        response["transcription"] = recognizer.recognize_google(audio, language=target, show_all=True)
        os.remove('output.wav')
        return response
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"
    
    

def han_get_safety_keywords(txt, risk_words):
    hannanum = Hannanum()
    word_dict = {}
    risk_words = risk_words
    try:
        lines = txt.split("\n")
    
        for line in lines:
            malist = hannanum.pos(line)
            for word in malist:
                if word[1] == "N":
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
    except:
        pass


       
async def trans_keyword(stt_result, input_lang, target_langs):
    
    st.markdown("##### 🌻:green[번역 결과] (영어를 거쳐 3국어로 번역)")
    
    target_dict = {
        '영어(ENG)': 'en',
        '베트남(VNM)': 'vi',
        '태국(THA)': 'th',
        '우즈베키스탄(UZB)': 'uz',
        '인도네시아(IDN)': 'id',
        '중국(CHN)': 'zh-cn',       # chinese simplified : zh-cn, chinese traditional : zh-tw
        '일본(JPN)': 'ja',
        '한국(KOR)': 'ko'
        }
    
    selected_input_lang = target_dict[input_lang]
    selected_target_langs = [target_dict[i] for i in target_langs]
    target_input = stt_result
    
    try:
        translations = await asyncio.gather(*[trans(target_input, selected_input_lang, selected_target_lang) for selected_target_lang in selected_target_langs])
        
        for lang, translation in zip(target_langs, translations):
            st.markdown(f"😉 **{lang}** : {translation}")
        
        return translations
    except:
        print("뭐꼬?")
        pass

def get_visiting_count(val1, cnt):
    if val1 != None:
        cnt += 1
        return cnt


if __name__ == "__main__":   
    
    col001, col002 = st.columns([5.5, 4.5])
    with col001:     
    
        st.markdown("###### :red[AI Insight] Series - :blue[안전생산]🍀 [beta service]")
        st.markdown("#### :green[외국인 근로자] 작업지시 :blue[통역지원]")
        st.markdown("###### :violet[(AI Work Order Translation Service for Foreign Workers)]")
        st.write('\n')  # add vertical spacer
        
        st.error("🌈 :red[**크롬 or 사파리**]에서 오픈~ 카톡 링크 경유 오픈시 우측 하단 버튼 + 다른 브라우저 열기 (문자 링크는 OK)")
        
        input_langs = ["한국(KOR)", "영어(ENG)", "베트남(VNM)", "태국(THA)", "우즈베키스탄(UZB)", "인도네시아(IDN)", "중국(CHN)", "일본(JPN)"]
        target_langs = ["영어(ENG)", "베트남(VNM)", "태국(THA)", "우즈베키스탄(UZB)", "인도네시아(IDN)", "중국(CHN)", "일본(JPN)", "한국(KOR)"]
        selected_input_lang = st.selectbox("📌 **입력 언어**(Input)를 선택하세요 (기본 한국어)", input_langs)
        selected_target_lang = st.multiselect("📌 **번역 언어**(Output)를 선택해주세요 (복수 선택 가능)", target_langs, target_langs)
        
        st.warning("👨‍🔧 외국인 근로자 작업지시는 :red[**쉬운 단어 + 한문장**]으로 명확하게 해주세요 :blue[**(Start~, Stop~ 버튼)**]")

        with st.container():
            data = audio_rec_demo()
                
            filename = "output.wav"
            sample_width = 2  # In bytes, for 16-bit audio
            sample_rate = 44100  # The number of samples per second (standard for audio CDs)
            channels = 2 # Stereo audio

            save_wave_file(filename, data, sample_width, sample_rate, channels)
            
            try:
                text = wave_to_stt(selected_input_lang)
                st.success(f"📢작업 지시 : {text['transcription']['alternative'][0]['transcript']}")
                revised_txt = st.text_area("🔄 아래 텍스트 :blue[**수정**]시 다시 번역 (수정후 글상자 외부 터치)", value = text['transcription']['alternative'][0]['transcript'] )
                
                with st.expander("🐳 :blue[**All Cases of STT Review**] - 음성 텍스트 변환 검토"):
                    st.info(f"{text['transcription']['alternative']}")
                    st.markdown('''
                                **[AI 토막 상식] STT란 무엇인가요??**\n
                                :red[**STT**]는 Speech to Text의 약자로서 사람이 말하는 음성 언어를 
                                AI 알고리즘으로 해석해 그 내용을 문자 데이터로 전환하는 것을 의미하며,
                                Confidence Level이 가장 높은 결과를 Best STT로 반환합니다.
                                STT는 향후 음성 데이터 기반 업무 개선 도구로 확대될 예정입니다.                      
                                ''')
            except:
                pass
        st.markdown("---")
        
        
        try:
            best_stt = revised_txt
            result = asyncio.run(trans_keyword(best_stt, selected_input_lang, selected_target_lang))
            if result != None:
                name = "박보검"
                data = {
                    "Name" : {"title": [{"text": {"content": name}}]},
                    }
                insert_data(data)
            
        except:
            pass
        st.markdown("---")
        
        mywords = pd.read_excel("mywords.xlsx")
        
        try:
            st.markdown("##### 💥:red[위험키워드]- Hannanum Test")
            risk_words_list = mywords["mywords"].values
            keyword_df = han_get_safety_keywords(best_stt, risk_words_list)
            keyword_df
        except:
            st.markdown("해당사항 없음(테스트중)")
            pass
        
        st.markdown("---")

        st.error("⚾ ***Created by :red[Advanced AI Team] in :blue[AI Center]***")
        st.markdown("###### 🔒 본 서비스는 음성 및 텍스트를 저장하지 않습니다.")
        st.markdown("###### 📧 Contact : jongbae.kim@ksoe.co.kr")
        st.markdown("###### 💖 Supported by [Stefan](https://github.com/stefanrmmr/streamlit_audio_recorder), [Google](https://github.com/ssut/py-googletrans), [Konlpy](https://konlpy.org/ko/latest/index.html), etc.")
