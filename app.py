import streamlit as st
from st_custom_components import st_audio_record

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

    # start_time = time.time()
    
    wav_audio_data = st_audio_record() # tadaaaa! yes, that's it! :D
    col_info, col_space = st.columns([0.9, 0.1])
    with col_info:
        st.write('\n')  # add vertical spacer
        st.write('\n')  # add vertical spacer
        
    if wav_audio_data is not None:
        # display audio data as received on the Python side
        st.success("녹음 파일이 완료되었습니다. 다운로드 버튼을 클릭해주세요.")

    # time_delta = time.time() - start_time

    return wav_audio_data

if __name__ == '__main__':
    
        # TITLE and Creator information
    st.markdown("#### :red[AI Copilot] Series - :blue[Safety]🍀")
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
    