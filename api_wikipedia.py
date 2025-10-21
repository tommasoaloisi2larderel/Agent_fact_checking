import requests
import re

def get_clean_wikipedia_text(title, lang="fr"):
    url = (
        f"https://{lang}.wikipedia.org/w/api.php?"
        f"action=query&prop=extracts&explaintext=true&format=json&titles={title.replace(' ', '_')}"
    )
    headers = {"User-Agent": "AgentFactChecking/1.0 (contact: thebawss200@gmail.com)"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("❌ Erreur:", response.text)
        return None

    data = response.json()
    pages = data["query"]["pages"]
    page = next(iter(pages.values()))
    raw_text = page.get("extract", "")

    # 🧼 Nettoyage du texte
    clean_text = re.sub(r'\n\s*\n+', '\n', raw_text)  # un seul saut de ligne entre paragraphes
    clean_text = re.sub(r'[ \t]+', ' ', clean_text)   # supprime les espaces multiples
    clean_text = clean_text.strip()                   # supprime le blanc en début/fin

    return clean_text


# Exemple d'utilisation
texte = get_clean_wikipedia_text("France")
print(texte[:1000])
