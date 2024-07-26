import arxiv
import html
import sqlite3
import datetime
import os

# Define the folder
folder = 'arxiv'

# Define the search query and category
query = 'cat:quant-ph'
keywords = [
    'photon', 'photonic', 'nonlinear', 'spdc', 'sfwm', 
    'lithium niobate', 'integrated', 'chip',
    'sensing', 'metrology', r"cram\'er", 'estimation', 
    'tomography', 'povm', 'fidelity', 'shadow']

# Set up SQLite database
db_filename = f'./{folder}/processed_articles.db'

def setup_database():
    """Create the database and table if they do not exist."""
    with sqlite3.connect(db_filename) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id TEXT PRIMARY KEY,
                title TEXT,
                summary TEXT
            )
        ''')
        conn.commit()

def article_exists(article_id):
    """Check if the article ID already exists in the database."""
    with sqlite3.connect(db_filename) as conn:
        c = conn.cursor()
        c.execute('SELECT 1 FROM articles WHERE id = ?', (article_id,))
        return c.fetchone() is not None

def insert_article(article_id, title, summary):
    """Insert a new article into the database."""
    with sqlite3.connect(db_filename) as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO articles (id, title, summary)
            VALUES (?, ?, ?)
        ''', (article_id, title, summary))
        conn.commit()
        
def create_folder_if_not_exists(folder_path):
    # Check if the folder already exists
    if not os.path.exists(folder_path):
        # If not, create the folder
        os.makedirs(folder_path)
        print(f"Folder created: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")

# Create arXiv folder
create_folder_if_not_exists(folder)

# Set up database
setup_database()

# Perform the search
search = arxiv.Search(
    query=query,
    max_results=100,
    sort_by=arxiv.SortCriterion.SubmittedDate
)

# Function to highlight keywords
def highlight_keywords(text, keywords):
    for keyword in keywords:
        keyword_escaped = html.escape(keyword)
        text = text.replace(
            keyword_escaped, 
            f'<span class="highlight">{keyword_escaped}</span>'
        )
        text = text.replace(
            keyword_escaped.lower(), 
            f'<span class="highlight">{keyword_escaped.lower()}</span>'
        )
        text = text.replace(
            keyword_escaped.capitalize(), 
            f'<span class="highlight">{keyword_escaped.capitalize()}</span>'
        )
    return text

# Filter articles and update database
selected_articles = []
for result in search.results():
    article_id = result.entry_id
    if not article_exists(article_id):
        title = result.title
        summary = result.summary
        highlighted_title = highlight_keywords(title, keywords)
        highlighted_summary = highlight_keywords(summary, keywords)
        insert_article(article_id, title, summary)
        selected_articles.append((highlighted_title, highlighted_summary, article_id))

# Generate the HTML content
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Selected Articles from arXiv (quant-ph)</title>
    <style>
        .highlight {
            background-color: yellow;
        }
    </style>
    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({
          tex2jax: {
            inlineMath: [ ['$','$'] ],
            processEscapes: true
          }
        });
    </script>
    <script type="text/javascript"
            src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
    </script>
</head>
<body>
    <h1>Selected Articles from arXiv (quant-ph)</h1>
    <ul>
"""

for title, summary, url in selected_articles:
    html_content += f"""
    <li>
        <a href="{url}" target="_blank">{title}</a>
        <p>{summary}</p>
    </li>
    """

html_content += """
    </ul>
</body>
</html>
"""

date = datetime.date.today().strftime('%Y_%m_%d')
file_path = f'./{folder}/arxiv_{date}.html'

# Check if the file already exists
if os.path.exists(file_path):
    print(f"File already exists: {file_path}. Aborting the process.")
else:
    with open(file_path, 'w', encoding='UTF-8') as file:
        file.write(html_content)
    print(f"HTML file '" + file_path + "' has been created.")
