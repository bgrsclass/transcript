import tkinter as tk
from tkinter import ttk, messagebox
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs

def get_available_languages(video_id):
    try:
        # Fetch all available languages for the video
        languages = YouTubeTranscriptApi.list_transcripts(video_id)
        return [language.language_code for language in languages]  # Return list of available language codes
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while fetching available languages: {e}")
        return []

def get_transcript():
    video_url = url_entry.get()
    preferred_language = language_combobox.get().strip().lower()
    
    try:
        # Parse the URL
        parsed_url = urlparse(video_url)
        
        # Extract video ID for short and standard URLs
        if "youtu.be" in parsed_url.netloc:
            video_id = parsed_url.path.lstrip("/")  # Get the path as video ID
        elif "youtube.com" in parsed_url.netloc:
            video_id = parse_qs(parsed_url.query).get('v', [None])[0]  # Extract 'v' parameter
        else:
            raise ValueError("Invalid YouTube URL format")
        
        # Ensure video_id was found
        if not video_id:
            raise ValueError("Video ID could not be extracted from the URL")
        
        # Get available languages for the video
        available_languages = get_available_languages(video_id)
        
        if not available_languages:
            raise ValueError("No available languages for the transcript")
        
        if preferred_language not in available_languages:
            raise ValueError(f"Transcript not available in the selected language: {preferred_language}")
        
        # Fetch the transcript in the selected language
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[preferred_language])
        
        # Replace timestamps with a period and format as a paragraph
        transcript_text.delete("1.0", tk.END)  # Clear previous text
        paragraph = ". ".join(item['text'] for item in transcript)  # Combine with period separators
        transcript_text.insert(tk.END, paragraph)
    
    except TranscriptsDisabled:
        messagebox.showerror("Error", "Transcripts are disabled for this video.")
    except NoTranscriptFound:
        messagebox.showerror("Error", "No transcript found for this video in the selected language.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def fetch_available_languages():
    video_url = url_entry.get()
    parsed_url = urlparse(video_url)
    
    # Extract video ID for short and standard URLs
    if "youtu.be" in parsed_url.netloc:
        video_id = parsed_url.path.lstrip("/")  # Get the path as video ID
    elif "youtube.com" in parsed_url.netloc:
        video_id = parse_qs(parsed_url.query).get('v', [None])[0]  # Extract 'v' parameter
    else:
        messagebox.showerror("Error", "Invalid YouTube URL format")
        return
    
    available_languages = get_available_languages(video_id)
    
    if available_languages:
        language_combobox['values'] = list(set(available_languages))  # Remove duplicates and set values
        language_combobox.set(available_languages[0])  # Set default to first available language

# Create main application window
root = tk.Tk()
root.title("YouTube Transcript Fetcher")
root.geometry("900x800")

# URL Input Section
url_label = ttk.Label(root, text="Enter YouTube URL:")
url_label.pack(pady=5)
url_entry = ttk.Entry(root, width=50)
url_entry.pack(pady=5)

# Language Selection Section (expanded with top hundred languages)
language_label = ttk.Label(root, text="Select Preferred Language:")
language_label.pack(pady=5)

# List of languages (expanded version)
languages = [
    ('en', 'English'), ('es', 'Spanish'), ('fr', 'French'), ('de', 'German'), ('it', 'Italian'),
    ('pt', 'Portuguese'), ('ja', 'Japanese'), ('zh', 'Chinese'), ('ru', 'Russian'), ('ar', 'Arabic'),
    ('ko', 'Korean'), ('hi', 'Hindi'), ('tr', 'Turkish'), ('nl', 'Dutch'), ('pl', 'Polish'),
    ('sv', 'Swedish'), ('da', 'Danish'), ('no', 'Norwegian'), ('fi', 'Finnish'), ('cs', 'Czech'),
    ('el', 'Greek'), ('ro', 'Romanian'), ('th', 'Thai'), ('hu', 'Hungarian'), ('sk', 'Slovak'),
    ('uk', 'Ukrainian'), ('he', 'Hebrew'), ('id', 'Indonesian'), ('ms', 'Malay'), ('vi', 'Vietnamese'),
    ('bg', 'Bulgarian'), ('sr', 'Serbian'), ('hr', 'Croatian'), ('lt', 'Lithuanian'), ('lv', 'Latvian'),
    ('sq', 'Albanian'), ('mk', 'Macedonian'), ('bs', 'Bosnian'), ('ca', 'Catalan'), ('gl', 'Galician'),
    ('ml', 'Malayalam'), ('ta', 'Tamil'), ('te', 'Telugu'), ('kn', 'Kannada'), ('mr', 'Marathi'),
    ('pa', 'Punjabi'), ('gu', 'Gujarati'), ('or', 'Odia'), ('as', 'Assamese'), ('ne', 'Nepali'),
    ('km', 'Khmer'), ('my', 'Burmese'), ('lo', 'Lao'), ('si', 'Sinhala'), ('bn', 'Bengali'),
    ('ur', 'Urdu'), ('iw', 'Hebrew'), ('cy', 'Welsh'), ('hy', 'Armenian'), ('fa', 'Persian'),
    ('sw', 'Swahili'), ('zu', 'Zulu'), ('jv', 'Javanese'), ('am', 'Amharic'), ('eu', 'Basque'),
    ('so', 'Somali'), ('sa', 'Sanskrit'), ('az', 'Azerbaijani'), ('ka', 'Georgian'), ('af', 'Afrikaans'),
    ('eo', 'Esperanto')
] 

# Populate combobox with the full list of languages
language_combobox = ttk.Combobox(root, width=20)
language_combobox['values'] = [lang[1] for lang in languages]  # Extract language names
language_combobox.set("English")  # Default to English
language_combobox.pack(pady=5)

# Fetch Button
fetch_button = ttk.Button(root, text="Fetch Transcript", command=get_transcript)
fetch_button.pack(pady=10)

# Transcript Display Section
transcript_text = tk.Text(root, wrap=tk.WORD, height=35, width=100)
transcript_text.pack(pady=10)

# URL Entry change listener
url_entry.bind("<FocusOut>", lambda event: fetch_available_languages())

# Run the application
root.mainloop()
