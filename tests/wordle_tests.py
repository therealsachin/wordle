# Copyright 2019-2020 Faculty Science Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import wordle


class TestWordle(unittest.TestCase):

    def test_is_pattern_ok(self):
        self.assertTrue(wordle.is_pattern_ok('GO...'))
        self.assertTrue(wordle.is_pattern_ok('.....'))
        self.assertTrue(wordle.is_pattern_ok('....O'))
        self.assertTrue(wordle.is_pattern_ok('GGGOO'))

        # Length not equals to 5.
        self.assertFalse(wordle.is_pattern_ok('GGGOOO'))
        self.assertFalse(wordle.is_pattern_ok('GGO'))

        # Invalid character in pattern. 
        self.assertFalse(wordle.is_pattern_ok('aGOOO'))
        self.assertFalse(wordle.is_pattern_ok('....k'))

    def test_get_pattern(self):
        self.assertEqual(wordle.get_pattern('raise', 'clock'), '.....')
        self.assertEqual(wordle.get_pattern('raise', 'arise'), 'OOGGG')
        self.assertEqual(wordle.get_pattern('raise', 'erase'), '.OOGG')
        self.assertEqual(wordle.get_pattern('raise', 'raise'), 'GGGGG')


if __name__ == '__main__':
    unittest.main()

