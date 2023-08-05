import unittest
import sphinxter.unittest

import test.code


class TestDual(sphinxter.unittest.TestCase):

    def test_definition(self):

        text = self.sphinxter(test.code.dual)["definition"]
        section = sphinxter.unittest.Section(text)
        self.assertSphinxterBlock(section.blocks[0])

    def test_usage(self):

        text = self.sphinxter(test.code.dual)["usage"]
        section = sphinxter.unittest.Section(text)
        self.assertSphinxterBlock(section.blocks[0], evaluate=False)


class TestMixing(sphinxter.unittest.TestCase):

    def test_evalme(self):

        text = self.sphinxter(test.code.mixing)["evalme"]
        section = sphinxter.unittest.Section(text)
        self.assertSphinxterSection(section)

    def test_leaveme(self):

        text = self.sphinxter(test.code.mixing)["leaveme"]
        section = sphinxter.unittest.Section(text)
        self.assertSphinxterSection(section, evaluate=False)

    def test_mixme(self):

        text = self.sphinxter(test.code.mixing)["mixme"]
        section = sphinxter.unittest.Section(text)
        self.assertSphinxterSection(section, evaluate=[True, False])


class TestDepth(sphinxter.unittest.TestCase):

    def test_all(self):

        self.assertSphinxter(test.code.depth, evaluate={
            "deepme.evalme": True,
            "deepme.mixme": [True, False]
        })
