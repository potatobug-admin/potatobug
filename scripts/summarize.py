import openai
import argparse

# Set up OpenAI API key
openai.api_key = ''  # Replace with your actual API key

def read_transcript_from_file(filename):
    """Read the transcript from a given filename."""
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        exit(1)

def summarize_transcript(transcript_text):
    # Split the transcript text if it's too long to fit in one request
    max_tokens = 4096  # for GPT-4-32k, adjust based on your plan
    if len(transcript_text) > max_tokens:
        transcript_text = transcript_text[:max_tokens]  # truncate for simplicity

    # Send the transcript to ChatGPT for summarization
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes YouTube transcripts."},
            {"role": "user", "content": f"Please summarize the following transcript:\n\n{transcript_text}"}
        ],
        max_tokens=500,  # Adjust the max_tokens for the response length you want
        temperature=0.5  # Controls randomness; lower values mean more focused output
    )

    # Extract summary text
    summary = response['choices'][0]['message']['content']
    return summary

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Summarize a YouTube transcript from a text file.")
    parser.add_argument('filename', type=str, help="The filename of the transcript text file")

    # Parse arguments
    args = parser.parse_args()

    # Read the transcript from file
    transcript_text = read_transcript_from_file(args.filename)

    # Get the summary
    summary = summarize_transcript(transcript_text)
    print("Summary of the transcript:\n")
    print(summary)

if __name__ == "__main__":
    main()
