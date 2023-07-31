# import os
# import numpy as np
# import streamlit as st
# from io import BytesIO
# import streamlit.components.v1 as components
# import time
# import streamlit as st

# def st_audio_record():
    
#     st.write('👉 Stop 버튼후 음성 데이터가 처리됩니다. 잠시 기다려주세요.')
    
#     # get parent directory relative to current directory
#     parent_dir = os.path.dirname(os.path.abspath(__file__))
#     # Custom REACT-based component for recording client audio in browser
#     build_dir = os.path.join(parent_dir, "st_audiorec/frontend/build")
#     # specify directory and initialize st_audiorec object functionality
#     st_audiorec = components.declare_component("st_audiorec", path=build_dir)
    
#     # Create an instance of the component: STREAMLIT AUDIO RECORDER
#     raw_audio_data = st_audiorec()  # raw_audio_data: stores all the data returned from the streamlit frontend
#     wav_bytes = None                # wav_bytes: contains the recorded audio in .WAV format after conversion
#     # the frontend returns raw audio data in the form of arraybuffer
#     # (this arraybuffer is derived from web-media API WAV-blob data)

#     if isinstance(raw_audio_data, dict):  # retrieve audio data   
        
#         with st.spinner('음성 데이터를 처리하고 있습니다...'):
#             ind, raw_audio_data = zip(*raw_audio_data['arr'].items())

#             ind = np.array(ind, dtype=int)  # convert to np array
#             raw_audio_data = np.array(raw_audio_data)  # convert to np array
#             sorted_ints = raw_audio_data[ind]
#             stream = BytesIO(b"".join([int(v).to_bytes(1, "big") for v in sorted_ints]))
#             stream = BytesIO(b"".join([int(v).to_bytes(1, "big") for v in raw_audio_data]))
#             # wav_bytes contains audio data in byte format, ready to be processed further
#             wav_bytes = stream.read()
            
       
#     return wav_bytes




# if __name__ == "__main__":
    # st.title("Client-Side Voice Record Test")
    # start_time = time.time()
    # st_audio_record()
    # # print(type(st_audio_record()))
    # time_delta = time.time() - start_time
    # st.markdown(f"Stop후 음성 데이터 처리 소요시간(초) : {np.round(time_delta, 2)}")   


import os
import numpy as np
import streamlit as st
from io import BytesIO
import streamlit.components.v1 as components
import time

def st_audio_record():
    st.write('👉 Please wait for audio data processing after pressing the Stop button.')

    # Get the parent directory relative to the current directory
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    # Path to the custom REACT-based component for recording client audio in the browser
    build_dir = os.path.join(parent_dir, "st_audiorec/frontend/build")
    # Declare the st_audiorec component functionality
    st_audiorec = components.declare_component("st_audiorec", path=build_dir)

    # Create an instance of the component: STREAMLIT AUDIO RECORDER
    raw_audio_data = st_audiorec()  # raw_audio_data: stores all the data returned from the Streamlit frontend
    wav_bytes = None  # wav_bytes: contains the recorded audio in .WAV format after conversion

    if isinstance(raw_audio_data, dict):  # Retrieve audio data
        with st.spinner('Processing audio data...'):
            # Extract audio data from the raw_audio_data dictionary
            ind, raw_audio_data = zip(*raw_audio_data['arr'].items())
            ind = np.array(ind, dtype=int)  # Convert to a NumPy array
            raw_audio_data = np.array(raw_audio_data)  # Convert to a NumPy array
            # Sort the audio data based on indices
            sorted_ints = raw_audio_data[ind]
            # Convert the audio data to bytes format
            stream = BytesIO(b"".join([int(v).to_bytes(1, "big") for v in sorted_ints]))
            # wav_bytes contains audio data in byte format, ready to be processed further
            wav_bytes = stream.read()

    return wav_bytes

if __name__ == "__main__":
    st.title("Client-Side Voice Record Test")
    start_time = time.time()
    st_audio_record()
    time_delta = time.time() - start_time
    st.markdown(f"Time taken for audio data processing (seconds): {np.round(time_delta, 2)}")
