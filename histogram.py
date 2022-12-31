""" Simpler histogram graphs form solvers csv output files """
import argparse
import glob
from os import path

class GuessData:
    guesses: list
    wrong_guesses: list

    def __init__(self) -> None:
        self.guesses = []
        self.wrong_guesses = []

def read_and_process(filepath: str) -> GuessData:
    with open(filepath, "r", encoding="utf8") as ifp:
        csv_lines = ifp.read().strip().split("\n")

    guesses = GuessData()
    hist_guesses = {}
    hist_wrong_guesses = {}
    if len(csv_lines) == 1:
        return guesses
    # read "first" line (skipping header line)
    data = csv_lines[1].split(";")
    if data[0] in hist_guesses:
        hist_guesses[data[0]] += 1
    else:
        hist_guesses[data[0]] = 1

    if data[1] in hist_wrong_guesses:
        hist_wrong_guesses[data[1]] += 1
    else:
        hist_wrong_guesses[data[1]] = 1

    if len(csv_lines) > 2:
        # process seconds line foward
        for line in csv_lines[2:]:
            data = line.split(";")
            if data[0] in hist_guesses:
                hist_guesses[data[0]] += 1
            else:
                hist_guesses[data[0]] = 1

            if data[1] in hist_wrong_guesses:
                hist_wrong_guesses[data[1]] += 1
            else:
                hist_wrong_guesses[data[1]] = 1

    # translate dict to list
    for k, v in hist_guesses.items():
        guesses.guesses.append((int(k), v))
    for k, v in hist_wrong_guesses.items():
        guesses.wrong_guesses.append((int(k), v))
    return guesses

def draw(data: list, max_value: int, lenght_label: int, lenght_column: int) -> None:
    data.sort(key=lambda k:k[0])
    for label, value in data:
        value_length = 100 * value // max_value
        padding = " "*(lenght_label-len(str(label)))
        print(f"{padding}{label}|{'='*value_length}")

if __name__ == "__main__":
    _parser = argparse.ArgumentParser(description="Simpler histogram graph from csv files")
    _parser.add_argument("-s", "--source", default=".", help = "Source folder with the csv files.")
    _parser.add_argument("-l", "--length-columns", type=int, default=20,
        help = "Max lenght of columns")

    ARGS = _parser.parse_args()

    hist_data = []
    max_guesses = 0
    max_wrong_guesses = 0
    max_label = 0
    # process data
    for file in glob.glob(path.join(ARGS.source, "*.csv")):
        data = read_and_process(file)
        max_guesses = max(max_guesses, max(data.guesses, key=lambda k:k[1])[1])
        max_wrong_guesses = max(max_wrong_guesses, max(data.wrong_guesses, key=lambda k:k[1])[1])
        max_label = max(
            max_label, 
            max(data.guesses, key=lambda k:k[0])[0], 
            max(data.wrong_guesses, key=lambda k:k[0])[0],
        )
        hist_data.append((file, data))
    max_label = len(str(max_label))
    # print data
    for filename, data in hist_data:
        print(filename)
        print("guesses")
        draw(data.guesses, max_guesses, max_label, ARGS.length_columns)
        print()
        print("wrong guesses")
        draw(data.wrong_guesses, max_wrong_guesses, max_label, ARGS.length_columns)
        print()
