import os
import json
from collections import defaultdict

############################################################################
# GENERATE SCORES BASED ON TEXT_MATCH AND EXPLANATION_MATCH
############################################################################ 
def evaluate_scoring(responses_dir):
    scores = defaultdict(lambda: {
        "total": 0,
        "correct": 0,
        "text_matches": 0,
        "text_match_v1": 0,
        "text_match_v2": 0,
        "explanation_matches": 0,
        "explanation_match_scores": []
    })

    for root, _, files in os.walk(responses_dir):
        if not files:
            continue

        subdir = os.path.basename(root)

        for file in files:
            if not file.endswith(".json"):
                continue

            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    predictions = json.load(f)
            except json.JSONDecodeError:
                print(f"❌ Skipping malformed JSON: {file_path}")
                continue

            for pred in predictions:
                if not isinstance(pred, dict):
                    continue

                if "text_match" in pred and "explanation_match" in pred:
                    scores[subdir]["total"] += 1

                    if pred["text_match"]:
                        scores[subdir]["text_matches"] += 1
                    if pred.get("text_match_v1"):
                        scores[subdir]["text_match_v1"] += 1
                    if pred.get("text_match_v2"):
                        scores[subdir]["text_match_v2"] += 1
                    if pred["explanation_match"]:
                        scores[subdir]["explanation_matches"] += 1
                    if pred["text_match"] and pred["explanation_match"]:
                        scores[subdir]["correct"] += 1
                    if pred.get("explanation_match_score") is not None:
                        scores[subdir]["explanation_match_scores"].append(pred["explanation_match_score"])
                    
                    

    for subdir, stats in scores.items():
        total = stats["total"]
        if total == 0:
            continue
        print(f"\n📁 Directory: {subdir}")
        print(f"Text Match (any): {stats['text_matches']} / {total}")
        print(f"  ├─ v1 (changed_text): {stats['text_match_v1']} / {total}")
        print(f"  └─ v2 (contradicted_text): {stats['text_match_v2']} / {total}")
        print(f"Explanation Match: {stats['explanation_matches']} / {total}")
        print(f"Text + Explanation Match: {stats['correct']} / {total}")

    return {
        subdir: {
            "text_matches": stats["text_matches"],
            "text_match_v1": stats["text_match_v1"],
            "text_match_v2": stats["text_match_v2"],
            "explanation_matches": stats["explanation_matches"],
            "correct": stats["correct"],
            "total": stats["total"],
            "explanation_match_scores": stats["explanation_match_scores"],
        }
        for subdir, stats in scores.items()
    }