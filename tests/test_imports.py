import unittest

from pyYandexLinguistics import *  # to test absolute import
from .commons import assert_correct_import


class TestImports(unittest.TestCase):
    @assert_correct_import
    def test_import_all(self):
        assert "Translator" in globals() and "Vocabulary" in globals()
        assert "Predictor" in globals() and "YaTranslateException" in globals()
        assert "_YaAPIHandler" not in globals()

    @assert_correct_import
    def test_from_init(self):
        from pyYandexLinguistics import Translator
        assert Translator
        from pyYandexLinguistics import Vocabulary
        assert Vocabulary
        from pyYandexLinguistics import Predictor
        assert Predictor
        from pyYandexLinguistics import YaTranslateException
        assert YaTranslateException

    @assert_correct_import
    def test_from_modules(self):
        from pyYandexLinguistics import Translate
        assert Translate and Translate.Translator
        from pyYandexLinguistics import Dictionary
        assert Dictionary and Dictionary.Dictionary
        from pyYandexLinguistics import Prediction
        assert Prediction and Prediction.Predictor


if __name__ == "__main__":
    unittest.main()
