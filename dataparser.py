from bs4 import BeautifulSoup

class FrameDataParser(object):
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
            data = self.html.find(html_element)
        else:
            data = self.html.find(html_element, element_class_name)
        return data.strip()

class AttackDataParser(FrameDataParser):
    def __init__(self, html):
        super().__init__(html)
    
    def __extract_hitbox(self):
        """
        Extract the hitbox animations from the move container html element.
        Since moves can have attributes such as different angles, some moves might
        have multiple hitbox animations.

        TODO: New characters might not have hitbox visualizations, some characters
        might not have hitbox visualizations
        """
        hitboxes = self.html.find_all("img")
        hitboxImgUrls = []
        if len(hitboxes) < 1:
           return hitboxImgUrls        
        for h in hitboxes:
            url = h['src'].strip()
            hitboxImgUrls.append(url)
        return hitboxImgUrls
