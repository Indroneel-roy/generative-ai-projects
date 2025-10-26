import pandas as pd
import json
from difflib import SequenceMatcher

class FewShotPosts:
    def __init__(self, file_path="Data/cleaned_posts.json"):
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)

    def load_posts(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)
            self.df = pd.json_normalize(posts)

            # Normalize line length category
            self.df["length"] = self.df["line_count"].apply(self.categorize_length)

            # Clean tags
            self.df["tags"] = self.df["tags"].apply(self.clean_tags)

            # Collect unique tags
            all_tags = [t for tags in self.df["tags"] for t in tags]
            self.unique_tags = sorted(list(set(all_tags)))

    def clean_tags(self, tags):
        """Normalize tags (lowercase, remove #, unify similar ones)."""
        tag_map = {
            "job search": "jobs",
            "jobs": "jobs",
            "jobseekers": "jobs",
            "career advice": "career",
            "career growth": "career",
            "growth": "career_growth",
            "motivation": "motivation",
            "inspiration": "motivation",
            "resilience": "resilience",
            "focus": "focus",
            "success": "success",
            "integrity": "integrity",
            "legacy": "legacy",
            "mental health": "mental_health",
            "mentalhealth": "mental_health",
            "mentalhealthmatters": "mental_health",
            "selfcare": "self_care",
            "self care": "self_care",
            "wellbeing": "wellbeing",
            "productivity": "productivity",
            "workplace": "workplace",
            "peacefullife": "peaceful_life",
            "comfortzone": "comfort_zone",
            "linkedin": "linkedin",
            "scams": "scam",
        }

        cleaned = []
        for t in tags:
            t = t.lower().replace("#", "").strip()
            t = tag_map.get(t, t)  # map to unified form if available
            cleaned.append(t)
        return cleaned

    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_filtered_posts(self, length, language, tag):
        """Filter posts by approximate tag match (case-insensitive)."""
        tag = tag.lower().replace("#", "").strip()

        def tag_match(tags):
            if not tags:
                return False
            return any(tag in t or t in tag or SequenceMatcher(None, tag, t).ratio() > 0.7 for t in tags)

        df_filtered = self.df[
            self.df["tags"].apply(tag_match)
            & (self.df["language"].str.lower() == language.lower())
            & (self.df["length"] == length)
        ]

        return df_filtered.to_dict(orient="records")

    def get_tags(self):
        return self.unique_tags


if __name__ == "__main__":
    fs = FewShotPosts("Data/cleaned_posts.json")

    print("✅ Available tags:")
    print(fs.get_tags())

    # Try filtering
    posts = fs.get_filtered_posts(length="Short", language="english", tag="Motivation")
    print(f"\n🔍 Found {len(posts)} posts for 'Motivation':\n")
    for p in posts:
        print("-", p["text"][:80], "...")
