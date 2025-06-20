from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
import os, re, json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Fireworks


FIREWORKS_MODEL = "accounts/fireworks/models/llama-v2-7b-chat"

def get_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc.lower()

def suggest_site_with_llm(query):
    llm = Fireworks(model=FIREWORKS_MODEL)
    prompt = PromptTemplate.from_template(
        "Given the query: '{query}', return only a single valid, working e-commerce or news website URL (like https://www.amazon.in) where this query can be answered. Do NOT include any other text or explanation."
    )
    chain = prompt | llm | StrOutputParser()
    suggestion = chain.invoke({"query": query})
    urls = re.findall(r'https?://[^\s)\]}\'\"]+', suggestion)
    return urls[0].rstrip('/') if urls else None

def scrape_with_llm_and_video(query, url=None, video_folder="recordings"):
    if not url:
        url = suggest_site_with_llm(query)
        print(" Suggested URL from LLM:", url)

    if not url or not url.startswith("http"):
        print(" Invalid URL from LLM. Skipping.")
        return url, {"text": "Invalid or unreachable website", "images": []}

    os.makedirs(video_folder, exist_ok=True)
    result_file = os.path.join(video_folder, "result.json")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(record_video_dir=video_folder)
        page = context.new_page()

        try:
            print(" Opening:", url)
            page.goto(url, timeout=70000)
        except Exception as e:
            return url, {"text": " Failed to load website", "images": []}

        try:
            input_box = page.query_selector("input[type='search'], input[type='text'], input[name*=search], input[id*=search]")
            if input_box:
                input_box.click()
                input_box.fill(query)
                input_box.press("Enter")  # Better than click() on many sites
                page.wait_for_timeout(6000)
            else:
                print(" No input box found.")
        except Exception as e:
            print(" Search failed:", e)

        page.wait_for_load_state("domcontentloaded")
        domain = get_domain(url)
        results = []

        all_images = page.query_selector_all("img")
        for img in all_images[:20]:
            try:
                src = img.get_attribute("src")
                alt = img.get_attribute("alt")
                if src and "logo" not in src and "sprite" not in src:
                    results.append({
                        "image": src if src.startswith("http") else "https:" + src,
                        "alt_text": alt or "No alt text",
                
                    })
            except:
                continue

        context.close()
        browser.close()

    final_data = {
        "query": query,
        "results": results
    }

    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=2)

    

    return url, {
        "text": f" Found {len(results)} images for: {query}" if results else " No content found.",
        "images": [item["image"] for item in results]
    }
