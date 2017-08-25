import unittest

from pyLinguist import *  # to test absolute import
from .commons import assert_correct_import


class TestImports(unittest.TestCase):
    @assert_correct_import
    def test_import_all(self):
        assert "Translator" in globals() and "Dictionary" in globals()
        assert "Predictor" in globals() and "YaTranslateException" in globals()
        assert "_YaAPIHandler" not in globals()

    @assert_correct_import
    def test_from_init(self):
        from pyLinguist import Translator
        assert Translator
        from pyLinguist import Dictionary
        assert Dictionary
        from pyLinguist import Predictor
        assert Predictor
        from pyLinguist import YaTranslateException
        assert YaTranslateException

    @assert_correct_import
    def test_from_modules(self):
        from pyLinguist import Translate
        assert Translate and Translate.Translator
        from pyLinguist import Vocabulary
        assert Vocabulary and Vocabulary.Dictionary
        from pyLinguist import Prediction
        assert Prediction and Prediction.Predictor


if __name__ == "__main__":
    unittest.main()
