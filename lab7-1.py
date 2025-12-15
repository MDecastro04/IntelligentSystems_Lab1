import tkinter as tk  
from tkinter import ttk, messagebox, scrolledtext  
import pandas as pd 
from pathlib import Path  

try:  #try
    from sklearn.feature_extraction.text import TfidfVectorizer  #import
    from sklearn.neighbors import NearestNeighbors  #import
    SKLEARN_OK = True  #flag
except Exception:  #except
    SKLEARN_OK = False  #flag

BASE = Path(__file__).parent 
MOVIES_CSV = BASE / "movies.csv"
RATINGS_CSV = BASE / "ratings.csv"  

try:  #try
    movies = pd.read_csv(MOVIES_CSV) 
    ratings = pd.read_csv(RATINGS_CSV) 
except Exception as e:  
    tk.Tk().withdraw()  
    messagebox.showerror("File error", str(e)) 
    raise SystemExit(1)  

avg_ratings = ratings.groupby("movieId")["rating"].mean().to_dict()  
movies["avg_rating"] = movies["movieId"].apply(lambda x: float(avg_ratings.get(x, 0.0))) 
movies["genres"] = movies["genres"].fillna("").astype(str)  #clean

all_genres = sorted({g for gs in movies["genres"] for g in gs.split("|") if g and g != "(no genres listed)"})  #genres

if SKLEARN_OK:  
    try:  #try
        tfidf = TfidfVectorizer(stop_words="english")  #vectorizer
        genres_matrix = tfidf.fit_transform(movies["genres"])
        knn = NearestNeighbors(metric="cosine", algorithm="brute") 
        knn.fit(genres_matrix)  #train
        CONTENT_MODE = "sklearn"  #mode
    except Exception:  #except
        CONTENT_MODE = "fallback"  #mode
        genres_matrix = knn = None  
else:  #else
    CONTENT_MODE = "fallback"  #mode
    genres_matrix = knn = None 

liked_movies = []  
disliked_movies = []
current_user = None  

root = tk.Tk()  #root
root.title("Movie Recommender - Multi-Search")  
root.geometry("1300x700")  

def login_screen():  #login
    win = tk.Toplevel(root)  
    win.title("Login")  
    win.geometry("300x150")  
    win.grab_set()  

    tk.Label(win, text="Username:", font=("Segoe UI", 12)).pack(pady=10)  
    entry = tk.Entry(win, font=("Segoe UI", 12))  #entry
    entry.pack()  

    def submit():  #submit
        global current_user  #global
        if not entry.get().strip():  
            messagebox.showwarning("Empty", "Enter a username") 
            return  
        current_user = entry.get().strip()  #assign
        user_label.config(text=f"👤 Logged in as: {current_user}") 
        win.destroy()  

    tk.Button(win, text="Login", command=submit).pack(pady=10)  

root.after(100, login_screen)  #delay

user_label = tk.Label(root, text="👤 Logged in as: (none)", anchor="w")  
user_label.pack(fill="x", padx=10)  

# Multi-search frame with improved layout
search_frame = tk.Frame(root)  
search_frame.pack(fill="x", padx=10, pady=(5, 0))

# Title label for search area
tk.Label(search_frame, text="Search Movies (enter multiple titles separated by commas or new lines):", 
         font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 5))

# Multi-line text widget for multiple search terms
search_text = scrolledtext.ScrolledText(search_frame, height=4, width=60, font=("Segoe UI", 11))
search_text.pack(side="left", padx=(0, 10), fill="x", expand=True)

# Function to parse multiple search terms
def parse_search_terms(text_widget):
    """Extract and clean multiple search terms from text widget"""
    text = text_widget.get("1.0", tk.END).strip()
    if not text:
        return []
    
    # Split by commas or newlines, and clean
    terms = []
    for line in text.split('\n'):
        for term in line.split(','):
            term = term.strip()
            if term:  # Only add non-empty terms
                terms.append(term.lower())
    
    return terms

# Function to add sample search terms
def add_sample_search():
    """Add sample search terms for demonstration"""
    sample_terms = """The Matrix\nStar Wars\nToy Story\nJurassic Park\nForrest Gump"""
    search_text.delete("1.0", tk.END)
    search_text.insert("1.0", sample_terms)

# Button frame for search actions
search_buttons_frame = tk.Frame(search_frame)
search_buttons_frame.pack(side="right", fill="y")

# Search button
search_button = tk.Button(search_buttons_frame, text="🔍 Search Movies", 
                          command=lambda: search_by_title_and_genre(),
                          font=("Segoe UI", 10), bg="#4CAF50", fg="white")
search_button.pack(pady=(0, 5))

# Sample button
tk.Button(search_buttons_frame, text="Load Sample", 
          command=add_sample_search, font=("Segoe UI", 9)).pack(pady=(0, 5))

