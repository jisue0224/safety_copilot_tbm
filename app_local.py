import streamlit as st
from st_custom_components import st_audio_record
from audio_to_text import audio_to_text
import speech_recognition as sr
from notion_api import insert_data, get_pages, read_as_df
from nlp_review import get_morphs_cnt, get_safety_keywords, get_mecab_nouns
import pandas as pd
from my_slack import Slack_Msg
from all_in_one import all_in_one_main
from trans import trans



st.set_page_config(page_title="AI_Copilot[Safety]")
# Design move app further up and remove top padding
st.markdown('''<style>.css-1egvi7u {margin-top: -3rem;}</style>''',
            unsafe_allow_html=True)
# Design change st.Audio to fixed height of 45 pixels
st.markdown('''<style>.stAudio {height: 45px;}</style>''',
            unsafe_allow_html=True)
# Design change hyperlink href link color
st.markdown('''<style>.css-v37k9u a {color: #ff4c4b;}</style>''',
            unsafe_allow_html=True)  # darkmode
st.markdown('''<style>.css-nlntq9 a {color: #ff4c4b;}</style>''',
            unsafe_allow_html=True)  # lightmode

def audiorec_demo_app():
    st.markdown('#### 🎙️:red[TBM] :blue[안전생산 브리핑] :green[Recorder]')
    
    wav_audio_data = st_audio_record() # tadaaaa! yes, that's it! :D
    col_info, col_space = st.columns([0.9, 0.1])
    with col_info:
        st.write('\n')  # add vertical spacer
        st.write('\n')  # add vertical spacer
        
    if wav_audio_data is not None:
        # display audio data as received on the Python side
        st.success("녹음 파일이 완료되었습니다. 다운로드 버튼을 클릭해주세요.")

    return wav_audio_data

if __name__ == '__main__':
    
    # TITLE and Creator information
    st.markdown("#### :red[AI Copilot] Series - :blue[Safety]🍀 ----------- Local 환경")
    st.markdown("## :red[TBM 음성 데이터] 기반 :blue[위험 예측 플랫폼]")
    st.write('\n')  # add vertical spacer
    
    with st.expander("🎈 TBM 안전생산 브리핑 가이드"):
        st.markdown('''
                    - `TBM`시 그날의 중요한 안전 및 생산에 관련 사항을 팀원들에게 1~2분 정도 브리핑(녹음 실시)
                    - 브리핑을 AI가 분석하여, `안전키워드`, `위험지수` 등을 관리자 및 차상위 관리자에게 모바일 전송
                    - 여러 생산팀에서 어떤 위험정보가 공유되었는지 확인하고 `현장 안전관리 체크포인트`로 참고
                    - 브리핑 내용을 `요약/번역`하여 외국인 근로자에게 모바일 알림 제공도 가능
                    ''')
    
    st.markdown("---")
    # 안전생산 브리핑 녹음
    with st.expander("🎙️ TBM 안전생산 브리핑 음성녹음"):
        
        audiorec_demo_app()
    
    st.markdown("---")
    # 음성 녹음 텍스트 변환(STT) --- 로컬에서만 작동
    with st.expander("🌞 음성 녹음 텍스트 변환 - STT"):
    
        recog=sr.Recognizer()
        st.markdown("<h3 style='text-align: center;'>Audio To Text Converter</h3>", unsafe_allow_html=True)
        st.markdown("---", unsafe_allow_html=True)  
        
        with st.form("Result"): 
            col1, col2, col3 = st.columns(3)
            with col1:
                dept_name = st.selectbox("부서", ["가공소조립1부", "판넬조립1부", "대조립1부"])
            with col2:
                sub_name = st.selectbox("생산팀", ["가공1팀", "판계1팀", "T/O팀", "조립1팀"])
            with col3:
                name = st.selectbox("성명", ["박보검", "박서준", "아이유", "이강인"])

            st.markdown("\n")
            audio=st.file_uploader("Upload TBM Audio File", type=['wav'])
            
            d_btn=st.form_submit_button("Proceed STT")    
            if d_btn:
                data = audio_to_text(audio, dept_name, sub_name, name)
                insert_data(data)
    
    st.markdown("---")
    # 저장 데이터 확인
    with st.expander("✏️ 텍스트 변환 데이터 조회"):
        df = read_as_df(get_pages())
        st.dataframe(df)
    
    st.markdown("---")
    with st.expander("📌 형태소 분석 - 위험키워드 빈출도 / Konlpy(Mecab)"):
        try:
            id = st.text_input("id를 입력해주세요")
            target_df = df[df["id_list"]==id]
            target_df
            target_txt = target_df['tbm_result'].values[0]
            target_txt
            
            dupl_cnt = st.slider('몇회 이상 중복 단어만 볼 것인가?', 1, 5, 1)
            mywords = pd.read_excel("C:/my_develop2/AI_TBM/my_words/mywords.xlsx")
            risk_words_list = mywords["mywords"].values
            조회구분 = st.checkbox("안전 관련 위험 단어만 보기")
            # print(조회구분)
            review_result = get_morphs_cnt(target_txt, dupl_cnt, risk_words_list, 조회구분)
            review_result.T
        except:
            pass
        
    st.markdown("---")
    
    with st.expander("📲 문자 전송"):
        try:
            id = st.text_input("id를 입력해주세요1")
            target_df = df[df["id_list"]==id]
            target_txt = target_df['tbm_result'].values[0]
            mywords = pd.read_excel("C:/my_develop2/AI_TBM/my_words/mywords.xlsx")
            risk_words_list = mywords["mywords"].values

            review_result = get_safety_keywords(target_txt, risk_words_list)
            review_result
            
            words = review_result["Word"].tolist()
            cnts= review_result["Count"].tolist()
            
            pairs = [pair for pair in zip(words, cnts)]
            # print(pairs)
            messages = []
            for i, pair in enumerate(pairs):
                pair = list(pair)
                # print(pair)
                # print(f"{pair[0]}는 {pair[1]}회 표출되었습니다.")
                msg = f"{pair[0]}: {pair[1]}회 표출"
                messages.insert(len(messages), msg)
                # print(messages)
            
            if st.button("Send"):
                Slack_Msg("[**TBM 안전생산 브리핑 안전지수***]")
                Slack_Msg(f'''
                          금일 TBM에서 언급된 위험관련 키워드는 다음과 같습니다.
                          {messages}
                          감사합니다.
                          ''')
        except:
            pass
    
    st.markdown("---")
    with st.expander("🚀 [참고용] 한문장 All in One 테스트 -- 녹음 파일을 거치지 않고 STT + 형태소 분석(Mecab)"):
        best_txt = all_in_one_main()
        # print(best_txt)
        
        target_lang = st.selectbox("번역 언어 선택", ["en", "zh", "vi", "th", "ja"])
        # print(target_lang)
        try:
            trans_result = trans(best_txt, target_lang)
            # print(trans_result.text)
            st.markdown(f"✏️ 번역결과 : {trans_result.text}")
        except:
            st.markdown("✏️ 번역 내용이 없습니다.")