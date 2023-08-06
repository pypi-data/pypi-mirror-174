from __future__ import unicode_literals
import unittest
import codecs
from get_chars import get_chars
from get_tokens import read_tokens
from volt import build_d_matrix
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

class TestVoltCharsMethod(unittest.TestCase):

    def test_get_chars_simple(self):
        source = codecs.open(os.path.join(currentdir,'testData','simpleSource.txt'),encoding='utf-8')
        target = codecs.open(os.path.join(currentdir,'testData','simpleTarget.txt'),encoding='utf-8')
        chars = get_chars(source, target);

        result = codecs.open(os.path.join(currentdir,'testData','simpleResult.txt'),encoding='utf-8')
        resultLines = result.readlines()
        count = 0
        for line in resultLines:
            charsString = list(chars.items())[count][0] + ':' + list(chars.items())[count][0]
            self.assertEqual(line,charsString)
            count += 1
        
        source.close()
        target.close()
        result.close()


    def test_get_chars_complex(self):
        source = codecs.open(os.path.join(currentdir,'testData','charSource.txt'),encoding='utf-8')
        target = codecs.open(os.path.join(currentdir,'testData','charTarget.txt'),encoding='utf-8')
        chars = get_chars(source, target);

        result = codecs.open(os.path.join(currentdir,'testData','charResult.txt'),encoding='utf-8')
        resultLines = result.readlines()
        count = 0
        for line in resultLines:
            charsString = list(chars.items())[count][0] + ':' + list(chars.items())[count][0]
            self.assertEqual(line,charsString)
            count += 1
        
        source.close()
        target.close()
        result.close()

class TestVoltTokensMethod(unittest.TestCase):

    def test_read_tokens(self):
        source = codecs.open(os.path.join(currentdir,'testData','tokenTest.txt'),encoding='utf-8')
        result = codecs.open(os.path.join(currentdir,'testData','tokenResult.txt'),encoding='utf-8')

        tokens = read_tokens(source)
        resultLines = result.readlines()
        count = 0

        for line in resultLines:
            charsString = list(tokens.items())[count][0] + ':' + list(tokens.items())[count][0]
            self.assertEqual(line,charsString)
            count += 1
        
        source.close()
        result.close()

class TestVoltOTMethod(unittest.TestCase):

    def test_build_d_matrix(self):
        charSource = codecs.open(os.path.join(currentdir,'testData','charSource.txt'),encoding='utf-8')
        charTarget = codecs.open(os.path.join(currentdir,'testData','charTarget.txt'),encoding='utf-8')
        tokenSource = codecs.open(os.path.join(currentdir,'testData','tokenTest.txt'),encoding='utf-8')
        
        chars = get_chars(charSource, charTarget)
        tokens = read_tokens(tokenSource)
        d_matrix = build_d_matrix(chars, tokens)
        

if __name__== '__main__':
    unittest.main()
