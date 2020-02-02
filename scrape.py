import scrapeengine as engine

data_parser = engine.ScrapeEngine('wario')
wario_html = data_parser.get_page_for_character_name()
wario_data = data_parser.get_frame_data(wario_html)

print("ayyy")