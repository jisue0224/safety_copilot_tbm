import os
import numpy as np
import streamlit as st
from io import BytesIO
import streamlit.components.v1 as components
import wave
import speech_recognition as sr
from trans import trans
from konlpy.tag import Hannanum
import pandas as pd

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
    

def wave_to_stt():
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
        response["transcription"] = recognizer.recognize_google(audio, language="ko-KR", show_all=True)
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


       
def trans_keyword(stt_result, lang_list):
    
    st.markdown("##### 🌻:green[번역 결과] (한글▶️영어▶️3국어 변환)")
    
    target_dict = {
        '영어': 'en',
        '베트남': 'vi',
        '태국': 'th',
        '우즈베키스탄': 'uz',
        '인도네시아': 'id',
        '중국': 'zh-ch',
        '일본': 'jp'   
        }
    
    # changed_input = trans(stt_result, "en").txt  # 한글을 영어로 변환후 3국언어로 번역
    # print(changed_input)
    # st.markdown(f"{changed_input}")
    # target_input = changed_input
    
    target_input = stt_result
        
    try:
        for target_lang in lang_list:
            target_lang_key = target_dict[target_lang]
            
            trans_result = trans(target_input, target_lang_key).text
            st.markdown(f"😉 **{target_lang}** : {trans_result}")

        

        
    
        return stt_result, trans_result

    except:
        pass


if __name__ == "__main__":   
    
    col001, col002 = st.columns([5.5, 4.5])
    with col001:     
    
        st.markdown("###### :red[AI Copilot] Series - :blue[안전생산]🍀 [beta service]")
        st.markdown("#### :red[외국인 근로자] 업무지시 :blue[통역지원]")
        st.markdown("###### :violet[(AI Work Order Translation Service for Foreign Workers)]")
        st.write('\n')  # add vertical spacer
        
        st.error("✔️ 카톡 링크 열고 우측 하단 버튼 + 다른 브라우저로 열기--- :red[**크롬 or 사파리**]에서 오픈")
        st.warning("👨‍🔧 외국인 근로자 작업지시는 :red[**한문장 단위**]로 명확하게 해주세요 :blue[**(Start~, Stop~ 버튼)**]")
        
        
        langs = ["영어", "베트남", "태국", "우즈베키스탄", "인도네시아", "중국", "일본"]
        selected_lang = st.multiselect("📌 번역하고 싶은 외국어를 선택해주세요 (복수 선택 가능)", langs, ["영어", "베트남"])
        
        with st.container():
            data = audio_rec_demo()
                
            filename = "output.wav"
            sample_width = 2  # In bytes, for 16-bit audio
            sample_rate = 44100  # The number of samples per second (standard for audio CDs)
            channels = 2 # Stereo audio

            save_wave_file(filename, data, sample_width, sample_rate, channels)
            
            text = wave_to_stt()
            
            try:
                st.success(f"📢업무 지시 : {text['transcription']['alternative'][0]['transcript']}")
                with st.expander("🐳 :blue[**All Cases of STT Review**] - 음성의 텍스트 변환 검토"):
                    st.info(f"{text['transcription']['alternative']}")
                    st.markdown('''
                                **[AI 공부] STT란 무엇인가요??**\n
                                :red[**STT**]는 Speech to Text의 약자로서 사람이 말하는 음성 언어를 
                                AI 알고리즘으로 해석해 그 내용을 문자 데이터로 전환하는 것을 의미하며,
                                Confidence Level이 가장 높은 결과를 Best STT로 반환합니다.
                                STT는 향후 음성 데이터 기반의 업무 개선의 도구로 확대될 예정입니다.                      
                                ''')
            except:
                pass
        st.markdown("---")
        
        
        try:
            best_stt = text['transcription']['alternative'][0]['transcript']
            trans_keyword(best_stt, selected_lang)
        except:
            pass
        st.markdown("---")
        
        try:
            st.markdown("##### 💥:red[위험키워드]-Konlpy Hannanum")
            mywords = pd.read_excel("mywords.xlsx")
            risk_words_list = mywords["mywords"].values
            keyword_df = han_get_safety_keywords(best_stt, risk_words_list)
            keyword_df
        except:
            pass
        
        st.error("⚾ ***Created by :red[Advanced AI Team] in :blue[AI Center]***")
        
        st.markdown("---")
        st.markdown("###### ❓ Contact : jongbae.kim@ksoe.co.kr")
        st.markdown("###### 💖 Thanks to [Stefan](https://github.com/stefanrmmr/streamlit_audio_recorder), [GoogleTrans](https://github.com/ssut/py-googletrans), [Konlpy](https://konlpy.org/ko/latest/index.html), etc.")
