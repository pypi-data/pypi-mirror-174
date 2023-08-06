import pickle
from typing import List

from sikriml_core.models.ner.tokenizer import TokenData
from sikriml_core.models.ner.tokenizer.abstracts import TokenizerBase
from spacy.tokens import Doc
from spacy.vocab import Vocab


class SpacyTokenizer:
    def __init__(self, vocab: Vocab, tokenizer: TokenizerBase):
        self.vocab = vocab
        self.tokenizer = tokenizer

    def __call__(self, text: str) -> Doc:
        tokens: List[TokenData] = self.tokenizer(text)
        words = [token.text for token in tokens]
        spaces = [token.space_after for token in tokens]
        return Doc(self.vocab, words=words, spaces=spaces)

    # Required by spacy's Tokenizer https://support.prodi.gy/t/saving-custom-tokenizer/395
    def to_bytes(self):
        return pickle.dumps({k: v for k, v in self.__dict__.items() if k != "vocab"})

    # Required by spacy's Tokenizer https://support.prodi.gy/t/saving-custom-tokenizer/395
    def from_bytes(self, data):
        self.__dict__.update(pickle.loads(data))

    # Required by spacy's Tokenizer https://support.prodi.gy/t/saving-custom-tokenizer/395
    def to_disk(self, path, **kwargs):
        with open(path, "wb") as file_:
            file_.write(self.to_bytes())

    # Required by spacy's Tokenizer https://support.prodi.gy/t/saving-custom-tokenizer/395
    def from_disk(self, path, **kwargs):
        with open(path, "rb") as file_:
            self.from_bytes(file_.read())
