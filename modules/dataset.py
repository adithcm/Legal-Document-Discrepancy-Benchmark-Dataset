from abc import ABC, abstractmethod
import os
import json

############################################################################
# ABSTRACT DATASET
############################################################################ 
class Dataset(ABC):
    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __getitem__(self, idx):
        pass

############################################################################
# OUR MINI_EVAL DATASET
############################################################################ 
class MiniEvalDataset(Dataset):
    def __init__(self):
        self.mini_eval_dir = "mini-eval"
        self.mini_eval_answers_dir = os.path.join(self.mini_eval_dir, "answers_v2") # change this later
        self.mini_eval_documents_dir = os.path.join(self.mini_eval_dir, "documents_v2") # change this later
        self.files = [
            os.path.relpath(
                os.path.join(root, file), self.mini_eval_answers_dir
            ).replace(".json", "")
            for root, _, files in os.walk(self.mini_eval_answers_dir)
            for file in files
        ]
        self.files.sort()

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        with open(
            os.path.join(self.mini_eval_answers_dir, self.files[idx] + ".json"),
            "r",
            encoding="utf-8",
        ) as f:
            answers = "\n".join(f.readlines())
            answers = self.__remove_non_ascii(answers)
            answers = json.loads(answers)

        with open(
            os.path.join(self.mini_eval_documents_dir, self.files[idx] + ".txt"),
            "r",
            encoding="utf-8",
        ) as f:
            documents = "\n".join(f.readlines())
            documents = self.__remove_non_ascii(documents)


        return {
            "file_name": self.files[idx],
            "answers": answers,
            "documents": documents,
        }


    def __remove_non_ascii(self, s):
        return "".join(filter(lambda x: ord(x) < 128, s))
    
    # Just something to clean up file names since you punks keep adding shit to it
    def clean_filenames(self, prefixes=("modified_", "perturbed_")):
        def clean_dir(directory, extension):
            for root, _, files in os.walk(directory):
                for file in files:
                    if not file.endswith(extension):
                        continue

                    original_path = os.path.join(root, file)
                    new_name = file

                    for prefix in prefixes:
                        if new_name.startswith(prefix):
                            new_name = new_name[len(prefix):]
                            break  # Remove only the first matched prefix

                    if new_name != file:
                        new_path = os.path.join(root, new_name)
                        print(f"🔄 Renaming: {original_path} → {new_path}")
                        os.rename(original_path, new_path)

        clean_dir(self.mini_eval_answers_dir, ".json")
        clean_dir(self.mini_eval_documents_dir, ".txt")