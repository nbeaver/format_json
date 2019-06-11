#! /usr/bin/env python3

import format_json
import tempfile
import json
import logging
import unittest

class MyTestCase(unittest.TestCase):
    def test_input_output(self, payload=''):
        fp = tempfile.NamedTemporaryFile(mode='w', delete=False)
        json.dump(payload, fp)
        logging.info(fp.name)
        fp.close()
        format_json.format_json_in_place(fp.name)
        with open(fp.name) as fp2:
            out = json.load(fp2)
        assert(out == payload)

    def test_1(self):
        self.test_input_output(1)

    def test_1_str(self):
        self.test_input_output('1')

    def test_empty_list(self):
        self.test_input_output([])

    def test_empty_object(self):
        self.test_input_output({})

    def test_numeric_list(self):
        data = list(range(10))
        self.test_input_output(data)

    def test_simple_object(self):
        data = {
            'b' : 'B',
            'c' : 'C',
            'a' : 'A',
        }
        self.test_input_output(data)

    def test_formatting(self):
        payload = {'a' : 'A', 'b': 'B', 'c': 'C'}
        expected = """{
    "a": "A",
    "b": "B",
    "c": "C"
}
"""
        fp = tempfile.NamedTemporaryFile(mode='w', delete=False)
        json.dump(payload, fp)
        logging.info(fp.name)
        fp.close()
        format_json.format_json_in_place(fp.name)
        with open(fp.name) as fp2:
            out = fp2.read()
        assert(out == expected)

if __name__ == '__main__':
    unittest.main()
