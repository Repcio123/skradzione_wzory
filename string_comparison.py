from Levenshtein import distance as levenshtein_distance, matching_blocks as levenshtein_matching_blocks, editops as levenshtein_editops, ratio as levenshtein_similarity_ratio
import json
from difflib import SequenceMatcher
from antiplagarism_tools import AntiPlagiatResult

PARAGHRAPH_DEST = "tex_file_base/cached_paragraphs.json"
MIN_LEN = 8
MIN_DIST = 1


class StringComparison():
    @staticmethod
    def similarCharSequences(s1: str, s2: str):
        seq = []
        counter = 0
        if len(s1) > len(s2):
            for i in range(len(s2)):
                if s1[i] is s2[i]:
                    counter += 1
                else:
                    if counter >= MIN_DIST and levenshtein_distance(s1[i-counter:i], s2[i-counter:i]) == 1:
                        seq.append(s1[i-counter:i])
                    counter = 0
        else:
            for i in range(len(s1)):
                if s1[i] is s2[i]:
                    counter += 1
                else:
                    if counter >= MIN_LEN and levenshtein_distance(s1[i-counter:i], s2[i-counter:i]) == 1:
                        seq.append(s1[i-counter:i])
                    counter = 0
        return seq

    @staticmethod
    def compareChars(str1: str, str2: str):
        same_str_blocks = []
        match_pos = []
        mb = levenshtein_matching_blocks(
            levenshtein_editops(str1, str2), str1, str2)

        for x in mb:
            block1 = str1[x[0]:x[0]+x[2]]
            block2 = str2[x[0]:x[0]+x[2]]
            if len(block1) >= MIN_LEN and len(block2) >= MIN_LEN:
                same_str_blocks.append(block1)
                match_pos.append(x)
        same_str_blocks.append(StringComparison.similarCharSequences(str1, str2))
        return AntiPlagiatResult("compare chars", float('nan'), same_str_blocks, levenshtein_similarity_ratio(str1, str2)*100)

    @staticmethod
    def similarSentences(s1: str, s2: str):
        seq = []
        counter = 0
        matcher = SequenceMatcher(None, s1, s2)
        for op, i1, i2, j1, j2 in matcher.get_opcodes():
            if op == 'equal':
                counter += i2 - i1
                if counter >= MIN_LEN:
                    seq.append(s1[i1:i1+counter])
            else:
                counter = 0
        return seq



if __name__ == "__main__":
    f = open(PARAGHRAPH_DEST)
    data = json.load(f)
    print(StringComparison.similarSentences(data[0], data[9]))
