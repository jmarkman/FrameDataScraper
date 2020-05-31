from bs4 import BeautifulSoup

class HtmlDataParser(object):
    """This class handles parsing out the data from the html elements representing moves"""
    def __init__(self, html):
        self.html = html

    def get_data_from_element(self, html_element, element_class_name=None):
        """Retrieves the inner text from the specified html element

        Args:
            html_element: 
                The type of element to find in the container (i.e., <img>, <p>, etc.)
            element_class_name:
                Find all elements with the class name provided to this parameter. Default
                value is None.
        Returns:
            The inner text of the element as a string
        """
        if element_class_name is None:
            data = self.html.find(lambda tag: tag.name == html_element)
        else:
            data = self.html.find(lambda tag: tag.name == html_element and tag.get('class') == [element_class_name])

        if data is not None:
            return data.text.strip()
        else:
            return None

class AttackDataParser(HtmlDataParser):
    def __init__(self, html):
        super().__init__(html)
    
    def extract_hitbox(self):
        """Extract the hitbox animations from the move container html element.
        Since moves can have attributes such as different angles, some moves might
        have multiple hitbox animations.

        TODO: New characters might not have hitbox visualizations, some characters
        might not have hitbox visualizations
        """
        # Get hitboxes container
        hitbox_container = self.html.find_all("a", class_="hitboximg")
        hitboxImgUrls = []
        if not hitbox_container:
           return None        
        for h in hitbox_container:
            # Access the url of the hitbox animation via attribute dictionary
            url = h['data-featherlight'].strip()
            hitboxImgUrls.append(url)
        return hitboxImgUrls

class MiscDataParser(HtmlDataParser):
    def __init__(self, html):
        super().__init__(html)
        # The author uses an emdash instead of a regular dash to separate data
        self.unicode_em_dash = u'\u2014'
    
    def get_all_misc_data(self):
        """Retrieves all data from the 'misc info' section of the character's frame
        data page and attempts a first-pass cleaning of the data from the page

        Returns:
            A dictionary of the attributes and their respective values from
            the 'misc info' section
        """
        # Get all the elements in the misc info container except for the grab graphic
        misc_data_elements = self.html.find(lambda tag: tag.name == "div" and tag.get('class') != ['movecontainer'])
        # Remove all the newline elements
        misc_data_elements = [n for n in misc_data_elements if n != '\n']
        # From the complete list, get all the regular divs with information
        regular_misc_data = [e for e in misc_data_elements if not e.attrs]
        # Then, from the complete list, get all the divs with out of shield information
        oos_elements = [t for t in misc_data_elements if t.attrs]
        # We're gonna shove everything in this dictionary in the end
        misc_data_dict = {}

        for msc in regular_misc_data:
            split_text_data = self.__parse_data_from_html(msc.text)
            if "/" in msc.text:
                coupled_data = self.__split_data_loosely_coupled_by_forward_slash(split_text_data)
                for k, v in coupled_data:
                    misc_data_dict[k] = v
            else:
                normal_entry_tuple = self.__create_entry_from_regular_misc_data(split_text_data)
                misc_data_dict[normal_entry_tuple[0]] = normal_entry_tuple[1]
        return misc_data_dict

    def __parse_data_from_html(self, data):
        """Parses the textual data from the HTML element representing
        the current misc data element
        
        Args:
            data:
                The current 'misc info' HTML element
        Returns:
            A list containing the split and whitespace-stripped 
            information from the element
        """
        split_data = data.split(self.unicode_em_dash)
        split_data = [x.strip() for x in split_data]
        return split_data

    def __create_entry_from_regular_misc_data(self, data):
        """Creates a tuple based on the provided data from the
        current 'misc info' row if the data is nicely formatted
        (i.e., in this case, it's a property separated by a dash
        and then a value). This tuple will contain a legible key
        for further use down the line and the associated value

        Args:
            data:
                The current 'misc info' row
        Returns:
            A tuple containing a formatted key and its value
        """
        readable_key = self.__convert_to_readable_key(data[0])
        assoc_value = self.__clean_associated_value(data[1])
        return (readable_key, assoc_value)

    def __split_data_loosely_coupled_by_forward_slash(self, split_data):
        """Creates a dictionary of all of the loosely coupled values
        that are separated by forward slashes in the 'misc attributes'
        category. This will handle the short/full hop frames row and
        the fall speed frames row.

        Args:
            split_data:
                The row data that was previously split at the emdash
        Returns:
            The loosely coupled values as a dictionary
        """
        split_keys = split_data[0].split('/')
        split_values = split_data[1].split('/')
        data_dict = {}
        for k,v in zip(split_keys, split_values):
            formatted_key = self.__convert_to_readable_key(k)
            data_dict[formatted_key] = v
        return data_dict

    def __convert_to_readable_key(self, key):
        """Since the "keys" for the misc section dictionary are being
        ripped directly from the site, this method will clean the
        provided key, making it into a more programmer-digestable form

        Args:
            key: The key to sanitize into something readable
        Returns:
            The sanitized key as a string
        """
        lowercase_key = key.lower()

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
                "shield grab (grab, post-shieldstun)": lambda x: x[:11].replace(' ', ''),
                "shield drop": lambda x: x.replace(' ', '')
            }
            return conditions[case] if case in conditions else None
        
        result = switch(lowercase_key)

        if result is not None:
            return result
        else:
            return lowercase_key

    def __create_out_of_shield_key(self, oos_key):
        pass

    def __clean_associated_value(self, data):
        """The values associated with each section will have extra spaces
        and unnecessary string qualifiers (i.e., 'frames', '(universal)')
        """
        # TODO: just strip any extra whitespace, make more specific
        return data.strip()
        