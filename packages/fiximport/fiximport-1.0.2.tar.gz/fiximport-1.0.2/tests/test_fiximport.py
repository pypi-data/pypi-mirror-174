import unittest
import subprocess
from pathlib import Path
from os.path import dirname


class TestFiximport(unittest.TestCase):
    def test_without_fiximport(self):
        hello_world_py_path = Path(
            dirname(__file__), "sample/b/c/hello_world.py"
        ).resolve()

        cmd = subprocess.run(["python", hello_world_py_path], capture_output=True)
        stderr = cmd.stderr.decode()

        self.assertTrue("ModuleNotFoundError" in stderr)

    def test_with_fiximport(self):
        hello_world_py_path = Path(
            dirname(__file__), "sample_fiximport/b/c/hello_world.py"
        ).resolve()

        cmd = subprocess.run(["python", hello_world_py_path], capture_output=True)
        stdout = cmd.stdout.decode()
        stderr = cmd.stderr.decode()

        self.assertTrue("Hello world" in stdout)
        self.assertTrue("ModuleNotFoundError" not in stderr)


if __name__ == "__main__":
    unittest.main()
