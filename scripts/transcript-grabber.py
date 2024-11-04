from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id, language="en"):
    try:
        # Fetch transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        
        # Format and print or save transcript
        transcript_text = ""
        for entry in transcript:
            time = entry['start']
            text = entry['text']
            transcript_text += f"[{time:.2f}] {text}\n"
        
        # Save transcript to a file
        with open(f"{video_id}_transcript.txt", "w") as f:
            f.write(transcript_text)
        
        print("Transcript saved successfully.")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
video_id = ""  # Replace with actual video ID
get_transcript(video_id)
