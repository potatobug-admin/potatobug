from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import os

# Set up your API keys
youtube_api_key = ''  # Replace with your YouTube API key or set as an environment variable
openai.api_key = ''    # Replace with your OpenAI API key or set as an environment variable

# Function to get video title
def get_video_title(video_id):
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()
    if "items" in response and len(response['items']) > 0:
        return response['items'][0]['snippet']['title']
    else:
        print(f"Title not found for video {video_id}")
        return f"Video {video_id}"

# Function to get transcript for a video
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        print(f"Error retrieving transcript for video {video_id}: {e}")
        return None

# Function to create an AsciiDoc file based on video title and content
def create_asciidoc_file(video_id, title, content):
    safe_title = ''.join(char if char.isalnum() or char in "._-" else "_" for char in title)
    file_path = f"{safe_title}_{video_id}.adoc"

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return file_path

# Function to analyze transcript content with ChatGPT
def analyze_transcript_with_chatgpt(transcript_text):
    messages = [
        {"role": "user", "content": f"""
Please analyze the following YouTube transcript. Provide the following:
1. A brief summary of the discussed topics.
2. A list of arguments presented by the content creator, including references to Islamic sources and any rebuttals to guest counterpoints.
3. Ensure only high-quality Islamic sources that are well-accepted by the Sunni community are referenced.
4. For each reference, include a quote with the YouTube timestamp and a URL to view the reference.

Transcript:
{transcript_text}
"""}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
        messages=messages,
        max_tokens=1500,  # Adjust this based on your needs and model limits
        temperature=0.5
    )

    return response['choices'][0]['message']['content'].strip()

# Function to format ChatGPT's output into AsciiDoc format
def format_asciidoc_content(title, analysis):
    content = f"""= {title}

== Analysis
{analysis}
"""
    return content

# Main function to process a single video
def process_single_video(video_id):
    # Step 1: Get the video title
    title = get_video_title(video_id)

    # Step 2: Get the transcript for the video
    transcript = get_transcript(video_id)
    if not transcript:
        print(f"Skipping video {video_id} due to missing transcript.")
        return

    transcript_text = ' '.join([entry['text'] for entry in transcript])

    # Step 3: Analyze content with ChatGPT
    analysis = analyze_transcript_with_chatgpt(transcript_text)

    # Step 4: Format content in AsciiDoc
    formatted_content = format_asciidoc_content(title, analysis)

    # Step 5: Create and save AsciiDoc file
    create_asciidoc_file(video_id, title, formatted_content)
    print(f"AsciiDoc file created for video {video_id}")

# Run the main function with a specific video ID
if __name__ == "__main__":
    video_id = ''  # Replace with the actual video ID you want to process
    process_single_video(video_id)
