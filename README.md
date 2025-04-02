# Legal-Document-Discrepancy_Benchmark_Dataset

> full_contract_txt
- Contains the original documents (.txt)

> full_contract_pdf
- Contains the original documents (.pdf)

> pertubed_legal_documents
- Contains subdirs of various pertubations (ambiguity, inconsistencies, misaligned_terminology, omission, structural_flaws) and in 2 categories (inText, legal).
- `pertubed_legal_documents/<pertubation>_<categories>_contradiction/...json` contains structured data which states which line was modified to fulfill the criteria of the pertubation. 
- `pertubed_legal_documents/<pertubation>_<categories>_contradiction/modified_file_tags/modified...txt` contains the modified documents with the tags for parts that are modified.

# TODO
1. For eval purposes, we will need to remove the tags from `pertubed_legal_documents/<pertubation>_<categories>_contradiction/modified_file_tags/modified...txt` before passing into to other LLMs for evaluation.
2. Create prompts to read the non-tagged files and test to see if LLM can find the perturbation within the file. produce an explanation from LLM.
3. Create LLM persona and introduce few shot prompting, give definition of each type of perturbation.
4. LLM answer: section where perturbation lies, an explanation of why this is a perturbation, categorize the type of perturbation.
5. Human eval: compare LLM explanation answer to Json ground truth file.
6. Sketch out LLM eval and test it if possible.

Add `explanation_match` (check reasoning) - Use LLM, along with context
Use explanation + location to gauge + 1 / -1
Our `text_match` proposed `location_match` below
1) `location match` but `explanation !match` = -1
2) `location match` and `explanation match` = +1
3) `location !match` and `explanation match` 
- Case 1: Partial location match (only caught 1/2 of the 3 enclosed sentences) = +1 (already in our `text_match` implementation)
- Case 2: Location mismatch (not even in the tags) = -1 
4) `location !match` and `explanation !match` = -1