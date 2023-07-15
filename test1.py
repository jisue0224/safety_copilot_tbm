import os
import numpy as np
import streamlit as st
from io import BytesIO
import streamlit.components.v1 as components
import wave
import speech_recognition as sr

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
            st.audio(wav_audio_data, format='audio/wav')
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


if __name__ == "__main__":
    st.title("Client-Side Real-time Voice Record")
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

