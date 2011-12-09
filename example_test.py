# coding: utf-8

import unittest

from example import LifeGame

class LifeGameTest(unittest.TestCase):
    def test_overall(self):
        game = LifeGame(10, 10)
        s = ['__*_______',
             '*_*____***',
             '_**_______',
             '__________',
             '__________',
             '__________',
             '__________',
             '_______*__',
             '**____*_*_',
             '**___*___*']
        game.reset(s)

        for i in range(10):
            game.next()

        actual = game.show()
        expected = ['__________',
                    '_______***',
                    '____*_____',
                    '_____*____',
                    '___***____',
                    '__________',
                    '_______*__',
                    '______*_*_',
                    '**____*_*_',
                    '**_____*__']

        self.assertEqual(actual, '\n'.join(expected) + '\n')


if __name__=='__main__':
    unittest.main()




