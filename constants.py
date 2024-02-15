import pytz

LANG_DICT = {
            "vi": "vietnamese",
            "en": "english",
            "fr": "french",
            "es": "spanish",
            "de": "german",
            "it": "italian",
            "ja": "japanese",
            "ko": "korean",
            "tl": "philippines",
            "zh": "chinese",
        }


SMILEY_REGEX = r':[)]+'
FROWN_REGEX = r":[(]+"

TIME_ZONE = pytz.timezone("Asia/Ho_Chi_Minh")