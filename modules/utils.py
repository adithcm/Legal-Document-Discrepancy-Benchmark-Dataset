import json
import os

def clean_and_parse_model_response(raw_response):
    raw_response = raw_response.strip().strip("`")
    if raw_response.startswith("json"):
        raw_response = raw_response[4:].strip()

    try:
        parsed = json.loads(raw_response)
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e)
        return None

    return parsed


def add_section_identified_flag(predictions, ground_truth_perturbations):
    gt_locations = {p["location"].strip() for p in ground_truth_perturbations}
    gt_changed_texts = [p["changed_text"] for p in ground_truth_perturbations]
    gt_contradicted_texts = [p["contradicted_text"] for p in ground_truth_perturbations]

    for pred in predictions:
        # LOCATION MATCH
        pred_loc = pred.get("location", "").strip()
        pred["location_match"] = pred_loc in gt_locations

        # SECTION TEXT
        pred_section = pred.get("section", "").strip()

        # Match against changed text
        text_match_v1 = any(pred_section in gt_text or gt_text in pred_section for gt_text in gt_changed_texts)
        # Match against contradicted text
        text_match_v2 = any(pred_section in gt_text or gt_text in pred_section for gt_text in gt_contradicted_texts)

        # Final flags
        pred["text_match_v1"] = text_match_v1   # Checks against changed text
        pred["text_match_v2"] = text_match_v2   # Checks agaist contradicted text       
        pred["text_match"] = text_match_v1 or text_match_v2 # Checks against either

    return predictions

# Corrects path name such that it ignores path length limit and formats based on your OS definition
def correct_path_name(path):
    return r"\\?\{}".format(os.path.abspath(path))
