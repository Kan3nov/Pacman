import json


class Jsonparser:

    def __init__(self, json_path: str) -> None:
        self.path = json_path
        with open(self.path, "r") as f:
            self.json_str = self.del_comment(f.read())
            self.json_dict = json.loads(self.json_str)
            self.defaults_filled(self.json_dict)
        self.score_boards_file = self.json_dict["highscore_filename"]
        with open(self.score_boards_file, "r")as f:
            score_dict = json.load(f)
            self.sorted_board = dict(sorted(score_dict.items(),
                                     key=lambda item: -item[1]))

    @staticmethod
    def del_comment(json_str: str):
        cleand_str = ""
        need = False
        lines_json = json_str.split("\n")
        for line in lines_json:
            if ":" in line:
                need = False
            if not need:
                if not line.strip()[0] == "#":
                    cleand_str += line
                else:
                    need = True
                    continue
        return cleand_str
    
    @staticmethod
    def defaults_filled(json_dict: dict):
        defualts = {
            "highscore_filename": "score_board.json",
            "levels&size": [["1", (20, 20)], ["2", (50, 50)], ["3", (50, 50)],
                            ["4", (50, 50)], ["5", (50, 50)], ["6", (50, 50)],
                            ["7", (50, 50)], ["8", (50, 50)], ["9", (50, 50)],
                            ["10", (50, 50)]],
            "lives": 3,
            "pacgum": 42,
            "points_per_pacgum": 10,
            "points_per_super_pacgum": 50,
            "points_per_ghost": 200,
            "seed": 42,
            "level_max_time": 90
        }
        for item in defualts.keys():
            try:
                if json_dict[item] is not None and json_dict[item] != "":
                    pass
                raise KeyError(f"item {item} does not has a value")
            except KeyError:
                json_dict[item] = defualts[item]




file = Jsonparser("config.json")
#print(file.json_str)
# print(file.json_dict)
# print(file.sorted_board)