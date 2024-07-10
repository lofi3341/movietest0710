import os
import streamlit as st
from moviepy.editor import VideoFileClip

def extract_audio(video_path):
    clip = VideoFileClip(video_path)
    temp_audio_path = os.path.join('temp', 'extracted_audio.wav')
    audio_clip = clip.audio
    audio_clip.write_audiofile(temp_audio_path)
    return temp_audio_path

def remove_audio(video_path):
    clip = VideoFileClip(video_path)
    temp_video_no_audio_path = os.path.join('temp', 'video_no_audio.mp4')
    clip = clip.without_audio()
    clip.write_videofile(temp_video_no_audio_path, codec='libx264', threads=4)  # threadsを追加してみる
    return temp_video_no_audio_path

def main():
    st.title('Video Audio Extractor')
    st.write('Upload a video file and extract or remove audio.')

    uploaded_file = st.file_uploader("Choose a video file", type=['mp4', 'mov', 'avi'])

    temp_dir = 'temp'
    os.makedirs(temp_dir, exist_ok=True)

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

        if st.button('Remove Audio and Download Video'):
            st.write('Removing audio...')
            video_no_audio_path = remove_audio(video_path)
            st.success('Audio removed successfully!')

            with open(video_no_audio_path, 'rb') as file:
                btn = st.download_button(
                    label='Download Video without Audio',
                    data=file,
                    file_name='video_no_audio.mp4',
                    mime='video/mp4'
                )

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