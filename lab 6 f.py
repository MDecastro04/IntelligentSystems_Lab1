import pandas as pd
import random
import re

class MovieSuggestionSystem:
    def __init__(self):
        self.movie_collection = []
        self.user_preferences = {}
        self.feedback_log = []
        self.genre_importance = {}
        self.liked_movies = set()
        self.disliked_movies = set()
        
        self.initialize_movie_database()
        print(f"\nSystem ready with {len(self.movie_collection):,} movies")
    
    def initialize_movie_database(self):
        """Initialize the movie database."""
        print("Loading movie catalog...")
        
        try:
            movie_data = pd.read_csv('movies.csv')
            total_movies = len(movie_data)
            print(f"Found {total_movies:,} movie entries")
            
            for idx, movie_entry in movie_data.iterrows():
                try:
                    movie_id = int(movie_entry['movieId'])
                    title = str(movie_entry['title']).strip()
                    
                    # Extract genres
                    genres = []
                    if pd.notna(movie_entry['genres']) and str(movie_entry['genres']) != '(no genres listed)':
                        genres = str(movie_entry['genres']).split('|')
                    
                    # Extract title and year
                    clean_title = title
                    year = None
                    
                    year_pattern = r'\((\d{4})\)'
                    year_match = re.search(year_pattern, title)
                    if year_match:
                        year = int(year_match.group(1))
                        clean_title = re.sub(r'\s*\(\d{4}\)', '', title).strip()
                    
                    # Determine cast based on genres
                    actors = []
                    genre_actors = {
                        'Action': ['Dwayne Johnson', 'Keanu Reeves', 'Charlize Theron'],
                        'Comedy': ['Kevin Hart', 'Tina Fey', 'Will Ferrell'],
                        'Drama': ['Anthony Hopkins', 'Frances McDormand', 'Daniel Day-Lewis'],
                        'Horror': ['Vera Farmiga', 'Patrick Wilson', 'Tony Todd'],
                        'Romance': ['Timothee Chalamet', 'Zendaya', 'Henry Golding'],
                        'Sci-Fi': ['Chris Pine', 'Zoe Saldana', 'Michael B. Jordan'],
                        'Animation': ['Jack Black', 'Anya Taylor-Joy', 'Chris Pratt']
                    }
                    
                    for genre in genres:
                        if genre in genre_actors:
                            actors.extend(genre_actors[genre])
                    
                    actors = list(dict.fromkeys(actors))[:4]
                    
                    # Assign director
                    director_assignment = {
                        'Action': 'Michael Bay',
                        'Comedy': 'Paul Feig',
                        'Drama': 'David Fincher',
                        'Horror': 'James Wan',
                        'Romance': 'Jon M. Chu',
                        'Sci-Fi': 'Denis Villeneuve',
                        'Animation': 'Pete Docter'
                    }
                    
                    selected_director = 'Guillermo del Toro'
                    for genre in genres:
                        if genre in director_assignment:
                            selected_director = director_assignment[genre]
                            break
                    
                    # Determine rating
                    rating_levels = {
                        'Horror': 'R',
                        'Crime': 'R', 
                        'Children': 'PG',
                        'Animation': 'PG'
                    }
                    
                    rating = 'PG-13'
                    for genre in genres:
                        if genre in rating_levels:
                            rating = rating_levels[genre]
                            break
                    
                    if rating == 'PG-13':
                        rating = random.choice(['PG-13', 'PG', 'R'])
                    
                    # Create movie description
                    if genres:
                        primary_genre = genres[0].lower()
                        themes = ['relationships', 'conflict', 'journey', 'identity', 'survival', 'transformation']
                        description = f"A cinematic exploration of {random.choice(themes)} through {primary_genre} storytelling."
                    else:
                        description = "A compelling cinematic experience."
                    
                    # Define keywords
                    keywords = [genre.lower() for genre in genres[:3]]
                    if 'Action' in genres:
                        keywords.extend(['thrilling', 'spectacle', 'explosive'])
                    if 'Comedy' in genres:
                        keywords.extend(['hilarious', 'entertaining', 'lighthearted'])
                    if 'Drama' in genres:
                        keywords.extend(['profound', 'meaningful', 'intense'])
                    
                    keywords = list(dict.fromkeys(keywords))[:6]
                    
                    # Quality rating
                    quality_score = round(random.uniform(2.8, 4.9), 1)
                    
                    self.movie_collection.append({
                        'movie_id': movie_id,
                        'title': clean_title,
                        'year': year,
                        'genres': genres,
                        'rating': rating,
                        'quality_score': quality_score,
                        'actors': actors,
                        'director': selected_director,
                        'keywords': keywords,
                        'description': description
                    })
                    
                except Exception:
                    continue
            
            print(f"Successfully loaded {len(self.movie_collection):,} movies")
                
        except Exception as e:
            print(f"Data loading issue: {e}")
            self.load_example_movies()
    
    def load_example_movies(self):
        """Load example movies if CSV is unavailable."""
        print("Using example movie database...")
        
        example_movies = [
            {
                'movie_id': 101,
                'title': 'Inception',
                'year': 2010,
                'genres': ['Sci-Fi', 'Thriller', 'Action'],
                'rating': 'PG-13',
                'quality_score': 4.7,
                'actors': ['Leonardo DiCaprio', 'Joseph Gordon-Levitt'],
                'director': 'Christopher Nolan',
                'keywords': ['dream', 'mind', 'reality'],
                'description': 'A thief who steals corporate secrets through dream-sharing technology'
            },
            {
                'movie_id': 102,
                'title': 'Parasite',
                'year': 2019,
                'genres': ['Drama', 'Thriller', 'Comedy'],
                'rating': 'R',
                'quality_score': 4.8,
                'actors': ['Song Kang-ho', 'Lee Sun-kyun'],
                'director': 'Bong Joon Ho',
                'keywords': ['class', 'family', 'society'],
                'description': 'Greed and class discrimination threaten the newly formed symbiotic relationship'
            },
            {
                'movie_id': 103,
                'title': 'La La Land',
                'year': 2016,
                'genres': ['Musical', 'Romance', 'Drama'],
                'rating': 'PG-13',
                'quality_score': 4.4,
                'actors': ['Ryan Gosling', 'Emma Stone'],
                'director': 'Damien Chazelle',
                'keywords': ['music', 'dreams', 'hollywood'],
                'description': 'A jazz pianist falls for an aspiring actress in Los Angeles'
            }
        ]
        
        self.movie_collection = example_movies
    
    def collect_user_preferences(self):
        """Collect user movie preferences."""
        print("\n" + "-" * 45)
        print("MOVIE PREFERENCE SETUP")
        print("-" * 45)
        
        # Genre preferences
        print("\nWhat movie genres interest you? (comma separated)")
        print("Options: Action, Comedy, Drama, Sci-Fi, Romance, Horror, Animation")
        genre_input = input("Please enter an input: ").strip()
        self.user_preferences['genres'] = [g.strip().lower() for g in genre_input.split(',')] if genre_input else []
        
        # Rating preference
        print("\nMaximum rating preferred:")
        print("Choices: G, PG, PG-13, R")
        rating_input = input("Please enter an input: ").strip().upper()
        self.user_preferences['rating_limit'] = rating_input if rating_input in ['G', 'PG', 'PG-13', 'R'] else None
        
        # Actor/director preferences
        print("\nFavorite actors or directors (optional, comma separated):")
        print("Examples: Meryl Streep, Steven Spielberg, Viola Davis")
        actor_input = input("Please enter an input: ").strip()
        self.user_preferences['favorite_people'] = [a.strip().lower() for a in actor_input.split(',')] if actor_input else []
        
        # Keyword preferences
        print("\nWhat themes or elements interest you? (optional, comma separated)")
        print("Examples: superhero, historical, mystery, fantasy")
        keyword_input = input("Please enter an input: ").strip()
        self.user_preferences['keywords'] = [k.strip().lower() for k in keyword_input.split(',')] if keyword_input else []
        
        print("\nPreferences recorded!")
    
    def calculate_match_score(self, movie_entry):
        """Calculate match score between movie and preferences."""
        match_score = 0
        match_reasons = []
        
        if not self.user_preferences:
            return 0, []
        
        # Genre matching
        if self.user_preferences.get('genres'):
            movie_genres = [g.lower() for g in movie_entry['genres']]
            user_genres = self.user_preferences['genres']
            matched_genres = set(movie_genres) & set(user_genres)
            
            if matched_genres:
                base_score = len(matched_genres) * 2.2
                
                importance_multiplier = 1.0
                for genre in matched_genres:
                    if genre in self.genre_importance:
                        importance_multiplier += min(self.genre_importance[genre], 0.25)
                
                match_score += base_score * importance_multiplier
                match_reasons.append(f"Genres: {', '.join([g.title() for g in matched_genres])}")
        
        # Rating matching
        if self.user_preferences.get('rating_limit') and movie_entry['rating']:
            rating_hierarchy = {'G': 1, 'PG': 2, 'PG-13': 3, 'R': 4}
            movie_rating = movie_entry['rating']
            user_limit = self.user_preferences['rating_limit']
            
            if movie_rating in rating_hierarchy and user_limit in rating_hierarchy:
                if rating_hierarchy[movie_rating] <= rating_hierarchy[user_limit]:
                    match_score += 1.8
                    match_reasons.append(f"Rating: {movie_rating}")
        
        # Actor/director matching
        if self.user_preferences.get('favorite_people'):
            movie_actors = [a.lower() for a in movie_entry['actors']]
            movie_director = movie_entry['director'].lower()
            
            for person in self.user_preferences['favorite_people']:
                if person in movie_actors:
                    match_score += 1.7
                    match_reasons.append(f"Actor: {person.title()}")
                    break
                elif person in movie_director:
                    match_score += 2.2
                    match_reasons.append(f"Director: {movie_entry['director']}")
                    break
        
        # Keyword matching
        if self.user_preferences.get('keywords'):
            search_content = ' '.join([
                movie_entry['title'].lower(),
                ' '.join(movie_entry['keywords']),
                movie_entry['description'].lower()
            ])
            
            for keyword in self.user_preferences['keywords']:
                if keyword in search_content:
                    match_score += 1.2
                    match_reasons.append(f"Keyword: '{keyword}'")
                    break
        
        # Quality bonus
        if movie_entry['quality_score'] >= 4.2:
            match_score += 0.6
        
        # Normalize to 0-10 scale
        max_possible = 9.5
        normalized_score = min(match_score / max_possible * 10, 10.0)
        
        return round(normalized_score, 2), match_reasons[:2]
    
    def generate_suggestions(self, count=10):
        """Generate movie suggestions based on preferences."""
        if not self.user_preferences:
            return []
        
        suggestions = []
        
        for movie_entry in self.movie_collection:
            movie_id = movie_entry['movie_id']
            
            if movie_id in self.liked_movies or movie_id in self.disliked_movies:
                continue
            
            match_score, reasons = self.calculate_match_score(movie_entry)
            
            if match_score > 0:
                suggestions.append({
                    'movie_id': movie_id,
                    'title': movie_entry['title'],
                    'year': movie_entry['year'],
                    'genres': ', '.join(movie_entry['genres'][:3]),
                    'rating': movie_entry['rating'],
                    'quality_score': movie_entry['quality_score'],
                    'actors': ', '.join(movie_entry['actors']),
                    'director': movie_entry['director'],
                    'match_score': match_score,
                    'match_reasons': reasons
                })
        
        suggestions.sort(key=lambda x: x['match_score'], reverse=True)
        return suggestions[:count]
    
    def display_suggestions(self):
        """Display generated suggestions."""
        suggestions = self.generate_suggestions()
        
        if not suggestions:
            print("\nNo suitable suggestions found.")
            print("Consider adjusting your preferences or trying different genres.")
            return False
        
        print(f"\n" + "-" * 45)
        print(f"TOP {len(suggestions)} MOVIE SUGGESTIONS")
        print("-" * 45)
        print(f"Match scores range from 0-10 (higher is better)")
        
        for i, suggestion in enumerate(suggestions, 1):
            print(f"\n{i}. {suggestion['title']}")
            if suggestion['year']:
                print(f"   Year: {suggestion['year']}")
            print(f"   Rating: {suggestion['rating']} | Quality: {suggestion['quality_score']}/5")
            print(f"   Genres: {suggestion['genres']}")
            print(f"   Match Score: {suggestion['match_score']}/10")
            if suggestion['match_reasons']:
                print(f"   Why suggested: {', '.join(suggestion['match_reasons'])}")
        
        return True
    
    def collect_feedback(self):
        """Collect user feedback on suggestions."""
        suggestions = self.generate_suggestions()
        
        if not suggestions:
            return
        
        print("\n" + "-" * 45)
        print("PROVIDE FEEDBACK")
        print("-" * 45)
        
        # Helpfulness rating
        print("\nHow relevant were these suggestions? (1-5)")
        print("1: Not relevant, 5: Highly relevant")
        try:
            relevance_score = int(input("Please enter an input: ").strip())
            if 1 <= relevance_score <= 5:
                self.feedback_log.append({'relevance_score': relevance_score})
                print(f"Thank you! Relevance score: {relevance_score}/5")
        except:
            print("Input not recognized. Skipping relevance rating.")
        
        # Liked movies
        print(f"\nWhich movies did you like? (enter numbers 1-{len(suggestions)})")
        print("Format: 1, 3, 5 or 'none'")
        like_input = input("Please enter an input: ").strip()
        
        if like_input and like_input.lower() != 'none':
            try:
                selected_indices = [int(num.strip()) - 1 for num in like_input.split(',')]
                for idx in selected_indices:
                    if 0 <= idx < len(suggestions):
                        suggestion = suggestions[idx]
                        movie_id = suggestion['movie_id']
                        
                        self.liked_movies.add(movie_id)
                        
                        for genre in suggestion['genres'].split(', '):
                            genre = genre.strip().lower()
                            current_weight = self.genre_importance.get(genre, 0)
                            self.genre_importance[genre] = min(current_weight + 0.08, 0.25)
                        
                        print(f"Added to favorites: {suggestion['title']}")
            except:
                print("Format not recognized.")
        
        # Disliked movies
        print(f"\nWhich movies don't interest you? (enter numbers 1-{len(suggestions)})")
        dislike_input = input("Please enter an input: ").strip()
        
        if dislike_input:
            try:
                selected_indices = [int(num.strip()) - 1 for num in dislike_input.split(',')]
                for idx in selected_indices:
                    if 0 <= idx < len(suggestions):
                        suggestion = suggestions[idx]
                        movie_id = suggestion['movie_id']
                        
                        self.disliked_movies.add(movie_id)
                        
                        for genre in suggestion['genres'].split(', '):
                            genre = genre.strip().lower()
                            current_weight = self.genre_importance.get(genre, 0)
                            self.genre_importance[genre] = max(current_weight - 0.04, -0.15)
                        
                        print(f"Noted as not interested: {suggestion['title']}")
            except:
                print("Format not recognized.")
        
        print("\nFeedback incorporated. Future suggestions will be more personalized.")
    
    def demonstrate_profiles(self):
        """Demonstrate system with sample user profiles."""
        sample_profiles = [
            {
                'profile_name': 'ACTION FAN',
                'genres': ['action', 'thriller', 'adventure'],
                'rating_limit': 'PG-13',
                'favorite_people': ['dwayne johnson', 'keanu reeves'],
                'keywords': ['explosive', 'mission', 'combat']
            },
            {
                'profile_name': 'ROMANCE FAN',
                'genres': ['romance', 'drama', 'comedy'],
                'rating_limit': 'PG-13',
                'favorite_people': ['ryan gosling', 'zendaya'],
                'keywords': ['love', 'relationship', 'heartfelt']
            },
            {
                'profile_name': 'FILM BUFF',
                'genres': ['drama', 'foreign', 'indie'],
                'rating_limit': 'R',
                'favorite_people': ['anthony hopkins', 'frances mcdormand'],
                'keywords': ['artistic', 'profound', 'cinematic']
            }
        ]
        
        print("\n" + "-" * 45)
        print("DEMONSTRATION MODE")
        print("-" * 45)
        
        original_preferences = self.user_preferences.copy()
        
        for profile in sample_profiles:
            print(f"\n{profile['profile_name']}:")
            print(f"  Preferred genres: {', '.join(profile['genres'])}")
            print(f"  Rating limit: {profile['rating_limit']}")
            
            self.user_preferences = profile.copy()
            suggestions = self.generate_suggestions(5)
            
            if suggestions:
                print("  Suggested movies:")
                for i, suggestion in enumerate(suggestions[:3], 1):
                    print(f"    {i}. {suggestion['title']} (Score: {suggestion['match_score']}/10)")
            else:
                print("  No suggestions available")
        
        self.user_preferences = original_preferences
        print("\nDemonstration complete.")
    
    def show_current_preferences(self):
        """Display current preference settings."""
        print("\n" + "-" * 45)
        print("CURRENT PREFERENCES")
        print("-" * 45)
        
        if self.user_preferences:
            print(f"\nPreferred Genres: {', '.join(self.user_preferences.get('genres', []))}")
            print(f"Rating Limit: {self.user_preferences.get('rating_limit', 'Not specified')}")
            print(f"Favorite Actors/Directors: {', '.join(self.user_preferences.get('favorite_people', []))}")
            print(f"Keywords: {', '.join(self.user_preferences.get('keywords', []))}")
        else:
            print("\nNo preferences configured yet.")
        
        print(f"\nLiked movies: {len(self.liked_movies)}")
        print(f"Disliked movies: {len(self.disliked_movies)}")
        
        if self.genre_importance:
            print("\nGenre adjustment factors:")
            for genre, weight in list(self.genre_importance.items())[:4]:
                print(f"  {genre.title()}: {weight:+.2f}")
    
    def reset_all_settings(self):
        """Reset all preferences and history."""
        self.user_preferences = {}
        self.genre_importance = {}
        self.liked_movies.clear()
        self.disliked_movies.clear()
        self.feedback_log = []
        print("\nAll settings and history have been cleared.")
    
    def run(self):
        """Main program interface."""
        print("\n" + "-" * 45)
        print("MOVIE SUGGESTION SYSTEM")
        print("-" * 45)
        print(f"Database size: {len(self.movie_collection):,} movies")
        
        while True:
            print("\nMAIN MENU")
            print("1. Set Movie Preferences")
            print("2. Get Movie Suggestions")
            print("3. Demonstration Mode")
            print("4. View Current Preferences")
            print("5. Reset All Settings")
            print("6. Exit Program")
            
            try:
                choice = input("\nPlease enter an input: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n\nProgram terminated.")
                break
            
            if choice == '1':
                self.collect_user_preferences()
            
            elif choice == '2':
                if not self.user_preferences:
                    print("\nPlease set preferences first (option 1).")
                    continue
                
                suggestions_available = self.display_suggestions()
                if suggestions_available:
                    self.collect_feedback()
            
            elif choice == '3':
                self.demonstrate_profiles()
            
            elif choice == '4':
                self.show_current_preferences()
            
            elif choice == '5':
                self.reset_all_settings()
            
            elif choice == '6':
                print("\nThank you for using the Movie Suggestion System!")
                break
            
            else:
                print("Selection not recognized. Please choose 1-6.")


if __name__ == "__main__":
    movie_system = MovieSuggestionSystem()
    movie_system.run()