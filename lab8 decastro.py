import re
import spacy
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from textblob import TextBlob
from nltk.corpus import stopwords
import nltk

# Download NLTK stopwords if not already
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Initialize spaCy model (make sure to install it first: python -m spacy download en_core_web_sm)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Error: spaCy model 'en_core_web_sm' not found. Please install it with:")
    print("python -m spacy download en_core_web_sm")
    exit(1)

articles = [
    """
    Manila is experiencing worsening air pollution due to increasing vehicular emissions
    and construction activities. Environmental groups warn that Metro Manila's smog
    levels are approaching dangerous levels, urging LGUs to implement stricter air quality
    monitoring systems. Climate advocates say the Philippine government must prioritize
    renewable energy solutions in Manila.
    """,
    """
    In Cebu City, local officials launched an expanded waste segregation program after
    reports showed rising plastic pollution in nearby rivers. Volunteers from different
    barangays participated in the cleanup drive along the Guadalupe River in Cebu, noting tons
    of single-use plastics recovered during the effort. Cebu City government says this is part
    of a long-term environmental rehabilitation plan.
    """,
    """
    Davao del Sur recorded unusually high temperatures this year, which experts link to
    rapid deforestation and loss of tree cover. Environmental scientists warn that if
    agricultural lands continue to expand without regulation, Davao may face severe
    water shortages and declining crop yield.
    """,
    """
    In Baguio City, landslide-prone areas are increasing due to soil erosion and irresponsible
    hillside construction. Residents expressed concern after multiple small landslides occurred
    near Marcos Highway in Baguio. Authorities urge stricter building regulations to prevent
    further environmental degradation.
    """,
    """
    Zamboanga City reported an oil spill affecting coastal communities in Talon-Talon and
    Rio Hondo. Fisherfolk experienced major losses as marine life in Zamboanga declined rapidly.
    Environmental groups call for immediate cleanup operations.
    """,
    """
    Iloilo City launched a mangrove reforestation program aimed at restoring degraded
    coastal ecosystems. Local youth organizations joined the planting activities in
    coastal barangays in Iloilo, saying the initiative protects communities from storm surges.
    """,
    """
    In Pampanga, lahar-affected areas continue to show signs of soil instability. Residents of
    Porac and Mabalacat in Pampanga reported cracks in farmlands following heavy rainfall.
    Experts warn that improper quarrying may worsen erosion.
    """,
    """
    General Santos City recorded a spike in water pollution after chemical waste was found
    in a creek in Barangay Tambler. Authorities in GenSan coordinated with environmental
    agencies to prevent contamination in Sarangani Bay.
    """,
    """
    Cagayan de Oro continues to battle river pollution due to illegal dumping and poor
    wastewater treatment practices. Environmental watchdogs warn that heavy metals
    were detected in Cagayan River, prompting stricter LGU enforcement.
    """,
    """
    In Palawan, conservationists raised alarms over increasing cases of wildlife trafficking,
    especially in Puerto Princesa. Authorities rescued several endangered animals across Palawan.
    """
]

def clean_text(text):
    """Clean text by converting to lowercase and removing special characters"""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)  # Keep only letters and spaces
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    return text.strip()

def get_sentiment(text):
    """Analyze sentiment of text using TextBlob"""
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

def extract_locations(text):
    """Extract location entities from text using spaCy"""
    doc = nlp(text)
    locations = []
    for ent in doc.ents:
        if ent.label_ == "GPE":  # GPE = Geo-Political Entity
            locations.append(ent.text)
    return list(set(locations))  # Remove duplicates

def main():
    # Clean articles
    cleaned_articles = [clean_text(a) for a in articles]

    # Analyze sentiments
    sentiments = [get_sentiment(a) for a in cleaned_articles]

    # Extract all words for word cloud and bar chart
    all_words = [w for w in " ".join(cleaned_articles).split() if w not in stop_words]

    # Extract locations
    locations = []
    article_locations = []

    for art in articles:
        locs = extract_locations(art)
        locations.extend(locs)
        article_locations.append(locs)

    # Count location frequencies
    location_counts = Counter(locations)

    # Map words to locations
    location_word_map = {}
    for i, locs in enumerate(article_locations):
        words = cleaned_articles[i].split()
        for loc in locs:
            if loc not in location_word_map:
                location_word_map[loc] = []
            location_word_map[loc].extend(words)

    # Get top words per location
    top_words_per_location = {
        loc: Counter(words).most_common(10)
        for loc, words in location_word_map.items()
    }

    # 1. Generate and display Word Cloud
    print("Generating Word Cloud...")
    wc = WordCloud(
        width=1000,
        height=600,
        background_color="white",
        max_words=100,
        colormap="viridis"
    )
    wc.generate(" ".join(cleaned_articles))

    plt.figure(figsize=(12, 6))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title("Environmental News Word Cloud (Philippines)", fontsize=18, pad=20)
    plt.tight_layout()
    plt.show()

    # 2. Display location frequency bar chart
    print("Generating Location Frequency Chart...")
    if location_counts:
        plt.figure(figsize=(10, 6))
        locations_sorted = dict(sorted(location_counts.items(), key=lambda x: x[1], reverse=True))
        plt.bar(locations_sorted.keys(), locations_sorted.values(), color='steelblue', edgecolor='black')
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)
        plt.title("Most Mentioned Locations in Environmental Articles", fontsize=16, pad=20)
        plt.xlabel("Location", fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        plt.tight_layout()
        plt.show()
    else:
        print("No locations found for chart.")

    # 3. Display most mentioned words bar chart
    print("Generating Most Mentioned Words Chart...")
    word_counts = Counter(all_words)
    most_common_words = word_counts.most_common(15)  # Top 15 words
    words, counts = zip(*most_common_words)

    plt.figure(figsize=(12, 6))
    plt.bar(words, counts, color='darkorange', edgecolor='black')
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.title("Top 15 Most Mentioned Words in Environmental Articles", fontsize=16, pad=20)
    plt.xlabel("Word", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.show()

    # 4. Print text results
    print("\n" + "="*50)
    print("SENTIMENT ANALYSIS RESULTS")
    print("="*50)
    for i, (sent, art) in enumerate(zip(sentiments, articles[:3]), 1):  # Show first 3 for brevity
        print(f"\nArticle {i}: {sent}")
        print(f"Preview: {art[:100]}...")

    print(f"\nSentiment Distribution:")
    sentiment_dist = Counter(sentiments)
    for sent, count in sentiment_dist.items():
        print(f" {sent}: {count} articles ({count/len(sentiments)*100:.1f}%)")

    print("\n" + "="*50)
    print("LOCATION ANALYSIS")
    print("="*50)
    print(f"\nTotal unique locations mentioned: {len(location_counts)}")

    if location_counts:
        print("\nTop 5 locations by frequency:")
        for loc, freq in location_counts.most_common(5):
            print(f" {loc}: {freq} mentions")

    print("\n" + "="*50)
    print("TOP WORDS PER LOCATION")
    print("="*50)

    if top_words_per_location:
        # Show top 3 locations for brevity
        for i, (loc, words) in enumerate(top_words_per_location.items()):
            if i >= 3:  # Limit output
                print(f"\n... and {len(top_words_per_location)-3} more locations")
                break
            print(f"\n{loc}:")
            for w, f in words[:5]:  # Show top 5 words per location
                print(f" {w}: {f}")

if __name__ == "__main__":
    main()
