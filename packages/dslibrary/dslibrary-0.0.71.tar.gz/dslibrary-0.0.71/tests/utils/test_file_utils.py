import unittest
import tempfile
import shutil
import io
import mock

from dslibrary.utils.file_utils import FileOpener, connect_to_filesystem, write_stream_with_read_on_close, \
    adapt_fsspec_storage_options, is_breakout_path, join_uri_path


class TestFileUtils(unittest.TestCase):

    def test_FileOpener_local_file(self):
        tmp_f = tempfile.mkdtemp()
        fo = FileOpener(tmp_f)
        with fo.open("x", mode="w") as f_w:
            f_w.write("abc")
        with fo.open("x", mode="r") as f_r:
            self.assertEqual(f_r.read(), "abc")
        shutil.rmtree(tmp_f)

    def test_FileOpener_s3(self):
        tmp_f = tempfile.mkdtemp()
        fo = FileOpener(tmp_f)
        def opener(uri, **kwargs):
            self.assertEqual(uri, "s3://bucket/file.csv")
            self.assertEqual(kwargs, {'mode': 'r', 'key': 'K', 'secret': 'S'})
            return io.StringIO("x")
        with mock.patch("fsspec.open", opener):
            with fo.open("s3://bucket/file.csv", mode="r", access_key="K", secret_key="S") as f_r:
                d = f_r.read()
        self.assertEqual(d, "x")
        shutil.rmtree(tmp_f)

    def test_write_stream_with_read_on_close(self):
        log = []
        f_w = write_stream_with_read_on_close('w', 'r', on_close=lambda fh: log.append(fh.read()))
        f_w.write("abc")
        f_w.write("def")
        f_w.close()
        assert log == ["abcdef"]

    def test_connect_to_filesystem(self):
        tmp_f = tempfile.mkdtemp()
        try:
            fs = connect_to_filesystem(tmp_f, for_write=True)
            with fs.open("x", mode="w") as f_w:
                f_w.write("abc")
            with fs.open("x", mode="r") as f_r:
                self.assertEqual(f_r.read(), "abc")
            self.assertEqual(fs.ls(), [{'name': 'x', 'size': 3, 'type': 'file'}])
            self.assertEqual(fs.stat("x"), {'name': 'x', 'size': 3, 'type': 'file'})
            assert fs.exists("x") is True
            assert fs.exists("y") is False
        finally:
            shutil.rmtree(tmp_f)

    def test_adapt_fsspec_storage_options(self):
        self.assertEqual(adapt_fsspec_storage_options({"access_key": "K"}), {'storage_options': {'key': 'K'}})
        self.assertEqual(adapt_fsspec_storage_options({"key": "K"}), {'storage_options': {'key': 'K'}})
        self.assertEqual(adapt_fsspec_storage_options({"storage_options": {"x": 1}, "access_key": "K", "z": 2}), {'storage_options': {'key': 'K', 'x': 1}, 'z': 2})

    def test_is_breakout_path(self):
        self.assertEqual(True,  is_breakout_path("../x"))
        self.assertEqual(False, is_breakout_path("x/.."))
        self.assertEqual(True,  is_breakout_path("x/../.."))
        self.assertEqual(False, is_breakout_path("x/y/../.."))
        self.assertEqual(False, is_breakout_path("x/y/../../z"))
        self.assertEqual(True,  is_breakout_path("x/y/../../z/../.."))
        self.assertEqual(False, is_breakout_path("./"))
        self.assertEqual(True,  is_breakout_path("./.."))

    def test_test_openable__local(self):
        """
        "?" can be placed in 'mode' during open to see if the open is allowed.
        """
        tmp_f = tempfile.mkdtemp()
        try:
            fo = FileOpener(tmp_f)
            with fo.open("x", mode="w") as f_w:
                f_w.write("abc")
            self.assertEqual(True, fo.open("x", mode="r?"))
            self.assertEqual(False, fo.open("x2", mode="r?"))
            self.assertEqual(True, fo.open("z", mode="w?"))
            self.assertEqual(False, fo.open("sub/z", mode="w?"))
        finally:
            shutil.rmtree(tmp_f)

    def test_test_openable__http(self):
        fo = FileOpener()
        def ok(*a, **k):
            return io.StringIO()
        def err(*a, **k):
            raise Exception()
        with mock.patch("urllib.request.urlopen", err):
            r = fo.open("http://whatever", mode="rb?")
            self.assertEqual(False, r)
            r = fo.open("http://whatever", mode="w?")
            self.assertEqual(True, r)
        with mock.patch("urllib.request.urlopen", ok):
            r = fo.open("http://whatever", mode="rb?")
            self.assertEqual(True, r)
            r = fo.open("http://whatever", mode="w?")
            self.assertEqual(True, r)

    def test_test_openable__fsspec(self):
        fo = FileOpener()
        class MockS3FS(object):
            def exists(self, fn):
                if "file1" in fn:
                    return True
                return False
        def fss(protocol, **kwargs):
            assert protocol.startswith("s3:")
            return MockS3FS()
        with mock.patch("dslibrary.utils.file_utils.connect_to_filesystem", fss):
            r = fo.open("s3://bucket/file1.csv", mode="r?", access_key="K", secret_key="S")
            self.assertEqual(True, r)
            r = fo.open("s3://bucket/file2.csv", mode="r?", access_key="K", secret_key="S")
            self.assertEqual(False, r)

    def test_join_uri_path(self):
        self.assertEqual("abc/def", join_uri_path("abc", "def"))
        self.assertEqual("abc/def/xyz", join_uri_path("abc", "def", "xyz"))
        self.assertEqual("http://abc/def", join_uri_path("http://abc", "def"))
        self.assertEqual("http://host/abc/def?opts", join_uri_path("http://host/abc?opts", "def"))
        self.assertEqual("http://host/abc/def#opts", join_uri_path("http://host/abc#opts", "def"))
        self.assertEqual("file://def", join_uri_path("file://", "def"))
