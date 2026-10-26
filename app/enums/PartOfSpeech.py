from enum import Enum


class PartOfSpeech(str, Enum):
    NOUN = "noun"                   # Danh từ (名詞)
    VERB_GROUP_1 = "verb_group_1"   # Động từ nhóm 1 (五段動詞 - Godan)
    VERB_GROUP_2 = "verb_group_2"   # Động từ nhóm 2 (一段動詞 - Ichidan)
    VERB_GROUP_3 = "verb_group_3"   # Động từ nhóm 3 (サ変/カ変 - suru, kuru)
    ADJECTIVE_I = "adjective_i"     # Tính từ đuôi -i (い形容詞)
    ADJECTIVE_NA = "adjective_na"   # Tính từ đuôi -na (な形容詞)
    ADVERB = "adverb"               # Phó từ (副詞)
    PARTICLE = "particle"           # Trợ từ (助詞)
    CONJUNCTION = "conjunction"     # Liên từ (接続詞)
    OTHER = "other"                 # Khác