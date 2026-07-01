import json
from typing import Any


class Jsonparser:

    def __init__(self, json_path: str) -> None:
        self.path = json_path
        with open(self.path, "r") as f:
            self.json_str = self.del_comment(f.read())
            self.json_dict = json.loads(self.json_str)
            self.defaults_filled(self.json_dict)
        self.score_boards_file = self.json_dict["highscore_filename"]
        with open(self.score_boards_file, "r") as f:
            score_dict = json.load(f)
            self.sorted_board = dict(sorted(score_dict.items(),
                                     key=lambda item: item[1], reverse=True))

    def del_comment(self, json_str: str) -> str:
        cleand_str = ""
        need = False
        lines_json = json_str.split("\n")
        for line in lines_json:
            if ":" in line:
                need = False
            if not need:
                if len(line.strip()) != 0:
                    if not line.strip()[0] == "#":
                        cleand_str += line
                    else:
                        need = True
                        continue
        return self.validate_config(cleand_str)

    @staticmethod
    def check(key: str, value: str) -> str:
        defaults = {
            "highscore_filename": str,
            "lives": 3,
            "pacgum": 22,
            "points_per_pacgum": 10,
            "points_per_super_pacgum": 50,
            "points_per_ghost": 200,
            "seed": 42,
            "level_max_time": 100
        }
        if key not in defaults.keys():
            return ""
        if isinstance(defaults[key], int):
            try:
                _ = int(value)
                return f'"{key}":{value},'
            except Exception:
                return ""
        else:
            if value[0] == '"' and value.endswith('.json"'):
                return f'"{key}":{value},'
            return ""

    def validate_config(self, st: str) -> str:
        if st.strip()[0] != "{" or st.strip()[-1] != "}":
            return "{}"
        s = st.split(",")
        cleaned_str = "{"
        for pair in s:
            if pair[0] == "{":
                pair = pair[1:]
            if pair[-1] == "}":
                pair = pair[:-1]
            key, value = pair.split(":")
            key = key.strip(" \"")
            value = value.strip(" ")

            cleaned_str += self.check(key, value)
        cleaned_str = cleaned_str[:-1] + "}"
        return cleaned_str

    @staticmethod
    def defaults_filled(json_dict: dict[str, Any]) -> None:
        defaults = {
            "highscore_filename": "score_board.json",
            "lives": 3,
            "pacgum": 42,
            "points_per_pacgum": 10,
            "points_per_super_pacgum": 50,
            "points_per_ghost": 200,
            "seed": 42,
            "level_max_time": 90
        }
        for item in defaults.keys():
            try:
                if item not in json_dict.keys():
                    raise Exception(f"key {item} does not exist" +
                                    "or has invalid value, " +
                                    "resorting to default value")
            except Exception as e:
                print(f"Error: {str(e)}")
                json_dict[item] = defaults[item]

    def update_board(self, score_list: list[str | int]) -> None:

        if len(self.sorted_board):
            min_key = min(self.sorted_board,
                          key=lambda k: self.sorted_board[k])
        if len(self.sorted_board.keys()) < 10:
            self.sorted_board[score_list[0]] = score_list[1]
            self.save_data()
            return

        elif self.sorted_board[min_key] > score_list[1]:
            return
        else:
            self.sorted_board[score_list[0]] = score_list[1]
            del self.sorted_board[min_key]
            self.save_data()
            return

    def check_names(self, name: str) -> bool:
        try:
            if self.sorted_board[name]:
                return True
            return False
        except Exception:
            return False

    def save_data(self) -> None:
        with open(self.score_boards_file, "w") as f:
            json.dump(self.sorted_board, f, indent=4)
