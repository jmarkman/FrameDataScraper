"""A DTO module for the various pieces of frame data information on UltimateFrameData"""

import bs4 as BeautifulSoup

class Character(object):
    """A DTO for a given character's frame data.

    Args:
        name:
            The name of the character
        ground:
            The frame data for the character's ground attacks as a CharacterGroundAttacks object
        aerial:
            The frame data for the character's aerials as a CharacterAerialAttacks object
        special:
            The frame data for the character's specials as a CharacterSpecialAttacks object
        throw:
            The frame data for the character's throws as a CharacterThrowAttacks object
        dodges:
            The frame data for the character's dodges as a CharacterDodgeAttributes object
        misc:
            Various character data such as weight, move speed, air accel, etc., as a CharacterMiscAttributes object
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
        self.jabs = [j for j in moves if "jab" in j.name.lower()]
        self.tilts = [a for a in moves if "air" in a.name.lower()]
        self.dash = next(d for d in moves if "dash" in d.name.lower())
        self.smashes = [s for s in moves if "smash" in s.name.lower()]

class ChracterAerialAttacks(object):
    def __init__(self, moves):
        self.neutral_air = next(n for n in moves if "neutral" in n.name.lower())
        self.forward_air = next(f for f in moves if "forward" in f.name.lower())
        self.back_air = next(b for b in moves if "back" in b.name.lower())
        self.up_air = next(u for u in moves if "up" in u.name.lower())
        self.down_air = next(d for d in moves if "down" in d.name.lower())

class ChracterSpecialAttacks(object):
    def __init__(self, moves):
        self.neutral_special = next(n for n in moves if "neutral" in n.name.lower())
        self.side_special = next(s for s in moves if "side" in s.name.lower())
        self.up_special = next(u for u in moves if "up" in u.name.lower())
        self.down_special = next(d for d in moves if "down" in d.name.lower())

class ChracterThrowAttacks(object):
    def __init__(self, moves):
        self.stand_grab = next(st for st in moves if "stand" in st.name.lower())
        self.dash_grab = next(dsh for dsh in moves if "dash" in dsh.name.lower())
        self.pivot_grab = next(pvt for pvt in moves if "pivot" in pvt.name.lower())
        self.pummel = next(pml for pml in moves if "pummel" in pml.name.lower())
        self.forward_throw = next(fwd for fwd in moves if "forward" in fwd.name.lower())
        self.backward_throw = next(bck for bck in moves if "back" in bck.name.lower())
        self.up_throw = next(up for up in moves if "up" in up.name.lower())
        self.down_throw = next(dwn for dwn in moves if "down" in dwn.name.lower())

class CharacterDodgeAttributes(object):
    def __init__(self, moves):
        self.spot_dodge = next(spt for spt in moves if "spot" in spt.name.lower())
        self.forward_roll = next(fwd for fwd in moves if "forward" in fwd.name.lower())
        self.backward_roll = next(bck for bck in moves if "back" in bck.name.lower())
        self.neutral_air_dodge = next(n for n in moves if "neutral" in n.name.lower())
        self.down_air_dodge = next(da for da in moves if da.name.lower() == "air dodge, down")
        self.down_diagonal_air_dodge = next(dd for dd in moves if dd.name.lower() == "air dodge, diagonally down")
        self.horizontal_air_dodge = next(hz for hz in moves if "left/right" in hz.name.lower())
        self.up_air_dodge = next(ua for ua in moves if ua.name.lower() == "air dodge, up")
        self.up_diagonal_air_dodge = next(ud for ud in moves if ud.name.lower() == "air dodge, diagonally up")

class CharacterMiscAttributes(object):
    def __init__(self, attributes):
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

class CharacterAction(object):
    """Represents the data for any possible action that a character could perform while in combat"""
    def __init__(self, html):
        self.html = html
        self.name = self.__extract_move_name()
        self.total_frames = self.__extract_total_frames()
        self.landing_lag = self.__extract_landing_lag()
        self.notes = self.__extract_notes()
    
    def __extract_move_name(self):
        """Extract the name of the move from the move container html element"""
        move_name = self.html.find("div", class_="movename").text
        return move_name.strip()

    def __extract_total_frames(self):
        """Extract the total number of frames of the move from the move container html element"""
        total_frames = self.html.find("div", class_="totalframes").text
        return total_frames.strip()
    
    def __extract_landing_lag(self):
        """Extract the landing lag from the move container html element"""
        landing_lag = self.html.find("div", class_="landinglag").text
        return landing_lag.strip()

    def __extract_notes(self):
        """Extract any miscellaneous notes about the action from the move container html element"""
        notes = self.html.find("div", class_="notes").text
        return notes.strip()

class CharacterDodge(CharacterAction):
    """Represents the data for possible dodges a characterr could make while in combat"""
    def __init__(self, html):
        super().__init__(html)

# Ugh. There's a weird edge case that isn't covered in the move abstraction.
# TODO: Revisit the class hierarchy to fix this weird abstraction "failure"
class CharacterThrow(CharacterAction):
    """Represents any possible throw a character can perform while in combat.
    Does not include command grabs.
    """
    def __init__(self, html):
        super().__init__(html)
        # Going to take an L here and just attach the properties and
        # associated methods to this class and derive from the base
        # CharacterAction class. I wanted to derive from the CharacterAttack
        # class below, but this is still just a DTO
        self.startup_frames = self.__extract_startup_frames()
        self.base_damage = self.__extract_base_damage()

    def __extract_startup_frames(self):
        """Extract the startup frames from the move container html element"""
        startup = self.html.find("div", class_="startup").text
        return startup.strip()

    def __extract_base_damage(self):
        """Extract the base damage of the action from the move container html element"""
        base_damage = self.html.find("div", class_="basedamage").text
        return base_damage.strip()

class CharacterAttack(CharacterAction):
    """Represents the data for any aggressive attack a character could make while in combat"""
    def __init__(self, html):
        super().__init__(html)
        self.startup_frames = self.__extract_startup_frames()
        self.base_damage = self.__extract_base_damage()
        self.shield_lag = self.__extract_shield_lag()
        self.shield_stun = self.__extract_shield_stun()
        self.multiple_hitboxes = self.__extract_multiple_hitboxes()
        self.advantage = self.__extract_advantage()
        self.active_frames = self.__extract_active_frames()
        self.hitbox = self.__extract_hitbox()
        
    def __extract_startup_frames(self):
        """Extract the startup frames from the move container html element"""
        startup = self.html.find("div", class_="startup").text
        return startup.strip()

    def __extract_base_damage(self):
        """Extract the base damage of the action from the move container html element"""
        base_damage = self.html.find("div", class_="basedamage").text
        return base_damage.strip()

    def __extract_shield_lag(self):
        """Extract the base damage of the action from the move container html element"""
        base_damage = self.html.find("div", class_="shieldlag").text
        return base_damage.strip()

    def __extract_shield_stun(self):
        """Extract the amount of shield stun from the move container html element"""
        shield_stun = self.html.find("div", class_="shieldstun").text
        return shield_stun.strip()

    def __extract_multiple_hitboxes(self):
        """Extract the number of extra hitboxes from the move container html element"""
        mult_hboxes = self.html.find("div", class_="whichhitbox").text
        return mult_hboxes.strip()

    def __extract_advantage(self):
        """Extract the base damage of the action from the move container html element"""
        adv = self.html.find("div", class_="advantage").text
        return adv.strip()

    def __extract_active_frames(self):
        """Extract the base damage of the action from the move container html element"""
        active_frames = self.html.find("div", class_="activeframes").text
        return active_frames.strip()

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