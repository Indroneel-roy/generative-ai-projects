import json
import re

def clean_post_data(posts):
    cleaned = []
    for post in posts:
        # 1️⃣ Ensure consistent key order
        post = {
            "text": clean_text(post.get("text", "")),
            "engagement": int(post.get("engagement", 0)),
            "line_count": int(post.get("line_count", 0)),
            "language": normalize_language(post.get("language", "")),
            "tags": clean_tags(post.get("tags", []))
        }
        cleaned.append(post)
    return cleaned


def clean_text(text):
    # Remove surrogate characters and weird unicode
    if not isinstance(text, str):
        return ""
    text_bytes = text.encode("utf-8", "surrogatepass")
    text = text_bytes.decode("utf-8", "ignore")
    text = re.sub(r'[\ud800-\udfff]', '', text)
    return text.strip()


def normalize_language(lang):
    lang = lang.lower().strip()
    if lang not in ["english", "banglish", "bangla"]:
        lang = "english"  # Default fallback
    return lang


def clean_tags(tags):
    if not tags or not isinstance(tags, list):
        return []
    # Remove duplicates, normalize capitalization
    cleaned = list({tag.strip().title() for tag in tags if tag.strip()})
    return cleaned


def main():
    with open("data/processed_posts.json", "r", encoding="utf-8") as f:
        posts = json.load(f)

    cleaned_posts = clean_post_data(posts)

    with open("data/cleaned_posts.json", "w", encoding="utf-8") as f:
        json.dump(cleaned_posts, f, indent=4, ensure_ascii=False)

    print("✅ Cleaned JSON file saved to data/cleaned_posts.json")


if __name__ == "__main__":
    main()
