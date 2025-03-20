import os
import re

base_dir = 'perturbed_legal_documents'
PERTURBATION_TYPES = ['ambiguity', 'inconsistencies', 'misaligned_terminalogy', 'omission', 'structural_flaws']
CATEGORIES = ['inText', 'legal']
TAG_PATTERN = r'<\*\$p\$\*>' 

def remove_tag(text, tag_pattern):
    return re.sub(tag_pattern, '', text)

for p_type in PERTURBATION_TYPES:
    for category in CATEGORIES:
        tagged_path = f'{base_dir}/{p_type}_{category}_contradiction/modified_files_tags/'
        output_path = f'{base_dir}/{p_type}_{category}_contradiction/modified_files_no_tags/'
        
        os.makedirs(output_path, exist_ok=True)
        
        for filename in os.listdir(tagged_path):
            if filename.endswith('.txt'):
                # Using absolute path to avoid issues with path name length
                input_file = r"\\?\\" + os.path.abspath(os.path.join(tagged_path, filename))
                output_file = r"\\?\\" + os.path.abspath(os.path.join(output_path, filename))
                
                # try:        
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                
                with open(input_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                cleaned_content = remove_tag(content, TAG_PATTERN)
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
                
                print(f'Processed: {filename}')
                # except Exception:
                #     pass
