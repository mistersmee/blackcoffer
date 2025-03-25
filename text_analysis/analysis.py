import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import re
import textstat
from nltk.tokenize import sent_tokenize, word_tokenize

# Load the input Excel file
input_file = "Input.xlsx"
df = pd.read_excel(input_file)

# Ensure required columns exist
if not {"URL_ID", "URL"}.issubset(df.columns):
    raise ValueError("Input Excel file must contain 'URL_ID' and 'URL' columns")

# Directories for stopwords and sentiment analysis
stopwords_dir = "StopWords/"
sentiment_dir = "MasterDictionary/"

# Directory to save extracted articles
output_dir = "articles"
os.makedirs(output_dir, exist_ok=True)

# Load custom stopwords
def load_stopwords():
    stopwords = set()
    for file in os.listdir(stopwords_dir):
        if file.endswith(".txt"):
            try:
                with open(os.path.join(stopwords_dir, file), "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        clean_word = line.split("|")[0].strip().lower()  # Convert to lowercase
                        if clean_word:
                            stopwords.add(clean_word)
            except UnicodeDecodeError:
                with open(os.path.join(stopwords_dir, file), "r", encoding="latin-1", errors="ignore") as f:
                    for line in f:
                        clean_word = line.split("|")[0].strip().lower()
                        if clean_word:
                            stopwords.add(clean_word)
    return stopwords

custom_stopwords = load_stopwords()

# Load sentiment words
def load_sentiment_words():
    def read_file(filepath):
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                return set(word.lower() for word in f.read().splitlines())  # Convert to lowercase
        except UnicodeDecodeError:
            with open(filepath, "r", encoding="latin-1", errors="ignore") as f:
                return set(word.lower() for word in f.read().splitlines())

    positive_words = read_file(os.path.join(sentiment_dir, "positive-words.txt"))
    negative_words = read_file(os.path.join(sentiment_dir, "negative-words.txt"))
    return positive_words, negative_words

positive_words, negative_words = load_sentiment_words()

# Function to extract article text from the provided HTML structure
def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('title').text.strip() if soup.find('title') else ""

        # Extract text only from div with class "td-post-content"
        content_div = soup.find("div", class_="td-post-content")
        if content_div:
            elements = content_div.find_all(["p", "h1", "h2", "h3"])
            text = "\n".join(el.get_text(strip=True) for el in elements if el.get_text(strip=True))
        else:
            text = ""

        stop_phrases = ["Contact Details"]
        for phrase in stop_phrases:
            if phrase.lower() in text.lower():
                text = text[:text.lower().find(phrase.lower())].strip()
                break

        return title, text
    except Exception as e:
        print(f"Failed to extract text from {url}: {e}")
        return "", ""

# Function to analyze text
def analyze_text(text):
    words = word_tokenize(text)
    sentences = sent_tokenize(text)
    words_filtered = [w.lower() for w in words if w.isalnum() and w.lower() not in custom_stopwords]

    word_count = len(words_filtered)
    sentence_count = len(sentences)
    avg_sentence_length = word_count / sentence_count if sentence_count else 0

    complex_words = [w for w in words_filtered if textstat.syllable_count(w) > 2]
    complex_word_count = len(complex_words)
    percentage_complex_words = (complex_word_count / word_count) * 100 if word_count else 0

    fog_index = textstat.gunning_fog(text)
    avg_words_per_sentence = word_count / sentence_count if sentence_count else 0
    syllables_per_word = textstat.syllable_count(text) / word_count if word_count else 0
    avg_word_length = sum(len(w) for w in words_filtered) / word_count if word_count else 0

    # Sentiment Analysis
    positive_score = sum(1 for w in words_filtered if w in positive_words)
    negative_score = sum(1 for w in words_filtered if w in negative_words)
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (word_count + 0.000001)

    # Personal pronouns
    pronouns = re.findall(r'\b(I|we|my|ours|us|me|mine|our)\b', text, re.I)
    personal_pronouns = len(pronouns)

    return [positive_score, negative_score, polarity_score, subjectivity_score, avg_sentence_length,
            percentage_complex_words, fog_index, avg_words_per_sentence, complex_word_count,
            word_count, syllables_per_word, personal_pronouns, avg_word_length]

# Process each URL
results = []
for index, row in df.iterrows():
    url_id, url = row['URL_ID'], row['URL']
    title, text = extract_text_from_url(url)

    if text:
        # Save article text
        file_path = os.path.join(output_dir, f"{url_id}.txt")
        with open(file_path, "w", encoding="utf-8", errors="ignore") as f:
            f.write(text)

        # Analyze text
        analysis = analyze_text(text)
        results.append([url_id, url] + analysis)

# Save results to a new Excel file
output_columns = ["URL_ID", "URL", "POSITIVE SCORE", "NEGATIVE SCORE", "POLARITY SCORE", "SUBJECTIVITY SCORE",
                  "AVG SENTENCE LENGTH", "PERCENTAGE OF COMPLEX WORDS", "FOG INDEX", "AVG NUMBER OF WORDS PER SENTENCE",
                  "COMPLEX WORD COUNT", "WORD COUNT", "SYLLABLE PER WORD", "PERSONAL PRONOUNS", "AVG WORD LENGTH"]
output_df = pd.DataFrame(results, columns=output_columns)
output_df.to_excel("output.xlsx", index=False)

print("Processing complete. Analysis saved to output.xlsx")
