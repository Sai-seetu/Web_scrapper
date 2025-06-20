from flask import render_template, request, redirect, url_for, jsonify
from app import app, db, scheduler
from app.models import APILink
from app.scraper import scrape_with_llm_and_video
import os, uuid
import json

# Interval mapping in seconds
INTERVAL_MAP = {
    '1h': 3600,
    '6h': 21600,
    '24h': 86400
}

def schedule_scraping(link):
    def job():
        folder = f"static/videos/{uuid.uuid4()}"
        os.makedirs(folder, exist_ok=True)
        scrape_with_llm_and_video(link.search_query, link.website_url, folder)
        # Optionally update video path in DB on each job run:
        link.video_path = folder
        db.session.commit()

    seconds = INTERVAL_MAP.get(link.interval, 86400)
    scheduler.add_job(job, 'interval', seconds=seconds, id=str(link.id), replace_existing=True)

@app.route('/')
def index():
    links = APILink.query.order_by(APILink.timestamp.desc()).all()

    # Enrich each link with results (if any) from result.json
    for link in links:
        result_path = os.path.join(link.video_path, "result.json")
        if os.path.exists(result_path):
            with open(result_path, "r", encoding="utf-8") as f:
                link.result_data = json.load(f)
        else:
            link.result_data = {"results": []}

    return render_template("index.html", links=links)

@app.route("/scrape", methods=["POST"])
def scrape():
    query = request.form.get("query")
    url = request.form.get("url")
    interval = request.form.get("interval")

    video_folder = f"static/videos/{uuid.uuid4()}"
    os.makedirs(video_folder, exist_ok=True)

    # 🔁 Updated to get result
    final_url, result = scrape_with_llm_and_video(query, url, video_folder)
    print("Final URL:", final_url)
    print("Type:", type(final_url))

    # Construct a pseudo-API link
    data_id = video_folder.split("/")[-1]
    api_link_path = f"/api/data/{data_id}"

    link = APILink(
        search_query=query,
        website_url=final_url,
        video_path=video_folder,
        scraped_text=result.get("text", ""),
        api_endpoint=api_link_path,
        interval=interval,
        active=True
    )
    db.session.add(link)
    db.session.commit()

    schedule_scraping(link)
    return redirect(url_for("index"))


@app.route('/toggle/<int:id>', methods=['POST'])
def toggle(id):
    link = APILink.query.get(id)
    if not link:
        return jsonify({"status": "error", "message": "Link not found"}), 404

    link.active = not link.active
    db.session.commit()

    if link.active:
        schedule_scraping(link)
    else:
        try:
            scheduler.remove_job(str(link.id))
        except:
            pass  # Job may not exist yet

    return jsonify({"status": "success", "active": link.active})

@app.route('/api/<int:id>')
def api_result(id):
    link = APILink.query.get(id)
    if not link:
        return jsonify({"error": "Not found"}), 404
    return jsonify({
        "query": link.search_query,
        "url": link.website_url,
        "scraped_text": link.scraped_text,
        "video_path": link.video_path
    })

@app.route("/api/data/<uuid:data_id>", methods=["GET"])
def serve_scraped_data(data_id):
    link = APILink.query.filter_by(api_endpoint=f"/api/data/{data_id}").first()
    if not link:
        return jsonify({"error": "Not found"}), 404
    
    # Read result.json (if stored)
    result_path = os.path.join(link.video_path, "result.json")
    if os.path.exists(result_path):
        with open(result_path, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    else:
        return jsonify({
            "search_query": link.search_query,
            "website_url": link.website_url,
            "scraped_text": link.scraped_text or "No content found."
        })
