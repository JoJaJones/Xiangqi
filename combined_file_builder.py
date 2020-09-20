files_to_copy = ["constants.py", "XiangqiGame.py", "Board.py", "Piece.py", "General.py", "Advisor.py", "Chariot.py",
                 "Cannon.py", "Elephant.py", "Horse.py", "Soldier.py", "Player.py"]

with open("combined_Xiangqi.py", "w") as outfile:
    for file in files_to_copy:
        with open(file, "r") as infile:
            for line in infile:
                if "import" not in line:
                    outfile.write(line)
