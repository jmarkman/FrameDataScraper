import scrapeengine as engine
import os

script_path = os.path.dirname(__file__)
characters_filename = 'characters.txt'
characters_filepath = os.path.join(script_path, characters_filename)

char_frame_data = []

with open(characters_filepath) as char_file:
    characters = char_file.readlines()
characters = [char_name.strip() for char_name in characters]

for char in characters:
    data_parser = engine.ScrapeEngine(char)
    char_html = data_parser.get_page_for_character_name()
    print("Getting data for {0}".format(char))
    char_data = data_parser.get_frame_data(char_html)
    char_frame_data.append(char_data)

print("ayyy")