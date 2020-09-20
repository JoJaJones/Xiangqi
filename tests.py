import unittest
# from gradescope_utils.autograder_utils.decorators import weight, visibility
from XiangqiGame import XiangqiGame


class TestXiangqiGame(unittest.TestCase):
    
    def setUp(self):
        pass
    
    # @weight(5)
    # @visibility('visible')  # 'visible' for the first, simple test,
    # # 'after_due_date' for the rest
    def test_1(self):
        """Pass the game play given in the example; Check that game is UNFINISHED"""
        game = XiangqiGame()
        self.assertTrue(game.make_move('c1', 'e3'))
        self.assertFalse(game.is_in_check('black'))
        self.assertFalse(game.make_move('e4', 'e5'))
        self.assertEquals(game.get_game_state(), 'UNFINISHED')
    
    # @weight(1)
    # @visibility('after_due_date')  # 'visible' for the first, simple test,
    # # 'after_due_date' for the rest
    def test_2(self):
        """pawns"""
        game = XiangqiGame()
        self.assertFalse(game.make_move('a4', 'b4'))
        self.assertTrue(game.make_move('a4', 'a5'))
        self.assertTrue(game.make_move('a7', 'a6'))
        self.assertTrue(game.make_move('a5', 'a6'))
        game.make_move('f10', 'e9')
        self.assertTrue(game.make_move('a6', 'b6'))
    
    # @weight(1)
    # @visibility('after_due_date')  # 'visible' for the first, simple test,
    # # 'after_due_date' for the rest
    def test_3(self):
        """horses and elephants"""
        game = XiangqiGame()
        self.assertFalse(game.make_move('h1', 'f2'))
        self.assertTrue(game.make_move('h1', 'g3'))
        self.assertFalse(game.make_move('g3', 'h5'))
        self.assertTrue(game.make_move('g10', 'e8'))
        self.assertFalse(game.make_move('g3', 'h5'))
        self.assertTrue(game.make_move('g4', 'g5'))
        self.assertTrue(game.make_move('e8', 'g6'))
        self.assertTrue(game.make_move('g3', 'h5'))
        self.assertFalse(game.make_move('g6', 'i4'))
    
    # @weight(1)
    # @visibility('after_due_date')  # 'visible' for the first, simple test,
    # # 'after_due_date' for the rest
    def test_4(self):
        """cannons and chariots"""
        game = XiangqiGame()
        self.assertFalse(game.make_move('h3', 'a3'))
        self.assertTrue(game.make_move('h3', 'e3'))
        self.assertFalse(game.make_move('a10', 'a7'))
        self.assertFalse(game.make_move('a10', 'b9'))
        self.assertTrue(game.make_move('a10', 'a9'))
        self.assertTrue(game.make_move('e3', 'e7'))
        self.assertTrue(game.make_move('a9', 'd9'))
    
    # @weight(1)
    # @visibility('after_due_date')  # 'visible' for the first, simple test,
    # # 'after_due_date' for the rest
    def test_5(self):
        """advisors and generals"""
        game = XiangqiGame()
        self.assertFalse(game.make_move('d1', 'd2'))
        self.assertFalse(game.make_move('d1', 'c2'))
        self.assertTrue(game.make_move('d1', 'e2'))
        self.assertFalse(game.make_move('e10', 'd9'))
        self.assertTrue(game.make_move('e10', 'e9'))
        game.make_move('e4', 'e5')
        game.make_move('e7', 'e6')
        game.make_move('e5', 'e6')
        self.assertTrue(game.make_move('e9', 'd9'))
        self.assertFalse(game.make_move('e1', 'd1'))
        self.assertTrue(game.make_move('e2', 'f3'))
        self.assertFalse(game.make_move('d9', 'c9'))
        self.assertTrue(game.make_move('d9', 'e9'))
        self.assertFalse(game.make_move('e6', 'f6'))
        self.assertTrue(game.make_move('e1', 'd1'))
        self.assertFalse(game.make_move('e10', 'f9'))
    
    # @weight(1)
    # @visibility('after_due_date')  # 'visible' for the first, simple test,
    # # 'after_due_date' for the rest
    def test_6(self):
        """check"""
        # game = XiangqiGame()
        # game.make_move('h3', 'e3')
        # game.make_move('h10', 'g8')
        # game.make_move('e4', 'e5')
        # game.make_move('e10', 'e9')
        # game.make_move('h1', 'g3')
        # game.make_move('a10', 'a9')
        # game.make_move('g3', 'e4')
        # game.make_move('b8', 'c8')
        # game.make_move('e4', 'g5')
        # game.make_move('a9', 'b9')
        # self.assertFalse(game.is_in_check('black'))
        # game.make_move('g5', 'f7')  # red
        # self.assertTrue(game.is_in_check('black'))
        # game.make_move('e9', 'e10')  # black
        # self.assertFalse(game.is_in_check('black'))
        # game.make_move('e5', 'e6')
        # self.assertFalse(game.make_move('e7', 'e6'))  # black
        # game.make_move('b9', 'b3')  # black
        # self.assertFalse(game.is_in_check('black'))
        # game.make_move('e6', 'e7')
        # self.assertTrue(game.is_in_check('black'))
        # game.make_move('d10', 'e9')
        # self.assertFalse(game.is_in_check('black'))
        # game.make_move('e7', 'e8')  # red
        # self.assertFalse(game.is_in_check('red'))
        # game.make_move('b3', 'e3')  # black
        # self.assertTrue(game.is_in_check('red'))
        # game.make_move('f1', 'e2')  # red
        # self.assertFalse(game.is_in_check('red'))

        game = XiangqiGame()
        game.make_move('h3', 'e3')
        game.make_move('h10', 'g8')
        game.make_move('e4', 'e5')
        game.make_move('e10', 'e9')
        game.make_move('h1', 'g3')
        game.make_move('a10', 'a9')
        game.make_move('g3', 'e4')
        game.make_move('b8', 'c8')
        game.make_move('e4', 'g5')
        game.make_move('a9', 'b9')
        self.assertFalse(game.is_in_check('black'))
        game.make_move('g5', 'f7')  # red
        self.assertTrue(game.is_in_check('black'))
        game.make_move('e9', 'e10')  # black
        self.assertFalse(game.is_in_check('black'))
        game.make_move('e5', 'e6')
        self.assertFalse(game.make_move('e7', 'e6'))  # black
        game.make_move('b9', 'b3')  # black
        self.assertFalse(game.is_in_check('black'))
        game.make_move('e6', 'e7')
        self.assertTrue(game.is_in_check('black'))
        game.make_move('d10', 'e9')
        self.assertFalse(game.is_in_check('black'))
        game.make_move('e7', 'e8')  # red
        self.assertFalse(game.is_in_check('red'))
        game.make_move('b3', 'e3')  # black
        self.assertTrue(game.is_in_check('red'))
        game.make_move('f1', 'e2')  # red
        self.assertFalse(game.is_in_check('red'))
    
    # @weight(1)
    # @visibility('after_due_date')  # 'visible' for the first, simple test,
    # # 'after_due_date' for the rest
    def test_7(self):
        """ win for black"""
        game = XiangqiGame()
        game.make_move('b1', 'a3')
        game.make_move('h8', 'e8')
        game.make_move('b3', 'e3')
        game.make_move('b8', 'b5')
        game.make_move('h3', 'h7')
        game.make_move('e8', 'e4')
        game.make_move('e3', 'e7')
        self.assertEquals(game.get_game_state(), 'UNFINISHED')
        game.make_move('b5', 'e5')
        self.assertEquals(game.get_game_state(), 'BLACK_WON')
        self.assertFalse(game.make_move('i4', 'i5'))
    
    # @weight(1)
    # @visibility('after_due_date')  # 'visible' for the first, simple test,
    # # 'after_due_date' for the rest
    def test_8(self):
        """ win for red"""
        game = XiangqiGame()
        game.make_move('g4', 'g5')
        game.make_move('c7', 'c6')
        game.make_move('b3', 'c3')
        game.make_move('c10', 'e8')
        game.make_move('b1', 'a3')
        game.make_move('b8', 'b4')
        game.make_move('h1', 'g3')
        game.make_move('b10', 'c8')
        game.make_move('g1', 'e3')
        game.make_move('c8', 'd6')
        game.make_move('a1', 'b1')
        game.make_move('a10', 'b10')
        game.make_move('f1', 'e2')
        game.make_move('b4', 'b2')
        game.make_move('i1', 'f1')
        game.make_move('f10', 'e9')
        game.make_move('f1', 'f6')
        game.make_move('d6', 'c8')
        game.make_move('a4', 'a5')
        game.make_move('b2', 'b3')
        game.make_move('c3', 'd3')
        game.make_move('c8', 'b6')
        game.make_move('g3', 'f5')
        game.make_move('b6', 'c4')
        game.make_move('d3', 'd9')
        game.make_move('c4', 'a3')
        game.make_move('h3', 'b3')
        game.make_move('a3', 'b5')
        self.assertEquals(game.get_game_state(), 'UNFINISHED')
        game.make_move('b3', 'b10')
        self.assertEquals(game.get_game_state(), 'RED_WON')
        self.assertFalse(game.make_move('i10', 'i9'))
    
    # @weight(1)
    # @visibility('after_due_date')  # 'visible' for the first, simple test,
    # # 'after_due_date' for the rest
    def test_9(self):
        """stalemate win for red"""
        game = XiangqiGame()
        game.make_move('b1', 'a3')
        game.make_move('b8', 'b7')
        game.make_move('b3', 'c3')
        game.make_move('h8', 'h7')
        game.make_move('a1', 'b1')
        game.make_move('a10', 'a9')
        game.make_move('b1', 'b7')
        game.make_move('a9', 'a10')
        game.make_move('b7', 'a7')
        game.make_move('a10', 'a9')
        game.make_move('a7', 'c7')
        game.make_move('d10', 'e9')
        game.make_move('c7', 'e7')
        game.make_move('a9', 'a10')
        game.make_move('e7', 'g7')
        game.make_move('e9', 'd10')
        game.make_move('g7', 'h7')
        game.make_move('a10', 'a9')
        game.make_move('h7', 'i7')
        game.make_move('a9', 'a10')
        game.make_move('i7', 'i10')
        game.make_move('a10', 'a9')
        game.make_move('i10', 'h10')
        game.make_move('a9', 'a10')
        game.make_move('h10', 'g10')
        game.make_move('a10', 'a9')
        game.make_move('g10', 'g9')
        game.make_move('a9', 'a10')
        game.make_move('g9', 'c9')
        game.make_move('a10', 'a9')
        game.make_move('c9', 'c10')
        game.make_move('a9', 'a10')
        game.make_move('c10', 'b10')
        game.make_move('f10', 'e9')
        game.make_move('b10', 'a10')
        game.make_move('e10', 'f10')
        game.make_move('a10', 'a7')
        game.make_move('f10', 'e10')
        game.make_move('a7', 'e7')
        game.make_move('e10', 'f10')
        game.make_move('i1', 'i2')
        game.make_move('f10', 'e10')
        self.assertEquals(game.get_game_state(), 'UNFINISHED')
        game.make_move('i2', 'f2')
        self.assertEquals(game.get_game_state(), 'RED_WON')
