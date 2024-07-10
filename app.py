import os
import streamlit as st
from moviepy.editor import VideoFileClip

# Function to extract audio from video
def extract_audio(video_path):
    clip = VideoFileClip(video_path)
    audio_clip = clip.audio
    temp_audio_path = os.path.join('temp', 'extracted_audio.wav')
    audio_clip.write_audiofile(temp_audio_path)
    return temp_audio_path

# Function to remove audio from video
def remove_audio(video_path):
    clip = VideoFileClip(video_path)
    video_no_audio = clip.without_audio()
    temp_video_no_audio_path = os.path.join('temp', 'video_no_audio.mp4')
    video_no_audio.write_videofile(temp_video_no_audio_path)
    return temp_video_no_audio_path

# Main function for Streamlit app
def main():
    st.title('Video Audio Extractor and Remover')
    st.write('Upload a video file to extract audio or remove audio')

    uploaded_file = st.file_uploader("Choose a video file", type=['mp4', 'mov', 'avi'])

    temp_dir = 'temp'
    os.makedirs(temp_dir, exist_ok=True)  # Ensure temp directory exists

    if uploaded_file is not None:
        video_path = os.path.join(temp_dir, uploaded_file.name)
        with open(video_path, 'wb') as f:
            f.write(uploaded_file.read())
        st.success('Video successfully uploaded.')

        if st.button('Extract Audio'):
            st.write('Extracting audio...')
            audio_path = extract_audio(video_path)
            st.success('Audio extracted successfully!')
            st.audio(audio_path, format='audio/wav')
            st.write('Extracted Audio')  # Add caption here

        if st.button('Remove Audio'):
            st.write('Removing audio...')
            video_no_audio_path = remove_audio(video_path)
            st.success('Audio removed successfully!')
            st.video(video_no_audio_path)
            with open(video_no_audio_path, 'rb') as f:
                st.download_button(
                    label="Download video without audio",
                    data=f,
                    file_name='video_no_audio.mp4',
                    mime='video/mp4'
                )
            st.write('Video without audio')  # Add caption here

    # Clean up temporary directory
    if os.path.exists(temp_dir):
        for file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                st.error(f"Error cleaning up temporary files: {e}")

if __name__ == "__main__":
    main()
