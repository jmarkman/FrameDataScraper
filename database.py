import sqlite3
from os import path
from directory import DirectoryNav

class DatabaseGenerator(object):
    def __init__(self):
        self.save_folder = "FrameDataScraper_Database"
        self.database_file_name = "SmashMoves.db"
        self.character_table_name = "Characters"
        self.character_table_cols = {
            "Id": "INTEGER NOT NULL",
            "CharacterName": "TEXT"
        }
        self.move_table_name = "MoveData"
        self.move_table_cols = {}
        self.dir_nav = DirectoryNav()

    def create_database(self):
        db_save_directory = self.dir_nav.create_directory_at(self.dir_nav.get_home_path(), self.save_folder, return_new_dir_path=True)
        db_file = path.join(db_save_directory, self.database_file_name)
        return sqlite3.connect(db_file)
    
    def schema_setup(self, conn: sqlite3.Connection):
        cursor = conn.cursor()
        char_table_query = self.__build_sql_create_table_query(self.character_table_name, self.character_table_cols)
        moves_table_query = self.__build_sql_create_table_query(self.move_table_name, self.move_table_cols)
        cursor.execute(char_table_query)
        cursor.execute(moves_table_query)
        conn.commit()

    def populate_character_table(self):
        pass

    def __build_sql_create_table_query(self, table_name, table_columns: dict):
        sql =  f"create table '{self.character_table_name}' ("
        for key, value in self.character_table_cols.items():
            sql += f"'{key}' {value}"
        sql += ")"
