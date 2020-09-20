import unittest
from XiangqiGame import XiangqiGame


class TestXiangqi(unittest.TestCase):
    def test_0(self):
        t = XiangqiGame()
        self.assertFalse(t.make_move('h3 h2','h2'))
        self.assertTrue(t.make_move('h3','h2'))
        self.assertTrue(t.make_move('h8','h1'))
        self.assertTrue(t.make_move('h2','e2'))
        self.assertFalse(t.make_move('b10','b1'))
        self.assertTrue(t.make_move('b8','b1'))
        self.assertTrue(t.make_move('b3','e3'))
        self.assertTrue(t.make_move('e7','e6'))
        self.assertTrue(t.make_move('e4','e5'))
        self.assertTrue(t.make_move('b10','a8'))
        self.assertTrue(t.make_move('e5','e6'))
        self.assertEqual(t.get_game_state(), 'UNFINISHED')
        self.assertTrue(t.make_move('g10','e8'))
        self.assertTrue(t.make_move('e6', 'e7'))
        self.assertTrue(t.make_move('c7', 'c6'))
        self.assertTrue(t.make_move('a1', 'b1'))
        self.assertTrue(t.make_move('a8', 'c7'))
        self.assertTrue(t.make_move('b1', 'b8'))
        self.assertTrue(t.make_move('c10', 'a8'))
        self.assertTrue(t.make_move('b8', 'e8'))
        self.assertTrue(t.make_move('c7', 'e8'))
        self.assertTrue(t.make_move('e2', 'f2'))
        self.assertTrue(t.make_move('a7', 'a6'))
        self.assertTrue(t.make_move('e7', 'f7'))
        self.assertTrue(t.make_move('e8', 'c7'))
        self.assertTrue(t.make_move('f2', 'e2'))

        self.assertEqual(t.get_game_state(), 'RED_WON')

    def test_1(self):
        t = XiangqiGame()
        self.assertTrue(t.make_move('e4','e5'))
        self.assertTrue(t.make_move('i7','i6'))
        self.assertTrue(t.make_move('e5','e6'))
        self.assertTrue(t.make_move('h8','e8'))
        self.assertFalse(t.make_move('e6 f6','f6'))
        self.assertFalse(t.make_move('e6','f6'))
        self.assertTrue(t.make_move('a4','a5'))
        self.assertTrue(t.make_move('e8','f8'))
        self.assertTrue(t.make_move('e6','f6'))
        self.assertTrue(t.make_move('f8','e8'))
        self.assertFalse(t.make_move('f6','f7'))
        self.assertEqual(t.get_game_state(), 'UNFINISHED')


    def test_2(self):
        t = XiangqiGame()
        self.assertTrue(t.make_move('h3','e3'))
        self.assertTrue(t.make_move('e7','e6'))
        self.assertTrue(t.make_move('a4','a5'))
        self.assertTrue(t.make_move('e6','e5'))
        self.assertEqual(t.get_game_state(), 'UNFINISHED')
        self.assertTrue(t._players[1]._pieces["e5"].capture_causes_check((3, 4), "up"))
        self.assertTrue(t._players[1]._pieces["e5"].leaving_dir_causes_check("up"))

    def test_3(self):
        t = XiangqiGame()
        self.assertTrue(t.make_move('h3','e3'))
        self.assertTrue(t.make_move('e7','e6'))
        self.assertTrue(t.make_move('e3','e6'))
        self.assertEqual(t.get_game_state(), 'UNFINISHED')
        self.assertTrue(t._players[1]._pieces["g10"].entering_dir_causes_check((7, 4), "up"))

    def test_4(self):
        t = XiangqiGame()
        self.assertFalse(t.make_move('h1g3','g3'))
        self.assertTrue(t.make_move('h1','g3'))
        self.assertTrue(t.make_move('g7','g6'))
        self.assertTrue(t.make_move('g4','g5'))
        self.assertTrue(t.make_move('g6','g5'))
        self.assertTrue(t.make_move('g3','f5'))
        self.assertTrue(t.make_move('g5','g4'))
        self.assertTrue(t.make_move('f5','g7'))
        self.assertTrue(t.make_move('h8','h7'))
        self.assertFalse(t.make_move('g7','i8'))
        self.assertTrue(t.make_move('g7','e8'))
        self.assertTrue(t.make_move('a10','a9'))
        self.assertTrue(t.make_move('e8','g9'))
        self.assertTrue(t.is_in_check("black"))
        self.assertTrue(t.make_move("a9","f9"))
        t.make_move("h3", "h4")
        self.assertFalse(t.make_move("f9", "e9"))  # TODO fix horse logic
        self.assertTrue(t.make_move("f9", "g9"))

    def test_5(self):
        t = XiangqiGame()
        self.assertTrue(t.make_move('h3','e3'))
        self.assertTrue(t.make_move('e10','e9'))
        self.assertTrue(t.make_move('e4','e5'))
        self.assertFalse(t.make_move('g10','e10'))
        self.assertTrue(t.make_move('g10','e8'))
        self.assertTrue(t.make_move('e3','e7'))
        self.assertTrue(t.make_move('e9','f9'))
        self.assertTrue(t.make_move('b3','f3'))
        self.assertTrue(t.make_move('c10','a8'))
        self.assertTrue(t.make_move('e5','e6'))
        self.assertTrue(t.make_move('a8','c6'))
        self.assertTrue(t.make_move('e6','f6'))
        self.assertTrue(t.make_move('h8','f8'))
        self.assertFalse(t.make_move('f7','e7'))
        self.assertTrue(t.make_move('f6','e6'))
        self.assertTrue(t.make_move('f8','f1'))
        self.assertTrue(t.make_move('e6','f6'))
        self.assertFalse(t.make_move('f1f6','f6'))
        self.assertFalse(t.make_move('f1','f6'))
        self.assertEqual(t.get_game_state(), 'RED_WON')

    def test_6(self):
        t = XiangqiGame()
        self.assertTrue(t.make_move('h3','e3'))
        self.assertTrue(t.make_move('e10','e9'))
        self.assertTrue(t.make_move('e4','e5'))
        self.assertFalse(t.make_move('g10','e10'))
        self.assertTrue(t.make_move('g10','e8'))
        self.assertTrue(t.make_move('e3','e7'))
        self.assertTrue(t.make_move('e9','f9'))
        self.assertTrue(t.make_move('b3','f3'))
        self.assertTrue(t.make_move('c10','a8'))
        self.assertTrue(t.make_move('e5','e6'))
        self.assertTrue(t.make_move('a8','c6'))
        self.assertTrue(t.make_move('e6','f6'))
        self.assertTrue(t.make_move('h8','f8'))
        self.assertFalse(t.make_move('f7','e7'))
        self.assertTrue(t.make_move('f6','e6'))
        self.assertTrue(t.make_move('f8','f1'))
        self.assertTrue(t.make_move('e1','f1'))
        self.assertTrue(t.make_move('a7','a6'))
        self.assertTrue(t.make_move('e6','f6'))
        self.assertEqual(t.get_game_state(), 'RED_WON')

    def test_7(self):
        t = XiangqiGame()
        self.assertTrue(t.make_move('h1','g3'))
        self.assertTrue(t.make_move('a10','a9'))
        self.assertTrue(t.make_move('e4','e5'))
        self.assertTrue(t.make_move('a9','e9'))
        self.assertFalse(t.make_move('83','e4'))
        self.assertTrue(t.make_move('g3','e4'))
        self.assertTrue(t.make_move('b8','d8'))
        self.assertFalse(t.make_move('83','e3'))
        self.assertTrue(t.make_move('h3','e3'))
        self.assertTrue(t.make_move('h8','h7'))
        self.assertTrue(t.make_move('e5','e6'))
        self.assertTrue(t.make_move('d8','d7'))
        self.assertTrue(t.make_move('e4','f6'))
        self.assertTrue(t.make_move('a7','a6'))
        self.assertTrue(t.make_move('f6','e8'))
        self.assertTrue(t.make_move('a6','a5'))
        self.assertTrue(t.make_move('e6','e7'))
        self.assertTrue(t.make_move('c7','c6'))
        self.assertFalse(t.make_move('ee','e'))
        self.assertTrue(t.make_move('e7','d7'))
        self.assertTrue(t.make_move('c6','c5'))
        self.assertFalse(t.make_move('f8','h9'))
        self.assertFalse(t.make_move('e8','h9'))
        self.assertTrue(t.make_move('e8','g9'))
        self.assertTrue(t.make_move('e9','f9'))
        self.assertTrue(t.make_move('d7','e7'))
        self.assertTrue(t.make_move('c10','e8'))  # TODO should be valid
        self.assertFalse(t.make_move('d10','e9'))
        self.assertFalse(t.make_move('f10','e10'))
        self.assertFalse(t.make_move('f10','e9'))
        self.assertEqual(t.get_game_state(), 'UNFINISHED')
        self.assertTrue(t.make_move('c4', 'c5'))
        self.assertTrue(t.make_move('a5', 'a4'))
        self.assertTrue(t.make_move('e7','e8'))

    def test_8(self):
        t = XiangqiGame()
        self.assertTrue(t.make_move('h1','g3'))
        self.assertTrue(t.make_move('a10','a9'))
        self.assertTrue(t.make_move('e4','e5'))
        self.assertTrue(t.make_move('a9','e9'))
        self.assertFalse(t.make_move('83','e4'))
        self.assertTrue(t.make_move('g3','e4'))
        self.assertTrue(t.make_move('b8','d8'))
        self.assertFalse(t.make_move('83','e3'))
        self.assertTrue(t.make_move('h3','e3'))
        self.assertTrue(t.make_move('h8','h7'))
        self.assertTrue(t.make_move('e5','e6'))
        self.assertTrue(t.make_move('d8','d7'))
        self.assertTrue(t.make_move('e4','f6'))
        self.assertTrue(t.make_move('a7','a6'))
        self.assertTrue(t.make_move('f6','e8'))
        self.assertTrue(t.make_move('a6','a5'))
        self.assertTrue(t.make_move('e6','e7'))
        self.assertTrue(t.make_move('c7','c6'))
        self.assertFalse(t.make_move('ee','e'))
        self.assertTrue(t.make_move('e7','d7'))
        self.assertTrue(t.make_move('c6','c5'))
        self.assertFalse(t.make_move('f8','h9'))
        self.assertFalse(t.make_move('e8','h9'))
        self.assertTrue(t.make_move('e8','g9'))
        self.assertTrue(t.make_move('e9','f9'))
        self.assertTrue(t.make_move('d7','e7'))
        self.assertTrue(t.make_move('c10','e8'))  # TODO should be valid
        self.assertFalse(t.make_move('d10','e9'))
        self.assertFalse(t.make_move('f10','e10'))
        self.assertFalse(t.make_move('f10','e9'))
        self.assertEqual(t.get_game_state(), 'UNFINISHED')
        self.assertTrue(t.make_move('c4', 'c5'))
        self.assertTrue(t.make_move('a5', 'a4'))
        self.assertTrue(t.make_move('e7','e8'))
        self.assertTrue(t.make_move('d10', 'e9'))
        self.assertTrue(t.make_move('e8', 'f8'))
        self.assertTrue(t.make_move('e9', 'd10'))
        self.assertTrue(t.make_move('c5', 'c6'))
        self.assertTrue(t.make_move('f9', 'g9'))

    def test_9(self):
        t = XiangqiGame()
        self.assertTrue(t.make_move('e4','e5'))
        self.assertTrue(t.make_move('e7','e6'))
        self.assertFalse(t.make_move('h8','e8'))
        self.assertTrue(t.make_move('h3','e3'))
        self.assertTrue(t.make_move('h8','e8'))
        self.assertTrue(t.make_move('e5','e6'))
        self.assertTrue(t.make_move('a7','a6'))
        self.assertFalse(t.make_move('e6','f6'))
        self.assertTrue(t.make_move('e3','e2'))
        self.assertTrue(t.make_move('e8','e9'))
        self.assertFalse(t.make_move('g8','e10'))
        self.assertTrue(t.make_move('g1','e3'))
        self.assertTrue(t.make_move('e9','d9'))
        self.assertTrue(t.make_move('e6','f6'))
        self.assertTrue(t.make_move('g10','e8'))
        self.assertTrue(t.make_move('e3','g1'))
        self.assertTrue(t.make_move('e8','g10'))
        self.assertTrue(t.make_move('a4','a5'))
        self.assertFalse(t.make_move('f10','e9'))
        self.assertTrue(t.make_move('i7','i6'))
        self.assertFalse(t.make_move('e','2'))
        self.assertFalse(t.make_move('e2','f2'))
        self.assertFalse(t.make_move('f10','e9'))
        self.assertTrue(t.make_move('f6','e6'))
        self.assertTrue(t.make_move('f10','e9'))
        self.assertTrue(t.make_move('e6','f6'))
        self.assertTrue(t.make_move('b8','e8'))
        self.assertFalse(t.make_move('e2','e3'))
        self.assertEqual(t.get_game_state(), 'UNFINISHED')

