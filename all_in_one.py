import streamlit as st
import speech_recognition as sr
from konlpy.tag import Mecab, Hannanum
import pandas as pd
import time
import pyaudio

def recognize_speech_from_mic(recognizer, microphone):
    
    start_time = time.time()
    print("ready to record")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    print("end recording")
    time_delta = time.time() - start_time
    print(f"녹음시간: {time_delta}")
    response = {
        "success": True,
        "error": None,
        "transcription": None
        }
    
    try:
        response["transcription"] = recognizer.recognize_google(audio, language="ko-KR", show_all=True)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"
    
    return response

def get_safety_keywords(txt, risk_words):
    # hannanum = Hannanum()
    mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")
    word_dict = {}
    risk_words = risk_words
    try:
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

    except:
            pass
        
def all_in_one_main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    if st.button("한 문장 녹음 시작"):
        time.sleep(1)
        st.markdown("✏️ 녹음을 시작하세요")
        result1 = recognize_speech_from_mic(recognizer, microphone)

        txt = result1["transcription"]
        st.markdown("✏️ All Cases of Speech to Text")
        st.markdown(f"{txt}")
        
        try:
            best_txt = result1["transcription"]['alternative'][0]['transcript']
            st.markdown("✏️ Best Speech to Text : ")
            st.markdown(f"{best_txt}")
        
            mywords = pd.read_excel("./my_words/mywords.xlsx")
            risk_words_list = mywords["mywords"].values
            
            st.markdown("✏️ 위험키워드 빈출도------------")
            result2 = get_safety_keywords(best_txt, risk_words_list)
            st.dataframe(result2)
            
            return best_txt
        
        except:
            st.markdown("✏️ 녹음된 음성이 없습니다.")
            
            return "Nothing"
    

def han_get_safety_keywords(txt, risk_words):
    hannanum = Hannanum()
    word_dict = {}
    risk_words = risk_words
    try:
        lines = txt.split("\n")
    
        for line in lines:
            malist = hannanum.pos(line)
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

    except:
            pass

  
def han_all_in_one_main():
    recognizer = sr.Recognizer()
    # Get the default audio device index
    default_device_index = -1  # Change this to the desired index
    microphone = sr.Microphone(device_index = default_device_index)
    
    if st.button("한 문장 녹음 시작"):
        time.sleep(1)
        st.markdown("녹음을 시작하세요")
        result1 = recognize_speech_from_mic(recognizer, microphone)

        txt = result1["transcription"]
        st.markdown("All Cases of Speech to Text")
        st.markdown(f"{txt}")
        
        try:
            best_txt = result1["transcription"]['alternative'][0]['transcript']
            st.markdown("Best Speech to Text : ")
            st.markdown(f"{best_txt}")
        
            mywords = pd.read_excel("./my_words/mywords.xlsx")
            risk_words_list = mywords["mywords"].values
            
            st.markdown("위험키워드 빈출도------------")
            result2 = han_get_safety_keywords(best_txt, risk_words_list)
            st.dataframe(result2)
        except:
            st.markdown("녹음된 음성이 없습니다.")

if __name__ == "__main__":
    
    all_in_one_main()

    