"""Regression cases for accidental cross-domain links, including encoded paths."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('boundary', Path(__file__).with_name('check_boundary.py'))
boundary = importlib.util.module_from_spec(spec)
spec.loader.exec_module(boundary)


class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)/'survey-rsi'
        (self.root/'papers').mkdir(parents=True)
        (self.root/'README.md').write_text('# Public literature\n')
        self.card = self.root/'papers'/'example.md'

    def tearDown(self):
        self.tmp.cleanup()

    def rejected(self, content):
        self.card.write_text(content)
        self.assertTrue(boundary.check(self.root))

    def test_public_paper_not_blocked_by_acronym(self):
        self.card.write_text('[Home](../README.md)\nRLT / RouteRLT: [paper](https://arxiv.org/abs/2609.26467)\n')
        self.assertEqual(boundary.check(self.root), [])

    def test_relative_escape(self):
        self.rejected('[project](../../research/example.md)')

    def test_encoded_escape(self):
        self.rejected('[project](%2E%2E/%2E%2E/notes/example.md)')

    def test_own_repository_url(self):
        self.rejected('https://github.com/nkd-lkz/physical-self-evolution/blob/main/research/example.md')

    def test_remote_traversal(self):
        self.rejected('[project](https://github.com/nkd-lkz/physical-self-evolution/blob/main/survey-rsi/../research/example.md)')

    def test_website_reader(self):
        self.rejected('<a href="https://nkd-lkz.github.io/physical-self-evolution/reader.html?path=notes/example.md">note</a>')

    def test_json_note_escape(self):
        (self.root/'data.json').write_text('{"note":"../notes/example.md"}')
        self.assertTrue(boundary.check(self.root))

    def test_symlink(self):
        (self.root/'link.md').symlink_to(Path(self.tmp.name)/'outside.md')
        self.assertTrue(boundary.check(self.root))

    def test_known_project_heading(self):
        self.rejected('## 对当前 RLT 研究的影响\n')

    def test_survey_github_link(self):
        self.card.write_text('[card](https://github.com/nkd-lkz/physical-self-evolution/blob/main/survey-rsi/papers/example.md)')
        self.assertEqual(boundary.check(self.root), [])


if __name__ == '__main__':
    unittest.main()
