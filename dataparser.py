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
            data = self.html.find(html_element).text
        else:
            data = self.html.find(html_element, element_class_name).text
        return data.strip()

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
        if len(hitbox_container) < 1:
           return hitboxImgUrls        
        for h in hitbox_container:
            # Access the url of the hitbox animation via attribute dictionary
            url = h['data-featherlight'].strip()
            hitboxImgUrls.append(url)
        return hitboxImgUrls

class MiscDataParser(HtmlDataParser):
    def __init__(self, html):
        super().__init__(html)
    
    def get_all_misc_data(self):
        misc_data_elements = self.html.find_all("div")
        misc_data_dict = {}

        for d in misc_data_elements:
            split_text_data = d.text.split('-')
            if "/" in split_text_data[0]:
                # split by backslash, then add
            else:
                misc_data_dict[split_text_data[0]] = split_text_data[1]

    def __create_dict_key(self, text):
        pass

    def __split_by_backslash(self, text):
        pass