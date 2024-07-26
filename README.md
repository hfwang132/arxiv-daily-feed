# arXiv daily feed
Personal arXiv feed with filtered keywords in an html.

# Usage

- Update the arXiv category and keywords in myarxiv.py to match your interests.
- Run `python myarxiv.py`
- Open `./arxiv/arxiv_*.html` with any browser and enjoy!
- You can run this script from time to time. New feeds will be created and will not duplicate existing ones.

# Output

- A folder named `./arxiv`
- A database `./arxiv/processed_articles.db` that avoids repeated articles
- An html `./arxiv/arxiv_{date}.html` with articles filtered with keywords
