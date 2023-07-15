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
            st.info("녹음 완료")
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

    # Perform speech recognition
    try:
        # Use Google Speech Recognition for online speech recognition (requires internet connection)
        result = recognizer.recognize_google(audio, language='ko-KR')
        print("Recognized speech:", result)
        return result
    except sr.UnknownValueError:
        print("Unable to recognize speech")
    except sr.RequestError as e:
        print("Error: {0}".format(e))

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
       
def trans_keyword(stt_result):    
    try:
        target_lang = 'en'
        trans_result = trans(stt_result, target_lang).text
        st.markdown(f"영어 : {trans_result}")

        target_lang = 'ja'
        trans_result = trans(stt_result, target_lang).text
        st.markdown(f"일본어 :{trans_result}")
        
        target_lang = 'zh-cn'
        trans_result = trans(stt_result, target_lang).text
        st.markdown(f"중국어(simplified) :{trans_result}")
        
        target_lang = 'zh-tw'
        trans_result = trans(stt_result, target_lang).text
        st.markdown(f"중국어(traditional) :{trans_result}")
        
        target_lang = 'vi'
        trans_result = trans(stt_result, target_lang).text
        st.markdown(f"베트남어 : {trans_result}")
        
        target_lang = 'th'
        trans_result = trans(stt_result, target_lang).text
        st.markdown(f"태국어 : {trans_result}")
        
        target_lang = 'uz'
        trans_result = trans(stt_result, target_lang).text
        st.markdown(f"우즈베키스탄 : {trans_result}")
        
        target_lang = 'id'
        trans_result = trans(stt_result, target_lang).text
        st.markdown(f"인도네시아 : {trans_result}")
        
        st.markdown("---")
        st.markdown("#### 💥:red[위험키워드] - Konlpy Hannanum Class")
        mywords = pd.read_excel("./my_words/mywords.xlsx")
        risk_words_list = mywords["mywords"].values
        keyword_df = han_get_safety_keywords(stt_result, risk_words_list)
        keyword_df
        
    
        return stt_result, trans_result

    except:
        pass


if __name__ == "__main__":
    st.title("Client-Side Real-time Voice Record")
    st.error("카톡으로 링크로 열고, 우측 하단 점 세개 버튼 + 다른 브라우저로 열기- 크롬브라우저에서 오픈")
    st.warning("외국인 근로자 작업지시는 한문장 단위로 명확하게 해주세요")
    st.markdown("---")
    
    data = audio_rec_demo()
    print("1")
    print(type(data))
    
    
    filename = "output.wav"
    sample_width = 2  # In bytes, for 16-bit audio
    sample_rate = 44100  # The number of samples per second (standard for audio CDs)
    channels = 2 # Stereo audio

    save_wave_file(filename, data, sample_width, sample_rate, channels)
    
    text = wave_to_stt()
    st.success(f"{text}")
    
    st.markdown("---")
    trans_keyword(text)
    st.markdown("---")
    st.error("Created by Adannced AI Team")

