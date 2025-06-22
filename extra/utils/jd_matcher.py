import re

def extract_jd_keywords(text):
    text = text.lower()
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text)
    stopwords = set(["with", "your", "have", "you", "and", "the", "for", "are", "our", "will", "this", "that"])
    keywords = [word for word in words if word not in stopwords]
    return list(set(keywords))[:20]
