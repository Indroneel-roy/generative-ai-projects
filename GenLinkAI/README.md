
# LinkedIn Post Generator 🚀
This project is a Streamlit web application that generates LinkedIn posts using a Large Language Model (LLM). What makes it unique is its few-shot learning approach: it dynamically builds prompts by pulling relevant examples from a pre-processed dataset, allowing the LLM to match the tone, style, and structure of existing posts on a given topic.



## Demo
https://github.com/Indroneel-roy/generative-ai-projects/blob/main/GenLinkAI/git.png


## Features
Topic-Based Generation: Create posts based on a wide range of topics (e.g., "Motivation," "Jobs," "Career").

Style Adaptation: Uses few-shot examples to guide the LLM, resulting in posts that match a desired style.

Customizable Output: Control the Length ("Short," "Medium," "Long") and Language ("English," "Banglish") of the generated post.

Data Processing Pipeline: Includes a complete pipeline to ingest raw posts, extract metadata using an LLM, and clean the data for use.

Simple Web UI: Built with Streamlit for easy interaction.

## 🛠️ How It Works: The Data & Generation Pipeline
The project is split into two main parts: the data processing pipeline (to build the example dataset) and the generation app (to create new posts).

#### Data Processing Pipeline
This pipeline turns a raw JSON file of posts (data/raw_posts.json) into a clean, structured dataset (data/cleaned_posts.json) used for few-shot learning.

#### 1. preprocess.py:

* Reads data/raw_posts.json.

* For each post, it uses an LLM to extract metadata: line_count, language (English/Banglish), and tags.

* It then aggregates all extracted tags and uses the LLM again (get_unified_tags) to map similar tags to a single, unified tag (e.g., "Job Hunting" -> "Job Search").

* Saves the intermediate, enriched data to data/processed_posts.json.

#### 2. clean_json.py:

* Reads data/processed_posts.json.

* Performs final cleaning and standardization:

* Ensures consistent key order.

* Normalizes text (removes surrogates, strips whitespace).

* Normalizes language values (defaults to "english").

* Cleans and de-duplicates tags (converts to Title Case).

* Saves the final, app-ready dataset to data/cleaned_posts.json.

#### Post Generation App
#### 1. few_shot.py:

* This class loads data/cleaned_posts.json into a Pandas DataFrame for fast querying.

* It provides the get_filtered_posts() method, which finds example posts that match the user's selected length, language, and topic. It even uses difflib.SequenceMatcher for approximate tag matching.

#### 2. post_generator.py:

* This is the core generation logic.

* It calls few_shot.get_filtered_posts() to get 1-2 relevant examples.

* It constructs a detailed prompt for the LLM, including the user's request (topic, length, language) and the retrieved few-shot examples.

#### 3. main.py:

This script runs the Streamlit web app.

It creates the UI with dropdowns for Topic, Length, and Language.

When the "Generate" button is pressed, it calls generate_post() and displays the resulting post on the screen.

## 🧰 Tech Stack

* Python 3.10+

* Streamlit — UI framework

* LangChain + Groq/Gemma2 — LLM backend

* Pandas — Data manipulation

* JSON — Dataset storage

## Installation



```bash
  pip install -r requirements.txt

```

    
## Authors

- [@Indroneel](https://github.com/Indroneel-roy)



