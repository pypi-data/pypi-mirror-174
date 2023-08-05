import pytest
import os
import pathlib
from getcf.runner import Extractor

TEST_FILE_PATH = os.path.join(pathlib.Path(__file__).parent.absolute(), 'code.txt') 

def test_codes():
    e = Extractor()
    e.parse_data_txt(TEST_FILE_PATH)

    assert e.run()=='RVTMTL75L2D012N'