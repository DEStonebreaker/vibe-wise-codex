"""Check the distribution paths consumed by the Codex plugin loader."""

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PluginManifestTests(unittest.TestCase):
    def test_portable_identity_and_openai_extension(self):
        manifest = json.loads((ROOT / 'plugin.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['name'], 'vibe-wise-codex')
        self.assertEqual(manifest['version'], '0.1.0')
        self.assertEqual(manifest['license'], 'MIT')
        self.assertEqual(manifest['repository'],
                         'https://github.com/DEStonebreaker/vibe-wise-codex')
        extension = manifest['extensions']['com.openai']
        for relative in (extension['hooks'], extension['interface']['composerIcon']):
            with self.subTest(path=relative):
                self.assertTrue(relative.startswith('./'))
                path = (ROOT / relative).resolve()
                path.relative_to(ROOT)
                self.assertTrue(path.is_file())
        self.assertEqual(extension['hooks'], './hooks/hooks.json')
        icon = (ROOT / extension['interface']['composerIcon']).read_bytes()
        self.assertTrue(icon.startswith(b'\x89PNG\r\n\x1a\n'))

    def test_marketplace_resolves_from_repository_root(self):
        catalog = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text())
        self.assertEqual(catalog['name'], 'vibe-wise-codex')
        self.assertEqual(len(catalog['plugins']), 1)
        plugin = catalog['plugins'][0]
        self.assertEqual(plugin['name'], 'vibe-wise-codex')
        self.assertEqual(plugin['source']['source'], 'local')
        self.assertEqual((ROOT / plugin['source']['path']).resolve(), ROOT)
        self.assertEqual(plugin['policy']['installation'], 'AVAILABLE')
        self.assertEqual(plugin['policy']['authentication'], 'ON_INSTALL')
        self.assertEqual(plugin['category'], 'Productivity')

    def test_no_competing_provider_manifests_and_original_attribution(self):
        self.assertFalse((ROOT / '.claude-plugin').exists())
        self.assertFalse((ROOT / '.codex-plugin/plugin.json').exists())
        self.assertIn('Copyright (c) 2026 Noah Kim', (ROOT / 'LICENSE').read_text())


if __name__ == '__main__':
    unittest.main()
