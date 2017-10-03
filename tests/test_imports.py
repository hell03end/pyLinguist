from pyLinguist import *  # to test absolute import
from .commons import assert_correct_import


class TestImports:
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
        assert pyLinguist
        assert "pyLinguist" in locals()

    @assert_correct_import
    def test_from_init(self):
        from pyLinguist import Translator
        assert Translator
        assert "Translator" in locals()

        from pyLinguist import Dictionary
        assert Dictionary
        assert "Dictionary" in locals()

        from pyLinguist import Predictor
        assert Predictor
        assert "Predictor" in locals()

        from pyLinguist import Speller
        assert Speller
        assert "Speller" in locals()

        from pyLinguist import YaTranslateException
        assert YaTranslateException
        assert "YaTranslateException" in locals()

    @assert_correct_import
    def test_from_modules(self):
        from pyLinguist import Translate
        assert Translate
        assert "Translate" in locals()
        assert Translate.Translator

        from pyLinguist import Vocabulary
        assert Vocabulary
        assert "Vocabulary" in locals()
        assert Vocabulary.Dictionary
        assert Vocabulary.Speller

        from pyLinguist import Prediction
        assert Prediction
        assert "Prediction" in locals()
        assert Prediction.Predictor
