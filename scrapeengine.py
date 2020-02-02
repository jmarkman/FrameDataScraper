import requests
import character as dto
from bs4 import BeautifulSoup

class ScrapeEngine(object):

    ufdUrl = 'https://ultimateframedata.com/'

    def __init__(self, char_name):
        self.character_name = char_name

    def get_page_for_character_name(self):
        page_data = requests.get('{0}{1}.php'.format(self.ufdUrl, self.character_name))
        return BeautifulSoup(page_data.text, 'lxml')

    def get_frame_data(self, page_data):
        # There are 6 sections: ground moves, aerials, specials, throws, dodges, and misc info
        char_moves = page_data.find_all("div", class_="moves")

        ground_data = self.__get_attack_move_frame_data(char_moves[0])
        aerial_data = self.__get_attack_move_frame_data(char_moves[1])
        specials_data = self.__get_attack_move_frame_data(char_moves[2])
        throws_data = self.__get_throws_frame_data(char_moves[3])
        dodges_data = self.__get_dodges_frame_data(char_moves[4])
        misc_data = self.__get_misc_data(char_moves[5])

        return dto.Character(self.character_name, ground_data, aerial_data, specials_data, throws_data, dodges_data, misc_data)

    def __get_attack_move_frame_data(self, moves):
        """Retrieves the ground moves from the character's frame data page

        Keyword arguments:
        moves -- The html elements that represent the current section of moves on the character page
        """
        move_html = moves.find_all("div", class_="movecontainer")
        move_list = []
        for move in move_html:
            m = self.__get_move_from_container(move)
            move_list.append(m)
        return move_list

    def __get_throws_frame_data(self, throw_container):
        return dto.CharacterThrow(throw_container)

    def __get_dodges_frame_data(self, dodge_container):
        return dto.CharacterDodge(dodge_container)

    def __get_misc_data(self, misc_attributes):
        return []

    def __get_move_from_container(self, attack_container):
        return dto.CharacterAttack(attack_container)


    