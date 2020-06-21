import copy 
from dlgo.gotypes import Player

class Move():
    # 기사가 자기 차례에 할 수 있는 행동(is_play, is_pass, is_resign)을 설정
    def __init__(self, point = None, is_pass = False, is_resign = False):
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    # 바둑판에 돌 놓기
    def play(cls, point):
        return Move(point = point)
    
    @classmethod
    # 이 수는 차례를 넘긴다.
    def pass_turn(cls):
        return Move(is_pass = True)
    
    @classmethod
    # 이 수는 대국을 포기한다
    def resign(cls):
        return Move(is_resign = True)

# 이음을 set으로 인코딩
class GoString():
    # 바둑 이음은 같은 색 돌이 연속적으로 연결된 형식이다
    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)
    
    def remove_liberty(self, point):
        self.liberties.remove(point)
    
    def add_liberty(self, point):
        self.liberties.add(point)
    
    # 양 선수의 이음의 모든 돌을 저장한 새 이음을 반환
    def merged_with(self, go_string):
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
            return GoString(
                self.color,
                combined_stones,
                (self.liberties | go_string.liberties) - combined_stones)

    @property
        def num_liberties(self):
            return len(self.liberties)
        
        def __eq__(self, other):
                return isinstance(other, GoString) and \
                    self.color == other.color and \
                    self.stones == other.stones and \
                    self.liberties == other.liberties

# 바둑판
class Board():
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}

    # 활로 파악용 이웃 점 확인
    def place_stone(self, player, point):
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None
        adjacent_same_color = []
        adjacent_opposite_color = []
        liberties = []
        for neightbor in point.neightbors():
            if not self.is_on_grid(neightbor):
                continue
            neightbor_string = self._grid.get(neightbor)
            if neightbor_string is None:
                liberties.append(neightbor)
            elif neightbor_string.color == player:
                if neightbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neightbor_string)
            else:
                if neightbor_string not adjacent_opposite_color:
                    adjacent_opposite_color.append(neightbor_string)
        new_string = GoString(player, [point], liberties)
        
        # 같은 색의 인접한 이음을 합치기
        for same_color_string in adjacent_same_color:
            new_string = new_string.merged_with(same_color_string)
        for new_string_point in new_string.stones:
            self._grid[new_string_point] = new_string
        # 다른 색의 근접한 이음의 활로를 줄임
        for other_color_string in adjacent_opposite_color:
            other_color_string.remove_liberty(point)
        # 다른 색 이음의 활로가 0이 되면 그 돌을 제거
        for other_color_string in adjacent_opposite_color:
            if other_color_string.num_liberties == 0:
                self._remove_string(other_color_string)
        
        def _remove_string(self, string):
            for point in string.stones:
                for neightbor in point.neightbors():
                    neightbor_string = self._grid.get(neightbor)
                    if neightbor_string is None:
                        continue
                    if neightbor_string is not string:
                        neightbor_string.add_liberty(point)
                self._grid[point] = None
    
    # 돌 놓기와 따내기 유틸리티 메서드
    def is_on_grid(self, point):
        return 1 <= point.row <= self.num_rows and \
            1 <= point.col <= self.num_cols
        
    def get(self, point):
        string = self._grid.get(point)
        if string is None:
            return None
        return string.color
    
    # 해당 점의 돌에 연결된 모든 이음을 반환
    def get_go_string(self, point):
        string = self._grid.get(point)
        if string is None:
            return None
        return string