# Clear button
tk.Button(search_buttons_frame, text="Clear Search", 
          command=lambda: search_text.delete("1.0", tk.END),
          font=("Segoe UI", 9)).pack()

output_frame = tk.Frame(root)  
output_frame.pack(fill="both", expand=True, padx=10, pady=8)  

canvas = tk.Canvas(output_frame)  
scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=canvas.yview)  
scrollable = tk.Frame(canvas)  

scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))  #bind
canvas.create_window((0, 0), window=scrollable, anchor="nw")  
canvas.configure(yscrollcommand=scrollbar.set)  #config

canvas.pack(side="left", fill="both", expand=True)  
scrollbar.pack(side="right", fill="y")  

def clear_output():  #clear
    for w in scrollable.winfo_children(): 
        w.destroy()  

def show_text(text):  #show
    clear_output()  #old
    tk.Label(scrollable, text=text, justify="left", anchor="w").pack(fill="x", padx=10, pady=10)  

def require_login():  #guard
    if current_user is None:  
        messagebox.showwarning("Login", "Please login first")  #alert
        return False 
    return True 

def like_movie(mid):  #like
    if not require_login(): return  
    if mid not in liked_movies:  
        liked_movies.append(mid) 
    if mid in disliked_movies:  
        disliked_movies.remove(mid) 

def dislike_movie(mid):  #dislike
    if not require_login(): return
    if mid not in disliked_movies:  
        disliked_movies.append(mid)
    if mid in liked_movies:  
        liked_movies.remove(mid)

