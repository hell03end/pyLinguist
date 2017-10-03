import unittest

from pyLinguist import *  # to test absolute import
from .commons import assert_correct_import, GenericTest


class TestImports(GenericTest):
    def __init__(self, *args, **kwargs):
        super(TestImports, self).__init__(*args, **kwargs)

    def test_import_all(self):
        self.assertIn("Translator", globals())
        self.assertIn("Dictionary", globals())
        self.assertIn("Predictor", globals())
        self.assertIn("Speller", globals())
        self.assertIn("YaTranslateException", globals())
        self.assertNotIn("_YaAPIHandler", globals())

    @assert_correct_import
    def test_direct_import(self):
        import pyLinguist
        self.assertTrue(pyLinguist)
        self.assertIn("pyLinguist", locals())

    @assert_correct_import
    def test_from_init(self):
        from pyLinguist import Translator
        self.assertTrue(Translator)
        self.assertIn("Translator", locals())
        from pyLinguist import Dictionary
        self.assertTrue(Dictionary)
        self.assertIn("Dictionary", locals())
        from pyLinguist import Predictor
        self.assertTrue(Predictor)
        self.assertIn("Predictor", locals())
        from pyLinguist import Speller
        self.assertTrue(Speller)
        self.assertIn("Speller", locals())
        from pyLinguist import YaTranslateException
        self.assertTrue(YaTranslateException)
        self.assertIn("YaTranslateException", locals())

    @assert_correct_import
    def test_from_modules(self):
        from pyLinguist import Translate
        self.assertTrue(Translate)
        self.assertIn("Translate", locals())
        self.assertTrue(Translate.Translator)
        from pyLinguist import Vocabulary
        self.assertTrue(Vocabulary)
        self.assertIn("Vocabulary", locals())
        self.assertTrue(Vocabulary.Dictionary)
        self.assertTrue(Vocabulary.Speller)
        from pyLinguist import Prediction
        self.assertTrue(Prediction)
        self.assertIn("Prediction", locals())
        self.assertTrue(Prediction.Predictor)


if __name__ == "__main__":
    unittest.main()
