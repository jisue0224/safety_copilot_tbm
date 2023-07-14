import streamlit as st
import speech_recognition as sr
from trans import trans
from konlpy.tag import Hannanum
from st_custom_components import st_audio_record
import pandas as pd


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
        
        
# def transcribe_speech(audio):
    # Initialize the recognizer
    # r = sr.Recognizer()

    # Transcribe the speech
    # text = r.recognize_google(audio)

    # return text

def main():

    
    st.title("🍀 :green[안전생산] :red[번역] :blue[서비스](Beta)")
    st.markdown("👷‍♂️ 외국인과 명확한 소통을 위해 한문장 단위로 녹음 바랍니다.")

    try:
        wav_audio_data = st_audio_record()
        print(f"wav audio data type: {type(wav_audio_data)}")
        # print(wav_audio_data)
        audio_data = sr.AudioData(wav_audio_data, sample_rate=16000, sample_width=2)
        print(f"pre audio type: {type(audio_data)}")
        # print(audio_data)
        
        # Read audio file and get sample rate and sample width
        sample_rate = audio_data.sample_rate
        sample_width = audio_data.sample_width

        print(f"Sample Rate: {sample_rate}")
        print(f"Sample Width: {sample_width}")

        print(1)
        recognizer = sr.Recognizer()
        print(2)
        
        text = recognizer.recognize_google(audio_data, language="ko-KR", show_all=True)

        print(text)
        
        
        
    except:
        pass


if __name__ == "__main__":
    
    main()