def render_results(df, search_terms=None): 
    clear_output()  
    
    # Show search terms used (if provided)
    if search_terms:
        term_info = tk.Frame(scrollable, pady=5, bg="#f0f0f0")
        term_info.pack(fill="x", padx=5)
        terms_text = f"Search terms: {', '.join(search_terms[:5])}"
        if len(search_terms) > 5:
            terms_text += f" and {len(search_terms) - 5} more..."
        tk.Label(term_info, text=terms_text, font=("Segoe UI", 9, "italic"),
                bg="#f0f0f0").pack(side="left", padx=10)
    
    # Show result count
    count_frame = tk.Frame(scrollable, pady=2)
    count_frame.pack(fill="x", padx=5)
    tk.Label(count_frame, text=f"Found {len(df)} movies:", 
             font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
    
    for _, r in df.iterrows():  
        mid = int(r.movieId)  #id
        row = tk.Frame(scrollable, pady=4, padx=5)  
        row.pack(fill="x")  
        text = f"{r.title} | {r.genres} |  {r.avg_rating:.1f}"  #text
        tk.Label(row, text=text, anchor="w", font=("Segoe UI", 10)).pack(side="left", fill="x", expand=True)  
        tk.Button(row, text="Like 👍", command=lambda m=mid: (like_movie(m), refresh()),
                 bg="#e8f5e9", font=("Segoe UI", 9)).pack(side="right", padx=2)  
        tk.Button(row, text="Dislike 👎", command=lambda m=mid: (dislike_movie(m), refresh()),
                 bg="#ffebee", font=("Segoe UI", 9)).pack(side="right", padx=2)  

def search_by_title_and_genre():
    if not require_login():
        return

    # Get multiple search terms
    search_terms = parse_search_terms(search_text)
    selected_genres = [g for g, v in genre_vars.items() if v.get()]

    # Validation
    if not search_terms and not selected_genres:
        messagebox.showwarning(
            "Input Required",
            "Please enter at least one movie title or select at least one genre.\n\n"
            "You can enter multiple movie titles separated by commas or new lines."
        )
        return

    res = movies.copy()  # copy dataframe

    # Filter by multiple search terms
    if search_terms:
        # Create a boolean mask for ANY of the search terms
        mask = pd.Series(False, index=res.index)
        for term in search_terms:
            mask = mask | res.title.str.lower().str.contains(term, na=False)
        res = res[mask]

    # Filter by selected genres
    if selected_genres:
        res = res[res.genres.apply(
            lambda g: all(x in g.split('|') for x in selected_genres)
        )]

    # Show results
    if res.empty:
        messagebox.showwarning(
            "No Results",
            f"No movies match your {len(search_terms)} search term(s) and selected genres."
        )
        return

    # Sort by relevance (exact matches first, then partial matches)
    if search_terms:
        def relevance_score(title):
            title_lower = title.lower()
            score = 0
            for term in search_terms:
                if term in title_lower:
                    score += 1
            return score
        
        res['relevance'] = res['title'].apply(relevance_score)
        res = res.sort_values(['relevance', 'avg_rating'], ascending=[False, False])
        res = res.drop('relevance', axis=1)

    render_results(res.head(200), search_terms)

def refresh():  #refresh
    search_by_title_and_genre()  #call

# Genre selection frame
check_frame = tk.LabelFrame(root, text="Filter by Genres", padx=10, pady=5)
check_frame.pack(fill="x", padx=10, pady=5)

genre_vars = {}  #dict
col = row = 0  
for g in all_genres:  
    v = tk.BooleanVar()  
    tk.Checkbutton(check_frame, text=g, variable=v, font=("Segoe UI", 9)).grid(row=row, column=col, sticky="w", padx=2, pady=1)  
    genre_vars[g] = v 
    col += 1  
    if col >= 8:  # Increased to 8 columns for better layout
        col = 0  
        row += 1

# Add select all/none buttons for genres
genre_btn_frame = tk.Frame(check_frame)
genre_btn_frame.grid(row=row+1, column=0, columnspan=8, pady=5)

def select_all_genres():
    for var in genre_vars.values():
        var.set(True)

def clear_all_genres():
    for var in genre_vars.values():
        var.set(False)

tk.Button(genre_btn_frame, text="Select All Genres", command=select_all_genres,
         font=("Segoe UI", 9)).pack(side="left", padx=5)
tk.Button(genre_btn_frame, text="Clear All Genres", command=clear_all_genres,
         font=("Segoe UI", 9)).pack(side="left", padx=5)

def content_recs():  #content
    if not require_login() or not liked_movies:  
        show_text("Like a movie first")
        return  
    base_mid = liked_movies[-1]  #base
    base_idx = movies[movies.movieId == base_mid].index[0]  
    recs = []  
    if CONTENT_MODE == "sklearn":  
        _, idxs = knn.kneighbors(genres_matrix[base_idx], n_neighbors=25)  #neighbors
        for idx in idxs[0][1:]: 
            r = movies.iloc[idx]  
            if r.movieId not in disliked_movies:  
                recs.append(r)  #append
    else: 
        base_genres = set(movies.at[base_idx, 'genres'].split('|'))  
        for _, r in movies.iterrows():  
            if r.movieId in disliked_movies: continue  
            if base_genres & set(r.genres.split('|')):  
                recs.append(r)  
    render_results(pd.DataFrame(recs).head(20))  

def collaborative_recs(): 
    if not require_login() or not liked_movies: 
        show_text("Like a movie first")
        return  
    liked_genres = set() 
    for mid in liked_movies:  
        liked_genres.update(movies[movies.movieId == mid].iloc[0].genres.split('|'))
    scored = [] 
    for _, r in movies.iterrows():  
        if r.movieId in liked_movies or r.movieId in disliked_movies:  
            continue 
        overlap = len(liked_genres & set(r.genres.split('|')))  #overlap
        if overlap:  
            scored.append((overlap * 2 + r.avg_rating, r))  #score
    scored.sort(key=lambda x: x[0], reverse=True)  #sort
    render_results(pd.DataFrame([r for _, r in scored[:20]]))  

def hybrid_recs():  #hybrid
    if not require_login() or not liked_movies: 
        show_text("Like a movie first")  
        return  
    base_mid = liked_movies[-1]  
    base_idx = movies[movies.movieId == base_mid].index[0]  #index
    content_idxs = set()  
    if CONTENT_MODE == "sklearn":  
        _, idxs = knn.kneighbors(genres_matrix[base_idx], n_neighbors=30)  #neighbors
        content_idxs = set(idxs[0][1:])  
    hybrid = []  #list
    for idx, r in movies.iterrows():  #loop
        if r.movieId in liked_movies or r.movieId in disliked_movies:  
            continue  #skip
        score = (1 if idx in content_idxs else 0) + (r.avg_rating / 5) * 0.6  #score
        hybrid.append((score, r)) 
    hybrid.sort(key=lambda x: x[0], reverse=True)  #sort
    render_results(pd.DataFrame([r for _, r in hybrid[:20]])) 

# Recommendation buttons frame
btns = tk.Frame(root)  
btns.pack(fill="x", padx=10, pady=10)  

tk.Button(btns, text="Content-Based Recommendations", command=content_recs,
         font=("Segoe UI", 10), bg="#2196F3", fg="white").pack(side="left", padx=5)  
tk.Button(btns, text="Collaborative Recommendations", command=collaborative_recs,
         font=("Segoe UI", 10), bg="#FF9800", fg="white").pack(side="left", padx=5)  
tk.Button(btns, text="Hybrid Recommendations", command=hybrid_recs,
         font=("Segoe UI", 10), bg="#9C27B0", fg="white").pack(side="left", padx=5)  

# Liked/Disliked movies buttons
tk.Button(btns, text="⭐ Liked Movies", 
         command=lambda: render_results(movies[movies.movieId.isin(liked_movies)]),
         font=("Segoe UI", 10)).pack(side="right", padx=5)  
tk.Button(btns, text="👎 Disliked Movies", 
         command=lambda: render_results(movies[movies.movieId.isin(disliked_movies)]),
         font=("Segoe UI", 10)).pack(side="right", padx=5)  

root.mainloop()  #main