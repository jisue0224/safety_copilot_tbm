import streamlit as st
import speech_recognition as sr
from trans import trans
from konlpy.tag import Hannanum
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
        
        
def transcribe_speech(audio):
    # Initialize the recognizer
    r = sr.Recognizer()

    # Transcribe the speech
    text = r.recognize_google(audio)

    return text

def main():
    st.title("Speech Recognition with Streamlit")

    # Option to choose audio input source
    audio_source = st.radio("Select audio input source", ("File Upload", "Microphone"))

    if audio_source == "File Upload":
        # Upload an audio file
        audio_file = st.file_uploader("Upload an audio file", type=['wav'])

        if audio_file:
            # Convert the audio file to a path
            audio_path = audio_file.name

            # Display the audio file
            st.audio(audio_file)

            # Load the audio file
            with sr.AudioFile(audio_path) as source:
                # Read the entire audio file
                audio = r.record(source)
                
                
            response = {
            "success": True,
            "error": None,
            "transcription": None
            }


    elif audio_source == "Microphone":
        # Initialize the recognizer
        r = sr.Recognizer()

        # Start the microphone input
        with sr.Microphone() as source:
            st.info("Listening...")

            # Adjust microphone energy threshold for ambient noise levels
            r.adjust_for_ambient_noise(source)

            # Record the audio
            audio = r.listen(source)
            
        response = {
        "success": True,
        "error": None,
        "transcription": None
        }
    
        try:
            response["transcription"] = r.recognize_google(audio, language="ko-KR", show_all=True)
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"
        
        try:
            st.markdown(f"STT분석 결과 : {response['transcription']['alternative']}")
        except:
            pass
        try:
            stt_result = response["transcription"]['alternative'][0]['transcript']
            st.markdown(f"한국말 : {stt_result}")

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
            st.markdown("위험키워드 - Konlpy Hannanum Class 적용")
            mywords = pd.read_excel("./my_words/mywords.xlsx")
            risk_words_list = mywords["mywords"].values
            keyword_df = han_get_safety_keywords(stt_result, risk_words_list)
            keyword_df
        
            return stt_result, trans_result

        except:
            pass

if __name__ == "__main__":
    main()
