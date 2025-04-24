import os
import json
import tqdm
from google.api_core.exceptions import ResourceExhausted
import glob
import time
from sentence_transformers import SentenceTransformer, util

from modules.models import Model

############################################################################
# LLM-BASED EXPLANATION MATCH IMPLEMENTATION
############################################################################ 
def explanation_match(evaluation_model: Model, dataset, responses_dir):
    for sample in tqdm.tqdm(dataset, desc="Evaluating explanations"):
        file_name = sample["file_name"]
        
        # Normalize and split into subdir + base filename (fixes Windows paths)
        normalized_path = os.path.normpath(file_name)
        subdir = os.path.dirname(normalized_path).replace("\\", "/")
        base_filename = os.path.basename(normalized_path).replace(".json", "")

        # Match all _i.json variant files for this sample
        pattern = os.path.join(responses_dir, "self_consistency", subdir, f"{base_filename}_*.json")
        response_paths = sorted(glob.glob(pattern))

        if not response_paths:
            print(f"❌ No response files found for: {file_name}")
            continue

        # Extract GT explanations
        gt_explanations = [
            p["explanation"].strip()
            for p in sample["answers"][0]["perturbation"]
            if "explanation" in p
        ]

        for response_path in response_paths:
            with open(response_path, "r", encoding="utf-8") as f:
                try:
                    model_preds = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"❌ JSON decode error in {response_path}: {e}")
                    continue

            updated = False
            for pred in model_preds:
                if "explanation_match" in pred:
                    continue

                model_exp = pred.get("explanation", "").strip()
                if not model_exp:
                    pred["explanation_match"] = False
                    updated = True
                    continue

                match_found = False
                for gt_exp in gt_explanations:
                    prompt = f"""
You are evaluating whether the following model explanation captures the **same core reasoning** as the human (ground truth) explanation.

Ground Truth Explanation:
"{gt_exp}"

Model Explanation:
"{model_exp}"

Does the model explanation capture the same core reasoning as the ground truth explanation, even if phrased differently?

Answer "yes" or "no" only.
                    """.strip()

                    print(f"\n📄 Evaluating: {response_path}")
                    print(f"GT: {gt_exp}")
                    print(f"Model: {model_exp}")

                    try:
                        response = evaluation_model.generate(prompt)
                        result_text = response.strip().lower()
                        print(f"LLM response: {result_text}")

                        if "yes" in result_text:
                            match_found = True
                            break

                    except ResourceExhausted as e:
                        print(f"⚠️ Rate limit hit: {e}")
                        print("⏳ Sleeping for 40 seconds...")
                        time.sleep(40)
                        continue

                    except Exception as e:
                        print(f"⚠️ Unexpected error: {e}")
                        break

                    time.sleep(1.5)

                pred["explanation_match"] = match_found
                updated = True

            if updated:
                with open(response_path, "w", encoding="utf-8") as f:
                    json.dump(model_preds, f, indent=4)
                print(f"✅ Updated explanation_match in: {response_path}")
            else:
                print(f"⚠️ Skipped (no update needed): {response_path}")

############################################################################
# SBERT COSINE SIMILARITY-BASED EXPLANATION MATCH IMPLEMENTATION
############################################################################ 
def explanation_match_sbert(dataset, responses_dir, threshold=0.8, model_name="all-MiniLM-L6-v2"):
    # Load SBERT model once
    try:
        sbert = SentenceTransformer(model_name)
        sbert.to("cpu")
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Failed to load SBERT model '{model_name}': {e}")
        return

    for sample in tqdm.tqdm(dataset, desc="Evaluating explanations (SBERT)"):
        file_name = sample["file_name"]

        normalized_path = os.path.normpath(file_name)
        subdir = os.path.dirname(normalized_path).replace("\\", "/")
        base_filename = os.path.basename(normalized_path).replace(".json", "")

        pattern = os.path.join(responses_dir, "self_consistency", subdir, f"{base_filename}_*.json")
        response_paths = sorted(glob.glob(pattern))

        if not response_paths:
            print(f"❌ No response files found for: {file_name}")
            continue

        gt_explanations = [
            p["explanation"].strip()
            for p in sample["answers"][0]["perturbation"]
            if "explanation" in p
        ]

        if not gt_explanations:
            print(f"⚠️ No ground truth explanations for: {file_name}")
            continue

        gt_embeddings = sbert.encode(gt_explanations, convert_to_tensor=True)

        for response_path in response_paths:
            try:
                with open(response_path, "r", encoding="utf-8") as f:
                    model_preds = json.load(f)
            except json.JSONDecodeError as e:
                print(f"\n❌ JSON decode error in {response_path}: {e}")
                
                # Print surrounding lines for debugging
                with open(response_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    print("🪵 Showing lines around error:")
                    for i, line in enumerate(lines):
                        if e.lineno - 3 <= i <= e.lineno + 1:
                            print(f"{i + 1}: {line.strip()}")
                continue

            updated = False
            for pred in model_preds:
                if "explanation_match" in pred:
                    continue

                model_exp = pred.get("explanation", "").strip()
                if not model_exp:
                    pred["explanation_match"] = False
                    updated = True
                    continue

                model_embedding = sbert.encode(model_exp, convert_to_tensor=True)

                sim_scores = util.cos_sim(model_embedding, gt_embeddings)[0]
                max_sim = sim_scores.max().item()
                pred["explanation_match_score"] = max_sim
                pred["explanation_match"] = max_sim >= threshold
                updated = True

                print(f"\n📄 Evaluated: {response_path}")
                print(f"GT (top sim): {gt_explanations[sim_scores.argmax().item()]}")
                print(f"Model: {model_exp}")
                print(f"Score: {max_sim:.4f} → {'✅ Match' if pred['explanation_match'] else '❌ No Match'}")

            if updated:
                with open(response_path, "w", encoding="utf-8") as f:
                    json.dump(model_preds, f, indent=4)
                print(f"✅ Updated explanation_match in: {response_path}")
            else:
                print(f"⚠️ Skipped (no update needed): {response_path}")