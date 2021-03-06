import requests
import dataparser as hdp
import character as dto
from bs4 import BeautifulSoup

class ScrapeEngine(object):

    ufd_url = 'https://ultimateframedata.com/'
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
        page_data = requests.get('{0}{1}.php'.format(self.ufd_url, self.character_name))
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

        char_moves = self.__ensure_containers_hold_moves(char_moves)

        ground_data = self.__get_action_frame_data(char_moves[0])
        aerial_data = self.__get_action_frame_data(char_moves[1])
        specials_data = self.__get_action_frame_data(char_moves[2])
        throws_data = self.__get_action_frame_data(char_moves[3])
        dodges_data = self.__get_action_frame_data(char_moves[4])
        misc_data = self.__get_misc_data(char_moves[5], self.character_name)

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
            if data is None:
                if c == "hitboximg":
                    parsed_data[c] = None
                else:
                    continue
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
        # A dodge can have 4 or 5 different items because if you give a kid
        # some HTML tags he'll sprinkle them everywhere, trying to make
        # round pegs fit in square holes 
        if keys_in_pdd == 4 or keys_in_pdd == 5:
            return dto.CharacterDodge(parsed_data_dict)
        # Unless it's Terry's spot-dodge mechanic where he can u-tilt out of spot dodge
        # because the dude who wrote this website thinks an attack is a dodge
        elif parsed_data_dict["movename"].lower() == "spot dodge attack":
            return dto.TerryDodge(parsed_data_dict)
        # A throw has 7 items. 
        elif keys_in_pdd == 7:
            return dto.CharacterThrow(parsed_data_dict)
        # Unless it has 8, then it's a throw with active frames.
        elif keys_in_pdd == 8:
            return dto.CharacterThrowActiveFrames(parsed_data_dict)
        # Ok, now it DEFINITELY has to be an attack.
        else:
            return dto.CharacterAttack(parsed_data_dict)

    def __ensure_containers_hold_moves(self, retrieved_elements):
        """Some characters like Bowser might have extraneous information placed in 'move' 
        tags for some reason. Ensure that the move containers ONLY hold moves and not one-off
        pieces of data.

        Args:
            retrieved_elements: the html containers that hold all of the character's moves
        Returns:
            A sliced list that skips the first container if it has extraneous information.
            Else, returns the original list.
        """
        dumb_container = retrieved_elements[0].find(lambda tag: tag.name == 'div' and tag.get('class') == ['movecontainer', 'plain'])
        if dumb_container is None:
            return retrieved_elements
        else:
            return retrieved_elements[1:]

    def __get_misc_data(self, misc_attributes, char_name):
        """Retrieves any miscellaneous attributes for the character from their page"""
        parser = hdp.MiscDataParser(misc_attributes, char_name)
        parsed_misc_attributes = parser.get_all_misc_data()
        return parsed_misc_attributes


