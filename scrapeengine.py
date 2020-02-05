import requests
import dataparser as hdp
import character as dto
from bs4 import BeautifulSoup

class ScrapeEngine(object):

    ufdUrl = 'https://ultimateframedata.com/'
    html_classes = [
            "hitboximg", "movename", "startup",
            "totalframes", "landinglag", "notes",
            "basedamage", "shieldlag", "shieldstun",
            "whichhitbox", "advantage", "activeframes"
    ]

    def __init__(self, char_name):
        self.character_name = char_name

    def get_page_for_character_name(self):
        """Retrieves the html for the character's frame data web page
        
        Returns:
            The html of the character's frame data page as a BeautifulSoup object
        """
        page_data = requests.get('{0}{1}.php'.format(self.ufdUrl, self.character_name))
        return BeautifulSoup(page_data.text, 'lxml')

    def get_frame_data(self, page_data):
        """This function will retrieve the frame data from the html provided by BeautifulSoup
        
        Args:
            page_data: The frame data webpage as a BeautifulSoup object
        Returns:
            A Character DTO with the character's name and their frame data
        """
        # There are 6 sections: ground moves, aerials, specials, throws, dodges, and misc info
        char_moves = page_data.find_all("div", class_="moves")

        ground_data = self.__get_action_frame_data(char_moves[0])
        aerial_data = self.__get_action_frame_data(char_moves[1])
        specials_data = self.__get_action_frame_data(char_moves[2])
        throws_data = self.__get_action_frame_data(char_moves[3])
        dodges_data = self.__get_action_frame_data(char_moves[4])
        misc_data = self.__get_misc_data(char_moves[5])

        return dto.Character(self.character_name, ground_data, aerial_data, specials_data, throws_data, dodges_data, misc_data)

    def __get_action_frame_data(self, moves):
        """Retrieves the ground moves from the character's frame data page

        Args:
            moves:
                The html elements that represent the current section of moves on the character page
        Returns:
            A list of html elements that represent a given move's data
        """
        move_html = moves.find_all("div", class_="movecontainer")
        move_list = []
        for move in move_html:
            m = self.__get_move_from_container(move)
            move_list.append(m)
        return move_list   

    def __get_move_from_container(self, attack_container):
        """Extracts the raw data we actually want from the html container

        Returns:
            A DTO that derives from the base CharacterAction class
        """
        parser = hdp.AttackDataParser(attack_container)
        parsed_data = {}
        for c in self.html_classes:
            if c == "hitboximg":
                data = parser.extract_hitbox()
            else:
                data = parser.get_data_from_element("div", c)
            # If the element couldn't be found, skip it and try the next
            # (This covers elements that BS4 reports as nonexistent 
            # or empty hitbox visualization lists)
            if data is None or not data:
                continue
            elif not data and c == "hitboximg":
                parsed_data[c] = None
            else:
                parsed_data[c] = data
        return self.__generate_dto(parsed_data)

    def __generate_dto(self, parsed_data_dict):
        """Return a child DTO based on the parent CharacterAction class based on the
        number of keys in the parsed data dictionary. The idea is that if there are 4
        keys, it's the character's dodge, etc.

        Returns:
            The appropriate DTO
        """
        keys_in_pdd = len(list(parsed_data_dict.keys()))
        # A dodge has 4 items: name, total frames, landing lag, and any misc notes
        if keys_in_pdd == 4:
            return dto.CharacterDodge(parsed_data_dict)
        # A throw has 7 items: 4 from the base class, a hitbox visualization,
        # startup frames, and base damage
        elif keys_in_pdd == 7:
            return dto.CharacterThrow(parsed_data_dict)
        else:
            return dto.CharacterAttack(parsed_data_dict)

    def __get_misc_data(self, misc_attributes):
        return []


