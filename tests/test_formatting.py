import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from project_cbm.formatting import human_size
class Sizes(unittest.TestCase):
    def test_values_and_boundaries(self):
        for value, expected in [(None,'Unknown'),(-1,'Unknown'),(True,'Unknown'),(0,'0 bytes'),(999,'999 bytes'),(1023,'1023 bytes'),(1024,'1 KB'),(16384,'16 KB'),(1024**2-1,'1 MB'),(599*1024**2,'599 MB'),(59850*1024**2,'58.4 GB'),(1024**3,'1 GB')]:
            with self.subTest(value=value):self.assertEqual(human_size(value),expected)
