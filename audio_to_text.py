import streamlit as st
from pydub import AudioSegment, silence
import speech_recognition as sr
import os
from dev_files.notion_api import insert_data


def audio_to_text(audio, dept_name, sub_name, name):
    recog=sr.Recognizer()
    tbm_result = ""
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    # print(parent_dir)
    
    if audio:
        st.audio(audio)
        audio_segment=AudioSegment.from_wav(audio)
        chunks=silence.split_on_silence(audio_segment, min_silence_len=500, silence_thresh=audio_segment.dBFS-20, keep_silence=100)
        
        for index,chunk in enumerate(chunks):
            filename = str(index)+".wav"
            save_dir = os.path.join(parent_dir, "audio_samples/")
            path = save_dir+filename
            chunk.export(path, format="wav")

            with sr.AudioFile(path) as source:
                recorded=recog.record(source)
                try:
                    text=recog.recognize_google(recorded, language="ko-KR")
                    print(text)
                    tbm_result=tbm_result+" "+text
                    
                except:
                    print("None")
                    tbm_result=tbm_result+" Unaudible"
                    
            os.remove(path)
            
        # with st.form("Result"): 
        #     result=st.text_area("TEXT", value=tbm_result) 
        #     d_btn=st.form_submit_button("Download")    
        #     if d_btn:
        #         envir_var=os.environ
        #         usr_loc=envir_var.get('USERPROFILE')
        #         loc="C:/my_develop2/TBM_STT/txt_results/transcript.txt"
        #         with open(loc, 'w') as file:
        #             file.write(result)
        
        dept_name = dept_name
        sub_name = sub_name
        name = name
        tbm_result = tbm_result
        status = "False"
        
        data = {
            "dept_name" : {"title": [{"text": {"content": dept_name}}]},
            "sub_name": {"rich_text": [{"text": {"content": sub_name}}]},
            "name": {"rich_text": [{"text": {"content": name}}]},
            "tbm_result": {"rich_text": [{"text": {"content": tbm_result}}]},
            "status":  {"rich_text": [{"text": {"content": status}}]},
            }
        
        return data 

if __name__ == "__main__":
    
    recog=sr.Recognizer()
    st.markdown("<h1 style='text-align: center;'>Audio To Text Converter</h1>", unsafe_allow_html=True)
    st.markdown("---", unsafe_allow_html=True)  
    
    with st.form("Result"): 
        col1, col2, col3 = st.columns(3)
        with col1:
            dept_name = st.selectbox("부서", ["가공소조립1부", "판넬조립1부", "대조립1부"])
        with col2:
            sub_name = st.selectbox("생산팀", ["가공1팀", "판계1팀", "T/O팀", "조립1팀"])
        with col3:
            name = st.selectbox("성명", ["박보검"])

        st.markdown("\n")
        audio=st.file_uploader("Upload TBM Audio File", type=['wav'])
        
        d_btn=st.form_submit_button("Proceed STT")    
        if d_btn:
            data = audio_to_text(audio, dept_name, sub_name, name)
            insert_data(data)
                

        