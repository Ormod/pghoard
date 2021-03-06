"""
pghoard

Copyright (c) 2015 Ohmu Ltd
See LICENSE for details
"""
from pghoard.common import Queue
from pghoard.inotify import InotifyWatcher
import logging
import os
import platform
import shutil
import tempfile
import unittest

format_str = "%(asctime)s\t%(name)s\t%(threadName)s\t%(levelname)s\t%(message)s"
logging.basicConfig(level=logging.DEBUG, format=format_str)


class TestInotify(unittest.TestCase):
    def setUp(self):
        if platform.system() == "Darwin":
            raise unittest.SkipTest()

        self.queue = Queue()
        self.temp_dir = tempfile.mkdtemp()
        self.foo_path = os.path.join(self.temp_dir, "foo")
        with open(self.foo_path, "w") as out:
            out.write("foo")
        self.inotify = InotifyWatcher(self.queue, ignore_modified=False)
        self.inotify.add_watch(self.temp_dir)
        self.inotify.start()

    def test_create_file(self):
        with open(os.path.join(self.temp_dir, "bar"), "wb") as fp:
            fp.write(b"jee")
        self.assertEqual(self.queue.get()['type'], "CREATE")
        self.assertEqual(self.queue.get()['type'], "MODIFY")

    def test_modify(self):
        with open(os.path.join(self.temp_dir, "foo"), "ab") as fp:
            fp.write(b"jee")
        self.assertEqual(self.queue.get()['type'], "MODIFY")

    def test_delete(self):
        os.unlink(self.foo_path)
        self.assertEqual(self.queue.get()['type'], "DELETE")

    def test_move(self):
        os.rename(self.foo_path, os.path.join(self.temp_dir, "foo2"))
        event = self.queue.get()
        self.assertEqual(event['type'], "MOVE")
        self.assertEqual(event['src_path'], self.foo_path)
        self.assertEqual(event['full_path'], os.path.join(self.temp_dir, "foo2"))

    def tearDown(self):
        self.inotify.running = False
        shutil.rmtree(self.temp_dir)
