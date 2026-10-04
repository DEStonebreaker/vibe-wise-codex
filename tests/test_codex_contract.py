"""Validate skill discovery and portable references without a YAML dependency.

Text checks catch packaging regressions; they do not prove teaching behavior.
"""

import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CodexContractTests(unittest.TestCase):
    def test_skills_are_named_and_explicit_only(self):
        for name in ('vibe-wise', 'vibe-wise-reset'):
            with self.subTest(skill=name):
                directory = ROOT / 'skills' / name
                content = (directory / 'SKILL.md').read_text()
                frontmatter = content.split('---', 2)[1]
                self.assertRegex(frontmatter, rf'(?m)^name: {name}$')
                self.assertRegex(frontmatter, r'(?m)^description: .+$')
                self.assertNotIn('disable-model-invocation', frontmatter)
                metadata = (directory / 'agents/openai.yaml').read_text()
                self.assertRegex(metadata, r'(?m)^policy:\n  allow_implicit_invocation: false$')
                self.assertIn('$' + name, metadata)
                match = re.search(r'(?m)^  short_description: "(.+)"$', metadata)
                self.assertIsNotNone(match)
                self.assertTrue(25 <= len(match.group(1)) <= 64)

    def test_skill_relative_markdown_links_resolve(self):
        for guide in (ROOT / 'skills').rglob('*.md'):
            for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', guide.read_text()):
                with self.subTest(guide=guide, target=target):
                    path = (guide.parent / target).resolve()
                    path.relative_to(ROOT)
                    self.assertTrue(path.is_file())

    def test_runtime_guides_have_no_claude_integration_dependencies(self):
        for guide in (ROOT / 'skills').rglob('*.md'):
            with self.subTest(guide=guide):
                content = guide.read_text()
                for obsolete in ('AskUserQuestion', 'CLAUDE_PLUGIN_ROOT',
                                 '/vibe-wise:', 'Use the Read tool', 'Use Glob'):
                    self.assertNotIn(obsolete, content)

    def test_hook_lifecycle_is_exact_and_context_is_bounded(self):
        hooks = json.loads((ROOT / 'hooks/hooks.json').read_text())['hooks']
        self.assertEqual(set(hooks), {'SessionStart'})
        self.assertEqual(len(hooks['SessionStart']), 1)
        registration = hooks['SessionStart'][0]
        for source in ('startup', 'resume', 'clear', 'compact'):
            self.assertIsNotNone(re.search(registration['matcher'], source))
        for source in ('fork', 'prestartup', 'startup-extra', ''):
            self.assertIsNone(re.search(registration['matcher'], source))
        self.assertEqual(len(registration['hooks']), 1)
        handler = registration['hooks'][0]
        self.assertEqual(handler['type'], 'command')
        self.assertEqual(handler['command'], 'python3 "${PLUGIN_ROOT}/hooks/session_start.py"')
        self.assertEqual(handler['timeout'], 5)
        self.assertEqual(handler['additionalContextLimit'], 5000)


if __name__ == '__main__':
    unittest.main()
