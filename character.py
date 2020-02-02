import bs4 as BeautifulSoup

class Character(object):
    """A DTO for a given character's frame data.

    Keyword arguments:
    name -- The name of the character
    ground -- The frame data for the character's ground attacks as a CharacterGroundAttacks object
    aerial -- The frame data for the character's aerials as a CharacterAerialAttacks object
    special -- The frame data for the character's specials as a CharacterSpecialAttacks object
    throw -- The frame data for the character's throws as a CharacterThrowAttacks object
    dodges -- The frame data for the character's dodges as a CharacterDodgeAttributes object
    misc -- Various character data such as weight, move speed, air accel, etc., as a CharacterMiscAttributes object
    """
    def __init__(self, name, ground, aerial, special, throw, dodges, misc):
        self.character_name = name
        self.ground_attacks = ground
        self.aerial_attacks = aerial
        self.special_attacks = special
        self.throw_attacks = throw
        self.dodges = dodges
        self.misc_data = misc

class CharacterGroundAttacks(object):
    def __init__(self, moves):
        self.jabs = [j for j in moves if "jab" in j.move_name.lower()]
        self.tilts = [a for a in moves if "air" in a.move_name.lower()]
        self.dash = next(d for d in moves if "dash" in d.move_name.lower())
        self.smashes = [s for s in moves if "smash" in s.move_name.lower()]

class ChracterAerialAttacks(object):
    def __init__(self):
        self.neutral_air = None
        self.forward_air = None
        self.back_air = None
        self.up_air = None
        self.down_air = None

class ChracterSpecialAttacks(object):
    def __init__(self):
        self.neutral_special = None
        self.side_special = None
        self.up_special = None
        self.down_special = None

class ChracterThrowAttacks(object):
    def __init__(self):
        self.stand_grab = None
        self.dash_grab = None
        self.pivot_grab = None
        self.pummel = None
        self.forward_throw = None
        self.backward_throw = None
        self.up_throw = None
        self.down_throw = None

class CharacterDodgeAttributes(object):
    def __init__(self):
        self.spot_dodge = None
        self.forward_roll = None
        self.backward_roll = None
        self.neutral_air_dodge = None
        self.down_air_dodge = None
        self.down_diagonal_air_dodge = None
        self.horizontal_air_dodge = None
        self.up_air_dodge = None
        self.up_diagonal_air_dodge = None

class CharacterMiscAttributes(object):
    def __init__(self):
        self.weight = 0.0
        self.gravity = 0.0
        self.walk_speed = 0.0
        self.run_speed = 0.0
        self.initial_dash_speed = 0.0
        self.air_speed = 0.0
        self.total_air_acceleration = 0.0
        self.short_hop_frames = 0
        self.full_hop_frames = 0
        self.short_hop_fast_fall_frames = 0
        self.full_hop_fast_fall_frames = 0
        self.fastest_out_of_shield_options = []
        self.shield_grab_post_shield_stun = 0
        self.shield_drop = 11
        self.jump_squat = 3


class CharacterMove(object):
    """
    This class represents any single move a character might have
    """
    def __init__(self, move_html):
        self.move_html = move_html
        self.move_name = __extract_move_name()
        self.startup_frames = __extract_startup_frames()
        self.advantage = __extract_advantage()
        self.active_frames = __extract_active_frames()
        self.hitbox = None
        self.total_frames = None
        self.landing_lag = None
        self.move_notes = None
        self.base_damage = None
        self.shield_lag = None
        self.shield_stun = None
        self.which_hitbox = None


    def __extract_move_name(self):
        """Extract the name of the move from the move container html element"""
        move_name = strip(self.move_html.find("div", class_="movename").text)
        return move_name
    

    def __extract_startup_frames(self):
        """Extract the startup frames from the move container html element"""
        startup = strip(self.move_html.find("div", class_="startup").text)
        return startup


    def __extract_advantage(self):
        """Extract the advantage on hit from the move container html element"""
        adv = strip(self.move_html.find("div", class_="advantage").text)
        return adv

    def __extract_active_frames(self):
        """Extract the number of active frames from the move container html element"""
        active_frames = strip(self.move_html.find("div", class_="movename").text)
        return active_frames


    def __extract_hitbox(self):
        """
        Extract the hitbox animations from the move container html element.
        Since moves can have attributes such as different angles, some moves might
        have multiple hitbox animations.

        TODO: New characters might not have hitbox visualizations, some characters
        might not have hitbox visualizations
        """
        hitboxes = self.move_html.find_all("a", class_="hitboximg")
        hitboxImgUrls = []
        if len(hitboxes) < 1:
           return hitboxImgUrls        
        for h in hitboxes:
            hitboxImgUrls.append(h['src'])
        return hitboxImgUrls

    # def __extract_move_name(self):
    #     move_name = strip(self.move_html.find("div", class_="movename").text)
    #     return move_name

    # def __extract_move_name(self):
    #     move_name = strip(self.move_html.find("div", class_="movename").text)
    #     return move_name

    # def __extract_move_name(self):
    #     move_name = strip(self.move_html.find("div", class_="movename").text)
    #     return move_name

    # def __extract_move_name(self):
    #     move_name = strip(self.move_html.find("div", class_="movename").text)
    #     return move_name