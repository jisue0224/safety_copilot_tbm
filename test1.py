import streamlit as st

def main():
    st.title("WebRTC Example with Streamlit")
    
    # Render the HTML for capturing audio using WebRTC
    st.components.v1.html(
        """
        <h2>Audio Capture</h2>
        <div id="audio-container"></div>
        <button id="start-btn">Start Recording</button>
        <button id="stop-btn" disabled>Stop Recording</button>
        <script>
        // Create audio context
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();

        // Create media stream source
        navigator.mediaDevices.getUserMedia({ audio: true })
          .then(stream => {
            const mediaStreamSource = audioContext.createMediaStreamSource(stream);
            
            // Create audio processor
            const processor = audioContext.createScriptProcessor(1024, 1, 1);
            
            // Connect audio source to processor
            mediaStreamSource.connect(processor);
            
            // Connect processor to output
            processor.connect(audioContext.destination);
            
            // Handle audio data
            processor.onaudioprocess = function(event) {
              const audioData = event.inputBuffer.getChannelData(0);
              
              // Send audio data to Streamlit app
              Streamlit.setComponentValue(audioData);
            };
            
            // Start recording
            const startBtn = document.getElementById('start-btn');
            const stopBtn = document.getElementById('stop-btn');
            
            startBtn.onclick = function() {
              processor.onaudioprocess = function(event) {
                const audioData = event.inputBuffer.getChannelData(0);
                
                // Send audio data to Streamlit app
                Streamlit.setComponentValue(audioData);
              };
              
              startBtn.disabled = true;
              stopBtn.disabled = false;
            };
            
            // Stop recording
            stopBtn.onclick = function() {
              processor.onaudioprocess = null;
              
              startBtn.disabled = false;
              stopBtn.disabled = true;
            };
          });
        </script>
        """,
        height=300,
    )

    # Display the received audio data
    audio_data = st.experimental_get_query_params().get("audio", [None])[0]
    if audio_data:
        st.subheader("Received Audio Data")
        st.write(audio_data)

if __name__ == "__main__":
    main()
