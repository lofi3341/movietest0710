import os
import streamlit as st
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

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
    clip.write_videofile(temp_video_no_audio_path, codec='libx264', threads=4)
    return temp_video_no_audio_path

def convert_video(video_path):
    # Extract audio
    audio_path = extract_audio(video_path)

    # Remove audio from video
    video_no_audio_path = remove_audio(video_path)

    # Load clips
    audio_clip = AudioFileClip(audio_path)
    video_clip = VideoFileClip(video_no_audio_path)

    # Set audio to video
    final_clip = video_clip.set_audio(audio_clip)

    # Save final video
    final_video_path = os.path.join('temp', 'final_video.mp4')
    final_clip.write_videofile(final_video_path, codec='libx264', audio_codec='aac', threads=4)
    return final_video_path

def main():
    st.title('Video Audio Converter')
    st.write('Upload a video file and convert it by extracting audio and removing audio.')

    uploaded_file = st.file_uploader("Choose a video file", type=['mp4', 'mov', 'avi'])

    temp_dir = 'temp'
    os.makedirs(temp_dir, exist_ok=True)

    if uploaded_file is not None:
        video_path = os.path.join(temp_dir, uploaded_file.name)
        with open(video_path, 'wb') as f:
            f.write(uploaded_file.read())
        st.success('Video successfully uploaded.')

        if st.button('Convert'):
            st.write('Converting video...')
            final_video_path = convert_video(video_path)
            st.success('Video converted successfully!')

            with open(final_video_path, 'rb') as file:
                st.download_button(
                    label='Download Converted Video',
                    data=file,
                    file_name='final_video.mp4',
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