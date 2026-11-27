import csv
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

API = "https://api.stackexchange.com/2.3"
TAG = "python"
QUESTION_LIMIT = 25
OUTPUT = Path(__file__).resolve().parents[1] / "data" / "pilot"


def get_posts(endpoint, limit=None, **filters):
    """Fetch pages until there are no more posts or we reach the limit."""
    posts = []
    page = 1

    while True:
        response = requests.get(
            API + endpoint,
            params={
                "site": "stackoverflow",
                "filter": "withbody",
                "pagesize": 100,
                "page": page,
                **filters,
            },
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()

        if "backoff" in result:
            time.sleep(result["backoff"])

        posts.extend(result["items"])
        if limit is not None and len(posts) >= limit:
            return posts[:limit]
        if not result["has_more"]:
            return posts
        if result.get("quota_remaining") == 0:
            raise RuntimeError("API quota ran out before collection finished.")

        page += 1


def clean_text(body_html):
    """Keep the prose and leave code out of the cleaned version."""
    soup = BeautifulSoup(body_html, "html.parser")
    for block in soup.find_all("pre"):
        block.decompose()
    for code in soup.find_all("code"):
        code.decompose()
    return " ".join(soup.get_text(" ", strip=True).split())


def user_id(post):
    return (post.get("owner") or {}).get("user_id", "")


def save_csv(filename, columns, rows):
    with (OUTPUT / filename).open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def main():
    # Sample older questions so they have had time to receive answers.
    end = datetime.now(timezone.utc) - timedelta(days=30)
    start = end - timedelta(days=7)

    questions = get_posts(
        "/questions",
        limit=QUESTION_LIMIT,
        tagged=TAG,
        sort="creation",
        order="desc",
        fromdate=int(start.timestamp()),
        todate=int(end.timestamp()),
    )
    if not questions:
        raise RuntimeError("No questions found. Try a different date window.")

    # The API accepts up to 100 question IDs per answer request.
    answers = []
    for i in range(0, len(questions), 100):
        batch = questions[i:i + 100]
        ids = ";".join(str(q["question_id"]) for q in batch)
        answers.extend(get_posts(f"/questions/{ids}/answers"))

    OUTPUT.mkdir(parents=True, exist_ok=True)

    question_rows = [
        {
            "question_id": q["question_id"],
            "asker_id": user_id(q),
            "title": BeautifulSoup(q["title"], "html.parser").get_text(),
            "tags": ",".join(q["tags"]),
            "created_at_unix": q["creation_date"],
            "accepted_answer_id": q.get("accepted_answer_id", ""),
            "body_html": q["body"],
            "clean_text": clean_text(q["body"]),
        }
        for q in questions
    ]

    askers = {q["question_id"]: q["asker_id"] for q in question_rows}
    answer_rows = [
        {
            "answer_id": a["answer_id"],
            "question_id": a["question_id"],
            "answerer_id": user_id(a),
            "created_at_unix": a["creation_date"],
            "is_accepted": a["is_accepted"],
            "body_html": a["body"],
            "clean_text": clean_text(a["body"]),
            "usable_for_graph": bool(user_id(a) and askers.get(a["question_id"])),
        }
        for a in answers
    ]

    save_csv("questions.csv", list(question_rows[0]), question_rows)
    save_csv(
        "answers.csv",
        ["answer_id", "question_id", "answerer_id", "created_at_unix",
         "is_accepted", "body_html", "clean_text", "usable_for_graph"],
        answer_rows,
    )

    usable = sum(row["usable_for_graph"] for row in answer_rows)
    summary = (
        f"Tag: {TAG}\n"
        f"Question window (UTC): {start.isoformat()} to {end.isoformat()}\n"
        f"Selection: newest {QUESTION_LIMIT} questions in that window\n"
        f"Questions collected: {len(question_rows)}\n"
        f"Answers collected: {len(answer_rows)}\n"
        f"Answers usable for the graph: {usable}\n"
        f"Answers excluded from the graph due to missing user IDs: "
        f"{len(answer_rows) - usable}\n"
    )
    (OUTPUT / "pilot_summary.txt").write_text(summary, encoding="utf-8")
    print(summary)
    print(f"Files saved in: {OUTPUT}")


if __name__ == "__main__":
    main()
