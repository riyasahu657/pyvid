import streamlit as st
from pytubefix import YouTube
import os

st.set_page_config(page_title="YT Downloader", page_icon="🎬")

st.title("🎬 YouTube Video & Music Downloader")
st.write("Download YouTube videos or audio using Python + Streamlit")

url = st.text_input("🔗 Enter YouTube Video URL")

download_type = st.radio(
    "Select Download Type",
    ("🎥 Video", "🎵 Audio (MP3)")
)

if url:
    try:
        yt = YouTube(url)
        st.success(f"📌 Title: {yt.title}")

        if download_type == "🎥 Video":
            streams = yt.streams.filter(progressive=True, file_extension="mp4")
            resolutions = [s.resolution for s in streams]

            choice = st.selectbox("Select Quality", resolutions)

            if st.button("⬇ Download Video"):
                stream = streams.filter(resolution=choice).first()
                file_path = stream.download(output_path="downloads")
                st.success("✅ Video Downloaded!")
                st.write(file_path)

        else:
            if st.button("⬇ Download Audio"):
                audio = yt.streams.filter(only_audio=True).first()
                file_path = audio.download(output_path="downloads")

                base, ext = os.path.splitext(file_path)
                mp3_path = base + ".mp3"
                os.rename(file_path, mp3_path)

                st.success("✅ Audio Downloaded (MP3)")
                st.write(mp3_path)

    except Exception as e:
        st.error(f"❌ Error: {e}")
