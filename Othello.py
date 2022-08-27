import numpy as np
#マスの状態
EMPTY = 0#空きマス
WHITE = -1#白石
BLACK = 1#黒石
WALL = 2#壁

#ボードのサイズ
BOARD_SIZE = 8

#方向（2進数）
NONE = 0
LEFT = 2**0 #1
UPPER_LEFT = 2**1 #2
UPPER = 2**2 #4
UPPER_RIGHT = 2**3 #8
RIGHT = 2**4 #16
LOWER_RIGHT = 2**5 #32
LOWER = 2**6 #64
LOWER_LEFT = 2**7 #128

""""
ボードの変数の設定と初期配置を行うクラス
"""
class Board:
    #クラスメソッドの引数にはselfを書く
    #__init__関数はクラスオブジェクトを生成したときに初期化する
    def __init__(self):
        #全マスを空きマスに設定
        self.RawBoard = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)
        #壁の設定(numpyのスライシングを用いてる)
        #self.RawBoard[0, :] は0行目全列
        self.RawBoard[0, :] = WALL
        self.RawBoard[:, 0] = WALL
        self.RawBoard[BOARD_SIZE + 1, :] = WALL
        self.RawBoard[:, BOARD_SIZE + 1] = WALL
        #初期設定
        self.RawBoard[4, 4] = WHITE
        self.RawBoard[5, 5] = WHITE
        self.RawBoard[4, 5] = BLACK
        self.RawBoard[5, 4] = BLACK
        #手番
        self.Turns = 0
        #現在の手番の色
        self.CurrentColor = BLACK
        #置ける場所と石が返る場所
        self.MovablePos = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)
        self.MovableDir = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2), dtype=int)
        #MovablePosとMovableDirを更新
        self.initMovable()
    """
    どの方向に石が裏返るかチェックする関数
    """
    def checkMobility(self,x,y,color):
    #注目しているマスの裏返せる方向の情報が入る
        dir = 0
        #既に石がある場合はダメ
        if(self.RawBoard[x,y] != EMPTY):
            return dir
        ##左
        if(self.RawBoard[x-1, y] == - color):
            x_tmp = x-2
            y_tmp = y
            #相手の石が続いているだけループ
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp -= 1
                #相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | LEFT

        ##左上
        if(self.RawBoard[x-1, y-1] == - color):
            x_tmp = x-2
            y_tmp = y-2
            #相手の石が続いているだけループ
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp -= 1
                y_tmp -= 1
            #相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | UPPER_LEFT
    
        ##上
        if(self.RawBoard[x,y-1] == - color):
            x_tmp = x
            y_tmp = y-2
            #相手の石が続いているだけループ
            while self.RawBoard[x_tmp, y_tmp] == - color:
                y_tmp -= 1
            #相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | UPPER
    
        ##右上
        if(self.RawBoard[x+1,y-1] == - color):
            x_tmp = x+2
            y_tmp = y-2
            #相手の石が続いているだけループ
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp += 1
                y_tmp -= 1
            #相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | UPPER_RIGHT
    
        ##右
        if(self.RawBoard[x+1,y] == - color):
            x_tmp = x+2
            y_tmp = y
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp += 1
            #相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | RIGHT
    
        ##右下
        if(self.RawBoard[x+1,y+1] == - color):
            x_tmp = x+2
            y_tmp = y+2
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp += 1
                y_tmp += 1
            #相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | LOWER_RIGHT
        ##下
        if(self.RawBoard[x,y+1] == - color):
            x_tmp = x
            y_tmp = y+2
            while self.RawBoard[x_tmp, y_tmp] == - color:
                y_tmp += 1
            #相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | LOWER
        ##左下
        if(self.RawBoard[x-1,y+1] == - color):
            x_tmp = x-2
            y_tmp = y+2
            while self.RawBoard[x_tmp, y_tmp] == - color:
                x_tmp -= 1
                y_tmp += 1
            #相手の石を挟んで自分の石があればdirを更新
            if self.RawBoard[x_tmp, y_tmp] == color:
                dir = dir | LOWER_LEFT

        return dir

    """
    石を置いたことによる盤面の変化をボードに反映する関数
    """
    def flipDiscs(self, x, y):
        self.RawBoard[x,y]  = self.CurrentColor
        """
        石を置く関数
        """
    def move(self,x,y):
        #置く位置が正しいかどうかをチェック
        if x < 1 or BOARD_SIZE < x:
            return False
        if y < 1 or BOARD_SIZE < y:
            return False
        if self.MovablePos[x,y] == 0:
            return False
        #石を裏返す
        self.flipDiscs(x,y)
        #手番を進める
        self.Turns += 1
        #手番を交代する
        self.CurrentColor = - self.CurrentColor
        #MovablePosとMovableDirの更新
        self.initMovable()
        return True
    """
    MovablePosとMovableDirの更新
    """
    def initMovable(self):
        #MovablePosの初期化(すべてFalseにする)
        self.MovablePos[:, :] = False
        #すべてのマス（壁を除く）に対してループ
        for x in range(1, BOARD_SIZE+1):
            for y in range(1, BOARD_SIZE+1):
                dir = self.checkMobility(x, y, self.CurrentColor)
                self.MovableDir[x,y] = dir
                #dirが0じゃないときにMovablePosにTrueを代入
                if dir != 0:
                    self.MovablePos[x,y] = True

board = Board()
#テスト
# RawBoardの中身を確認
print('RawBoard')
for y in range(10):
    for x in range(10):
        print('{:^3}'.format(board.RawBoard[x, y]), end = '')
    print()

# MovablePosの中身を確認
print('MovablePos')
for y in range(10):
    for x in range(10):
        print('{:^3}'.format(board.MovablePos[x, y]), end = '')
    print()

# MovableDirの中身を確認
print('MovableDir')
for y in range(10):
    for x in range(10):
        print('{:^3}'.format(board.MovableDir[x, y]), end = '')
    print()
