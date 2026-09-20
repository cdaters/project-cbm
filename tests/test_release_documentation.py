"""Documentation parser regressions; no runtime or build execution."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    'release_docs', Path(__file__).resolve().parents[1] / 'tools/check_release_docs.py')
docs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(docs)


class ReleaseDocumentationParsingTests(unittest.TestCase):
    def test_wrapped_link_label_is_checked(self):
        self.assertEqual(docs.local_link_targets('[Release\nreadiness](audit.md#results)'),
                         ['audit.md#results'])

    def test_example_links_are_not_navigation(self):
        self.assertEqual(docs.local_link_targets('```text\n[example](absent.md)\n```\n[real](present.md)'),
                         ['present.md'])

    def test_duplicate_heading_anchors_and_punctuation(self):
        self.assertEqual(docs.anchors('# Help\n## BBS / Modem\n## Help\n'),
                         {'help', 'bbs--modem', 'help-1'})

    def test_headings_in_shell_examples_are_not_anchors(self):
        self.assertEqual(docs.anchors('# Real\n```sh\n# Shell comment\n```\n## Next'),
                         {'real', 'next'})

    def test_unicode_heading_and_formatted_link(self):
        self.assertEqual(docs.anchors('# Café\n## [Content](content.md) / USB'),
                         {'café', 'content--usb'})


if __name__ == '__main__':
    unittest.main()
