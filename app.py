from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Connexion à la base de données SQLite
def get_db_connection():
    conn = sqlite3.connect("blog.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Pour avoir des résultats sous forme de dictionnaire
    return conn

# Création de la table des articles (à faire une seule fois)
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY,
        title TEXT,
        content TEXT
    )
    """)
    conn.commit()
    conn.close()

create_table()  # Appel de la fonction pour créer la table au démarrage

# Page d'accueil
@app.route("/")
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles")
    articles = cursor.fetchall()
    conn.close()
    
    articles_html = "".join([f"""
        <h2>{article['title']}</h2>
        <p>{article['content']}</p>
        <form method="post" action="/delete">
            <input type="hidden" name="id" value="{article['id']}">
            <input type="submit" value="Supprimer">
        </form>
        <hr>
    """ for article in articles])
    
    return f"""
        <h1>Blog</h1>
        {articles_html}
        <a href='/add'>Ajouter un article</a>
    """

# Ajouter un article
@app.route("/add", methods=["GET", "POST"])
def add_article():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        
        # Sécurisation de l'insertion avec des paramètres
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO articles (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()
        
        return "Article ajouté avec succès ! <a href='/'>Retour au blog</a>"

    return """
        <h2>Ajouter un article</h2>
        <form method="post">
            Titre : <input type="text" name="title"><br>
            Contenu : <textarea name="content"></textarea><br>
            <input type="submit" value="Publier">
        </form>
    """

# Supprimer un article
@app.route("/delete", methods=["POST"])
def delete_article():
    article_id = request.form["id"]
    
    # Sécurisation de la suppression avec des paramètres
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles WHERE id = ?", (article_id,))
    conn.commit()
    conn.close()
    
    return "Article supprimé ! <a href='/'>Retour au blog</a>"

if __name__ == "__main__":
    app.run(debug=True)  # Active le mode debug pendant le développement