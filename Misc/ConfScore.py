# ─────────────────────────────────────────────────────────────────────────────
#  Law‑Validation Script  (handles scraped_snippet_1 / scraped_snippet_2)
# ─────────────────────────────────────────────────────────────────────────────
#  1) cosine‑similarity “cheap confidence” using MiniLM
#  2) Gemini verification prompt (uses ONE snippet → first non‑empty of the two)
#  3) writes results to a parallel output folder
# ─────────────────────────────────────────────────────────────────────────────

# pip install -q sentence-transformers scikit-learn google-generativeai tqdm

import os, json, re, time, pathlib
from tqdm.auto import tqdm
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import google.generativeai as genai

# ─── env / paths ─────────────────────────────────────────────────────────────
os.environ["GOOGLE_API_KEY"] = "AIzaSyDgafwAgDi2Zjvu6jdt_SIZ60VgK1Na32E"   # ← your key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

INPUT_FOLDER  = pathlib.Path("scraped_laws_v7/ambiguity_legal")             # *.snippet.json
OUTPUT_FOLDER = pathlib.Path("scraped_lawsCS/ambiguity_legal/") # results
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# ─── models ──────────────────────────────────────────────────────────────────
gemini = genai.GenerativeModel("gemini-2.0-flash")
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ─── helper: first non‑empty snippet (or '') ────────────────────────────────
def best_snippet(pert):
    s1 = (pert.get("scraped_snippet_1") or "").strip()
    s2 = (pert.get("scraped_snippet_2") or "").strip()
    return s1 if s1 else s2

# ─── cosine similarity score (cheap automatic check) ───────────────────────
def cosine_confidence(text_a: str, text_b: str) -> float:
    if not text_a or not text_b:
        return 0.0
    emb_a, emb_b = embedder.encode([text_a, text_b])
    return float(cosine_similarity([emb_a], [emb_b])[0, 0])

# ─── Gemini‑based verification prompt  (single snippet) ─────────────────────
def verification_prompt(pert):
    snippet = best_snippet(pert)
    return f"""
You are a legal‑verification expert. Decide whether the cited law is real, relevant,
and actually contradicted by the contract modification.

· **Perturbation type:** {pert.get("type",'')}
· **Perturbation explanation:** {pert.get("explanation",'')}
· **LLM law explanation:** {pert.get("law_explanation",'')}
· **Scraped law snippet:** {snippet or '[empty]'}  ← use if present

Return ONLY:

{{
  "confidence_score": <float 0‑1>,
  "justification": "<one short sentence>"
}}
""".strip()

def ask_gemini(prompt: str) -> dict:
    try:
        res = gemini.generate_content(prompt).text
        res = re.sub(r"```json|```", "", res).strip()
        return json.loads(res)
    except Exception as e:
        return {"confidence_score": None, "justification": f"Gemini failed: {e}"}

# ─── main loop ───────────────────────────────────────────────────────────────
input_files = [p for p in INPUT_FOLDER.glob("*.json")]
for fpath in tqdm(input_files, desc="Verifying contradictions"):
    with open(fpath, encoding="utf-8") as fh:
        data = json.load(fh)
    root = data[0] if isinstance(data, list) else data

    for pert in root.get("perturbation", []):
        # 1) cosine score
        snippet = best_snippet(pert)
        law_exp = pert.get("law_explanation", "")
        pert["cosine_confidence"] = round(cosine_confidence(law_exp, snippet), 4)

        # 2) Gemini score
        g_json = ask_gemini(verification_prompt(pert))
        pert["llm_confidence"] = g_json.get("confidence_score")
        pert["llm_justification"] = g_json.get("justification")
        time.sleep(4)          # polite pause to avoid quota spikes

    # write parallel file tree
    out_path = OUTPUT_FOLDER / fpath.name
    with open(out_path, "w", encoding="utf-8") as out:
        json.dump(data, out, indent=2, ensure_ascii=False)

print(f"✓  Finished.  Results saved under {OUTPUT_FOLDER}")
