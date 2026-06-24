import json

dic = {
    "highscore_filename": "score_board.json",
    "levels&size": [["1", (50, 50)], ["2", (50, 50)], ["3", (50, 50)],
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

score_dic = {
    "ahmed": 20,
    "mohammed": 1280,
    "younes": 5220,
    "mewo": 3000,
    "kaled": 2500,
    "abd": 0,
    "bashar": 2603,
    "laith": 2301,
    "nawar": 1232,
    "elias": 1315
}
with open("score_board.json", "w") as f:
    cont = json.dumps(score_dic, indent=4)
    f.write(cont)
