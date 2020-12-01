import json
import chess.pgn
import re
import sys


class P:

    def __init__(self,x, f):
        self.f = f
        self.set_pgn(x)

    def get_pgn(self):
        return self.__x

    def set_pgn(self, x):
        if x < 0:
            self.__x = 0
        elif x > 1000:
            self.__x = 1000
        else:
            self.__x = x

class PgnConverter:
    def __init__(self, pgn_path):
        self.pgn_path = pgn_path


    def convert(self, self.):
        pgn = open(f)

        print("Converting " + pgn_file +"to json...")

        json_file = open(pgn_file + '.json', 'a')

        node = chess.pgn.read_game(pgn)

        while node is not None:
            data = node.headers
            data["moves"] = []

            while node.variations:
                next_node = node.variation(0)
                data["moves"].append(re.sub(r"\{.*?\}", "", node.board().san(next_node.move)))
                node = next_node
            node = chess.pgn.read_game(pgn)
            json.dump(data, json_file, encoding='latin1')
            json_file.write('\n')

        json_file.close()