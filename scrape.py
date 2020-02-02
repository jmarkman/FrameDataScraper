import framedataparser as fdp

data_parser = fdp.FrameDataParser('wario')
wario_html = data_parser.get_page_for_character_name()
wario_data = data_parser.get_frame_data(wario_html)

print("ayyy")