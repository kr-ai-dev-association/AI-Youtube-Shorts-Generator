from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import re

def add_subtitles_to_video(input_video, output_video, transcriptions, video_start_time=0, original_title=None, original_url=None):
    """
    Add subtitles to video based on transcription segments.
    Also adds a permanent footer with original video info.
    """
    video = VideoFileClip(input_video)
    video_duration = video.duration
    
    # Create permanent footer if title/url provided
    footer_clips = []
    if original_title or original_url:
        footer_text = ""
        if original_title:
            footer_text += f"Source: {original_title}\n"
        if original_url:
            footer_text += f"{original_url}"
            
        footer_clip = TextClip(
            footer_text.strip(),
            fontsize=20,
            color='white',
            stroke_color='black',
            stroke_width=0.5,
            font='AppleGothic',
            method='caption',
            size=(video.w - 40, None)
        ).set_position(('center', video.h - 60)).set_start(0).set_duration(video_duration).set_opacity(0.7)
        footer_clips.append(footer_clip)

    # Filter transcriptions to only those within the video timeframe
    relevant_transcriptions = []
    for text, start, end in transcriptions:
        # Adjust times relative to video start
        adjusted_start = start - video_start_time
        adjusted_end = end - video_start_time
        
        # Only include if within video duration
        if adjusted_end > 0 and adjusted_start < video_duration:
            adjusted_start = max(0, adjusted_start)
            adjusted_end = min(video_duration, adjusted_end)
            relevant_transcriptions.append([text.strip(), adjusted_start, adjusted_end])
    
    if not relevant_transcriptions:
        print("No transcriptions found for this video segment")
        video.write_videofile(output_video, codec='libx264', audio_codec='aac')
        video.close()
        return
    
    # Create text clips for each transcription segment
    text_clips = []
    
    # Scale font size proportionally to video height (~3.25% of height)
    # 1080p → 35px, 720p → 23px
    dynamic_fontsize = int(video.h * 0.0325)
    
    for text, start, end in relevant_transcriptions:
        # Clean up text
        text = text.strip()
        if not text:
            continue
            
        # Create text clip with styling
        txt_clip = TextClip(
            text,
            fontsize=dynamic_fontsize,
            color='#2699ff',
            stroke_color='black',
            stroke_width=2,
            font='AppleGothic',  # macOS standard font that supports Korean
            method='caption',
            size=(video.w - 100, None)  # Leave 50px margin on each side
        )
        
        # Position at top center
        txt_clip = txt_clip.set_position(('center', 100))  # 100px from top
        txt_clip = txt_clip.set_start(start)
        txt_clip = txt_clip.set_duration(end - start)
        
        text_clips.append(txt_clip)
    
    # Composite video with subtitles and footer
    print(f"Adding {len(text_clips)} subtitle segments and footer to video...")
    final_video = CompositeVideoClip([video] + footer_clips + text_clips)
    
    # Write output
    final_video.write_videofile(
        output_video,
        codec='libx264',
        audio_codec='aac',
        fps=video.fps,
        preset='medium',
        bitrate='3000k'
    )
    
    video.close()
    final_video.close()
    print(f"✓ Subtitles added successfully -> {output_video}")
