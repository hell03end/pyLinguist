import unittest

from pyLinguist import *  # to test absolute import
from .commons import assert_correct_import


class TestImports(unittest.TestCase):
    def test_import_all(self):
        assert "Translator" in globals()
        assert "Dictionary" in globals()
        assert "Predictor" in globals()
        assert "Speller" in globals()
        assert "YaTranslateException" in globals()
        assert "_YaAPIHandler" not in globals()

    @assert_correct_import
    def test_direct_import(self):
        import pyLinguist
        assert pyLinguist and "pyLinguist" in locals()

    @assert_correct_import
    def test_from_init(self):
        from pyLinguist import Translator
        assert Translator and "Translator" in locals()
        from pyLinguist import Dictionary
        assert Dictionary and "Dictionary" in locals()
        from pyLinguist import Predictor
        assert Predictor and "Predictor" in locals()
        from pyLinguist import Speller
        assert Speller and "Speller" in locals()
        from pyLinguist import YaTranslateException
        assert YaTranslateException and "YaTranslateException" in locals()

    @assert_correct_import
    def test_from_modules(self):
        from pyLinguist import Translate
        assert Translate and "Translate" in locals()
        assert Translate.Translator
        from pyLinguist import Vocabulary
        assert Vocabulary and "Vocabulary" in locals()
        assert Vocabulary.Dictionary and Vocabulary.Speller
        from pyLinguist import Prediction
        assert Prediction and "Prediction" in locals()
        assert Prediction.Predictor


if __name__ == "__main__":
    unittest.main()
