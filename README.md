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
- For eval purposes, we will need to remove the tags from `pertubed_legal_documents/<pertubation>_<categories>_contradiction/modified_file_tags/modified...txt` before passing into to other LLMs for evaluation.