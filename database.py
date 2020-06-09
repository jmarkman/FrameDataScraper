import sqlite3
from directory import DirectoryNav

class DatabaseGenerator(object):
    def __init__(self):
        self.save_folder = "FrameDataScraper_Database"
        self.database_file_name = "SmashMoves.db"
        self.character_table_name = "Characters"
        self.character_table_cols = ["Id", "CharacterName"]
        self.move_table_name = "MoveData"
        self.move_table_cols = []

    

