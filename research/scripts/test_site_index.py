"""Check the document-routing contract used by the research homepage and reader."""
from pathlib import Path
import unittest

from build_site_index import ROOT, build, document_metadata, read_json


class SiteIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = read_json('document-registry')
        cls.index = build()

    def test_current_method_is_unique_and_resolves(self):
        current = [d['path'] for d in self.index['documents'] if d['role'] == 'current']
        self.assertEqual(current, [self.registry['current_path']])
        self.assertTrue((ROOT / current[0]).is_file())

    def test_registered_paths_exist_and_dates_are_explicit(self):
        for path, entry in self.registry['documents'].items():
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file())
                self.assertIn(entry['role'], self.registry['roles'])
                if entry['content_date']:
                    self.assertRegex(entry['content_date'], r'^20\d{2}-\d{2}-\d{2}$')
        # First-created filename must not override a reviewed current specification.
        meta = document_metadata(self.registry['current_path'], self.registry)
        self.assertEqual(meta['date'], self.registry['documents'][self.registry['current_path']]['content_date'])

    def test_unregistered_notes_cannot_promote_themselves_to_current(self):
        meta = document_metadata('research/new-plan-2026-09-12.md', self.registry)
        self.assertEqual((meta['role'], meta['date']), ('history', '2026-09-12'))
        unknown = document_metadata('research/new-plan.md', self.registry)
        self.assertEqual(unknown['date'], '')
        self.assertEqual(unknown['reviewed_at'], '')

    def test_history_and_external_claims_are_not_local_evidence(self):
        docs = {d['path']: d for d in self.index['documents'] if d['path']}
        self.assertEqual(docs['research/master-roadmap.md']['role'], 'history')
        self.assertEqual(docs['research/progress-2026-09-30-maniskill-rlt.md']['date'], '2026-09-30')
        self.assertEqual(docs['research/literature/rlt-followups.md']['role'], 'literature')
        self.assertEqual(docs['research/experiment-log.md']['role'], 'evidence')
        self.assertTrue(all(d['role'] == 'literature' for d in self.index['documents'] if not d['path']))

    def test_index_covers_project_documents_and_preserves_domain_boundary(self):
        actual = {p.relative_to(ROOT).as_posix() for folder in ['notes', 'research']
                  for p in (ROOT / folder).rglob('*.md')}
        indexed = {d['path'] for d in self.index['documents'] if d['path']}
        self.assertEqual(indexed, actual)
        self.assertFalse(any(p.startswith('survey-rsi/') for p in indexed))
        for entry in self.index['progress']:
            self.assertTrue((ROOT / entry['path']).is_file())

    def test_index_contains_no_git_worktree_dependent_dates(self):
        # A deploy's full checkout and a local shallow checkout must agree.
        import tempfile
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as empty:
            with patch.dict('os.environ', {'GIT_DIR': str(Path(empty) / 'missing')}):
                self.assertEqual(self.index, build())


if __name__ == '__main__':
    unittest.main()
