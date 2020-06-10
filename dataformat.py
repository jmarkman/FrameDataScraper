import re

class MiscDataFormatter(object):
    def __init__(self, character_name):
        self.character_name = character_name

    def convert_attribute_to_readable_key(self, attribute):
        """Since the "keys" for the misc section dictionary are being
        ripped directly from the site, this method will clean the
        provided miscellaneous attribute, making it into a more
        programmer-digestable form

        Args:
            attribute: The attribute to sanitize into something readable
        Returns:
            The sanitized attribute as a string"""
        lowercase_key = attribute.lower().strip()

        # full-hop fastfall needs to have the 'frames' part removed
        if "fhff" in lowercase_key:
            lowercase_key = lowercase_key.replace("frames", '').strip()

        def switch(case):
            conditions = {
                "walk speed": "walkspd",
                "run speed": "runspd",
                "initial dash": "initdash",
                "air speed": "airspd",
                "total air acceleration": "airaccel",
                "sh": "shorthop",
                "fh": "fullhop",
                "shff": "shorthopfastfall",
                "fhff": "fullhopfastfall",
                "fall speed": "fallspd",
                "fast fall speed": "fastfallspd",
                "shield grab (grab, post-shieldstun)": "shieldgrab",
                "shield drop": "shielddrop",
                "jump squat (pre-jump frames)": "jumpsquat"
            }
            return conditions[case] if case in conditions else None
        
        result = switch(lowercase_key)

        if result is not None:
            return result
        else:
            return lowercase_key

    def format_value_associated_with_key(self, value):
        """The values associated with each section will have extra spaces
        and unnecessary string qualifiers (i.e., 'frames', '(universal)')

        Args:
            value: The data to be cleaned/formatted
        Returns:
            The sanitized value as a string"""
        clean_value = value.strip()
        if "frames" in value:
            match = re.search("[0-9]\.?[0-9]{0,}", clean_value)
            if match:
                clean_value = match.group().strip()
            else:
                print("format_value_associated_with_key failed to clean {0}".format(value))
        return clean_value
    
    def create_out_of_shield_key(self, oos_key):
        """All OOS sections are prepended with 'Out of Shield, [move]'
        All we want in this case is the move.
        
        Args:
            oos_key: The out of shield move 'key'
        Returns:
            The sanitized key as a string"""
        comma_location = oos_key.find(',')
        move = oos_key[comma_location + 1:]
        return move.strip()

class StringFormat(object):
    def __init__(self):
        super().__init__()
    
    def format_character_name(self, character_name: str):
        character_name = self.__split_name_if_necessary(character_name)
        if isinstance(character_name, str):
            return character_name.capitalize()
        else:
            pass
    
    def __split_name_if_necessary(self, name: str):
        if name.find('_') < 0:
            return name
        else:
            return name.split('_')