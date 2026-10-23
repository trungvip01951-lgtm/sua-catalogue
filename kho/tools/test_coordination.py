"""Kiểm các tình huống ghi đè thật trong kho tạm riêng, không đụng catalogue."""
import importlib.util
import json
from pathlib import Path
import tempfile
import threading
import unittest

PROJECT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('coordination', Path(__file__).with_name('catalogue.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CoordinationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='coordination-qa-', dir=PROJECT/'work')
        self.root = Path(self.tmp.name).resolve()
        assert self.root.is_relative_to((PROJECT/'work').resolve())
        self.oldroot = module.ROOT
        module.ROOT = self.root
        for sub in ['state', 'source', 'out']:
            (self.root/sub).mkdir()
        self.source = self.root/'source'/'a.pdf'; self.source.write_bytes(b'nguon bat bien')
        self.current = self.root/'out'/'a.pdf'; self.current.write_bytes(b'ban da nghiem thu')
        (self.root/'rules.md').write_text('luat da chot', encoding='utf8')
        self.write('manifest.json', {'paths': {'source':str(self.root/'source'),'output':str(self.root/'out'),'progress':'ledger'}})
        self.write('state/control_manifest.json', {'files':[{'relative_path':'rules.md','sha256':module.digest(self.root/'rules.md')}]})
        self.write('state/catalogues.json', {'catalogues':[{'source_relative':'a.pdf','current_relative':'a.pdf','source_sha256':module.digest(self.source),'current_sha256':module.digest(self.current)}]})

    def write(self, name, data):
        (self.root/name).write_text(json.dumps(data, ensure_ascii=False), encoding='utf8')

    def tearDown(self):
        module.ROOT = self.oldroot
        assert self.root.is_relative_to((PROJECT/'work').resolve())
        self.tmp.cleanup()

    def claim(self, who='ChatGPT'):
        return module.claim('a.pdf',who,'phien-'+who,'viec ro rang',1800)

    def test_two_writers_cannot_claim_same_file(self):
        self.claim()
        with self.assertRaises(module.ProjectError): self.claim('Claude')

    def test_actual_changed_current_blocks_write(self):
        lock=self.claim(); self.current.write_bytes(b'ban phien khac vua doi')
        with self.assertRaises(module.ProjectError): module.check(lock['token'],'ChatGPT','phien-ChatGPT')

    def test_actual_changed_source_blocks_claim(self):
        self.source.write_bytes(b'nguon da doi')
        with self.assertRaises(module.ProjectError): self.claim()

    def test_changed_rules_block_old_authority(self):
        lock=self.claim(); (self.root/'rules.md').write_text('luat moi', encoding='utf8')
        with self.assertRaises(module.ProjectError): module.check(lock['token'],'ChatGPT','phien-ChatGPT')

    def test_wrong_owner_cannot_release(self):
        lock=self.claim()
        with self.assertRaises(module.ProjectError): module.release(lock['token'],'Claude','phien-Claude','ban giao')

    def test_expired_lock_not_automatically_stolen(self):
        lock=self.claim()
        with module.connect() as db: db.execute('UPDATE locks SET expires=0 WHERE token=?',(lock['token'],))
        with self.assertRaises(module.ProjectError): self.claim('Claude')

    def test_release_preserves_both_catalogue_bytes(self):
        source=self.source.read_bytes(); current=self.current.read_bytes(); lock=self.claim()
        module.release(lock['token'],'ChatGPT','phien-ChatGPT','da doc lai, ban giao chung cu')
        self.assertEqual(source,self.source.read_bytes()); self.assertEqual(current,self.current.read_bytes())
        self.claim('Claude')

    def test_real_sqlite_race_has_only_one_owner(self):
        with module.connect(): pass
        results=[]; barrier=threading.Barrier(2)
        def attempt(who):
            barrier.wait()
            try: self.claim(who); results.append('held')
            except module.ProjectError: results.append('blocked')
        a=threading.Thread(target=attempt,args=('ChatGPT',)); b=threading.Thread(target=attempt,args=('Claude',))
        a.start(); b.start(); a.join(); b.join()
        self.assertCountEqual(results,['held','blocked'])


if __name__=='__main__': unittest.main(verbosity=2)
