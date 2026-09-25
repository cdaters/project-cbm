"""Documentation parser regressions; no runtime or build execution."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    'release_docs', Path(__file__).resolve().parents[1] / 'tools/check_release_docs.py')
docs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(docs)


class ReleaseDocumentationParsingTests(unittest.TestCase):
    def test_title_accepts_one_badge_line_with_blank_separator(self):
        badge = '[![Release](https://img.shields.io/badge/release-1.1.0-blue)](https://example.com/release)'
        self.assertTrue(docs.has_document_title('# Project CBM\n'))
        self.assertTrue(docs.has_document_title(badge + ' ' + badge + '\n\n# Project CBM\n'))
        self.assertFalse(docs.has_document_title(badge + '\n# Project CBM\n'))
        self.assertFalse(docs.has_document_title(badge + '\n' + badge + '\n\n# Project CBM\n'))
        self.assertFalse(docs.has_document_title(badge + ' unrelated text\n\n# Project CBM\n'))

    def test_title_accepts_original_banner_with_separated_badges_and_heading(self):
        badge = '[![Release](https://img.shields.io/badge/release-1.1.0-blue)](https://example.com/release)'
        banner = ('<p align="center">\n'
                  '  <img src="assets/images/project-cbm-header.png" alt="Project CBM" width="100%">\n'
                  '</p>')
        text = badge + '\n\n' + banner + '\n\n# Project CBM\n'
        self.assertTrue(docs.has_document_title(text))
        self.assertFalse(docs.has_document_title(text.replace('</p>\n\n', '</p>\n')))
        self.assertFalse(docs.has_document_title(text.replace('project-cbm-header.png', 'other.png')))
        self.assertFalse(docs.has_document_title(badge + '\n' + text))

    def test_source_paths_exclude_document_relative_navigation(self):
        text = '[Publication](build/published-1.1.0.json) and `tools/package_manifest.py`'
        self.assertEqual(docs.source_references(text), {'tools/package_manifest.py'})
        self.assertEqual(docs.local_link_targets(text), ['build/published-1.1.0.json'])

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
