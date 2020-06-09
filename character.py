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
        self.ground_attacks = CharacterGroundAttacks(ground)
        self.aerial_attacks = CharacterAerialAttacks(aerial)
        self.special_attacks = self.__create_unique_dto_for_specials_if_necessary(special)
        self.throw_attacks = CharacterThrowAttacks(throw)
        self.dodges = CharacterDodgeAttributes(dodges)
        self.misc_data = CharacterMiscAttributes(misc)

    def __create_unique_dto_for_specials_if_necessary(self, specials):
        """This method shouldn't have to exist. This is a pseudo-factory
        for creating DTOs for the edge case characters that have otherwise
        broken the CharacterSpecialAttacks DTO due to the author of
        UltimateFrameData not keeping a consistent move organization scheme."""
        if self.character_name == "mii_brawler":
            return MiiBrawlerSpecialAttacks(specials)
        elif self.character_name == "mii_gunner":
            return MiiGunnerSpecialAttacks(specials)
        elif self.character_name == "mii_swordfighter":
            return MiiSwordFighterSpecialAttacks(specials)
        elif self.character_name == "terry":
            return TerrySpecialAttacks(specials)
        else:
            return CharacterSpecialAttacks(specials)
    
    # def __create_terry_dto_for_dodge_if_necessary(self, dodges):
    #     """Neither should this one, but I kinda get it since it's
    #     a weird mechanic that no one else has
    #     """
    #     if 

class CharacterGroundAttacks(object):
    def __init__(self, moves):
        self.jabs = [j for j in moves if "jab" in j.name.lower()]
        self.tilts = [a for a in moves if "tilt" in a.name.lower()]
        self.dash = next(d for d in moves if "dash" in d.name.lower())
        self.smashes = [s for s in moves if "smash" in s.name.lower()]

class CharacterAerialAttacks(object):
    def __init__(self, moves):
        self.neutral_air = next(n for n in moves if "neutral" in n.name.lower())
        self.forward_air = next(f for f in moves if "forward" in f.name.lower())
        self.back_air = next(b for b in moves if "back" in b.name.lower())
        self.up_air = next(u for u in moves if "up" in u.name.lower())
        self.down_air = next(d for d in moves if "down" in d.name.lower())

class CharacterSpecialAttacks(object):
    def __init__(self, moves):
        self.neutral_special = next(n for n in moves if "neutral" in n.name.lower())
        self.side_special = next(s for s in moves if "side" in s.name.lower())
        self.up_special = next(u for u in moves if "up" in u.name.lower())
        self.down_special = next(d for d in moves if "down" in d.name.lower())

class MiiBrawlerSpecialAttacks(object):
    """The Miis need special attention because they can have a bunch of
    different move combinations and the dude who made the frame data website 
    just shoved every last Mii move under "specials". For the Mii Brawler:
    """
    neutral_moves = ["Shot Put", "Flashing Mach Punch", "Exploding Side Kick"]
    side_moves = ["Onslaught", "Burning Dropkick", "Suplex"]
    up_moves = ["Soaring Axe Kick", "Helicopter Kick", "Thrust Uppercut"]
    down_moves = ["Head-On Assault", "Feint Jump", "Counter Throw"]

    def __init__(self, moves):
        self.neutral_special = [n for n in moves if any(m in self.neutral_moves for m in n.name.lower())]
        self.side_special = [s for s in moves if any(m in self.side_moves for m in s.name.lower())]
        self.up_special = [u for u in moves if any(m in self.up_moves for m in u.name.lower())]
        self.down_special = [d for d in moves if any(m in self.down_moves for m in d.name.lower())]

class MiiSwordFighterSpecialAttacks(object):
    """The Miis need special attention because they can have a bunch of
    different move combinations and the dude who made the frame data website 
    just shoved every last Mii move under "specials". For the Mii SwordFighter:
    """
    neutral_moves = ["Gale Strike", "Shuriken of Light", "Blurring Blade"]
    side_moves = ["Airborne Assault", "Gale Stab", "Chakram"]
    up_moves = ["Stone Scabbard", "Skyward Slash Dash", "Hero's Spin"]
    down_moves = ["Blade Counter", "Reversal Slash", "Power Thrust"]

    def __init__(self, moves):
        self.neutral_special = [n for n in moves if any(m in self.neutral_moves for m in n.name.lower())]
        self.side_special = [s for s in moves if any(m in self.side_moves for m in s.name.lower())]
        self.up_special = [u for u in moves if any(m in self.up_moves for m in u.name.lower())]
        self.down_special = [d for d in moves if any(m in self.down_moves for m in d.name.lower())]

class MiiGunnerSpecialAttacks(object):
    """The Miis need special attention because they can have a bunch of
    different move combinations and the dude who made the frame data website 
    just shoved every last Mii move under "specials". For the Mii Gunner:
    """
    neutral_moves = ["Charge Blast", "Laser Blaze", "Grenade Launch"]
    side_moves = ["Flame Pillar", "Stealth Burst", "Gunner Missile"]
    up_moves = ["Lunar Launch", "Cannon Jump Kick", "Arm Rocket"]
    down_moves = ["Echo Reflector", "Bomb Drop", "Absorbing Vortex"]

    def __init__(self, moves):
        self.neutral_special = [n for n in moves if any(m in self.neutral_moves for m in n.name.lower())]
        self.side_special = [s for s in moves if any(m in self.side_moves for m in s.name.lower())]
        self.up_special = [u for u in moves if any(m in self.up_moves for m in u.name.lower())]
        self.down_special = [d for d in moves if any(m in self.down_moves for m in d.name.lower())]

class TerrySpecialAttacks(object):
    """Terry also requires special attention because he has a "forward" 
    B/Special and a "back" B/Special. These can be grouped as Side
    B/Special and just labeled with a direction but noooooooooo, we need
    to break protocol for Terry too.
    
    Nothing's actually different about the class fields, but the population
    for the side_special field is different because of the above difference."""
    def __init__(self, moves):
        self.neutral_special = next(n for n in moves if "neutral" in n.name.lower())
        self.side_special = next(s for s in moves if "forward" in s.name.lower() or "back" in s.name.lower())
        self.up_special = next(u for u in moves if "up" in u.name.lower())
        self.down_special = next(d for d in moves if "down" in d.name.lower())

class CharacterThrowAttacks(object):
    def __init__(self, moves):
        self.stand_grab = next(st for st in moves if st.name.lower() == "grab")
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
    def __init__(self, attributes_dict):
        self.weight = attributes_dict["weight"]
        self.gravity = attributes_dict["gravity"]
        self.walk_speed = attributes_dict["walkspd"]
        self.run_speed = attributes_dict["runspd"]
        self.initial_dash_speed = attributes_dict["initdash"]
        self.air_speed = attributes_dict["airspd"]
        self.total_air_acceleration = attributes_dict["airaccel"]
        self.fall_speed = attributes_dict["fallspd"]
        self.fast_fall_speed = attributes_dict["fastfallspd"]
        self.short_hop_frames = attributes_dict["shorthop"]
        self.full_hop_frames = attributes_dict["fullhop"]
        self.short_hop_fast_fall_frames = attributes_dict["shorthopfastfall"]
        self.full_hop_fast_fall_frames = attributes_dict["fullhopfastfall"]
        self.fastest_out_of_shield_options = attributes_dict["oos"]
        self.shield_grab_post_shield_stun = attributes_dict["shieldgrab"]
        self.shield_drop = attributes_dict["shielddrop"]
        self.jump_squat = attributes_dict["jumpsquat"]

class CharacterAction(object):
    """Represents the data for any possible action that a character could perform while in combat"""
    def __init__(self, action_dict):
        self.name = action_dict["movename"]
        self.total_frames = action_dict["totalframes"]
        self.landing_lag = action_dict["landinglag"]
        self.notes = action_dict["notes"]

class CharacterDodge(CharacterAction):
    """Represents the data for possible dodges a characterr could make while in combat"""
    def __init__(self, dodge_dict):
        super().__init__(dodge_dict)

class TerryDodge(CharacterDodge):
    """Terry's a special snowflake and can u-tilt immediately out of spot dodge.
    Instead of putting this in the notes for u-tilt, where it would be relevant
    and an actual note about the move, the author of the website was like 'DUAHH
    IT'S A DODGE GUIZ' and now Terry has become another edge case that needs to be
    handled where a dodge attack.... has base damage....
    """
    def __init__(self, dodge_dict):
        super().__init__(dodge_dict)
        self.advantage = dodge_dict["advantage"]
        self.hitbox = dodge_dict["hitboximg"]
        self.active_frames = dodge_dict["activeframes"]
        self.startup = dodge_dict["startup"]

# Ugh. There's a weird edge case that isn't covered in the move abstraction.
# TODO: Revisit the class hierarchy to fix this weird abstraction "failure"
class CharacterThrow(CharacterAction):
    """Represents any possible throw a character can perform while in combat.
    Does not include command grabs.
    """
    def __init__(self, throw_dict):
        super().__init__(throw_dict)
        # Going to take an L here and just attach the properties and
        # associated methods to this class and derive from the base
        # CharacterAction class. I wanted to derive from the CharacterAttack
        # class below, but this is still just a DTO
        self.hitbox = throw_dict["hitboximg"]
        self.startup_frames = throw_dict["startup"]
        self.base_damage = throw_dict["basedamage"]

class CharacterThrowActiveFrames(CharacterThrow):
    """Some characters have grabs/throws with active frames, like Kirby."""
    def __init__(self, throw_dict):
        super().__init__(throw_dict)
        self.active_frames = throw_dict["activeframes"]

class CharacterAttack(CharacterAction):
    """Represents the data for any aggressive attack a character could make while in combat"""
    def __init__(self, attack_dict):
        super().__init__(attack_dict)
        self.startup_frames = attack_dict["startup"]
        self.base_damage = attack_dict["basedamage"]
        self.shield_lag = attack_dict["shieldlag"]
        self.shield_stun = attack_dict["shieldstun"]
        self.multiple_hitboxes = attack_dict["whichhitbox"]
        self.advantage = attack_dict["advantage"]
        self.active_frames = attack_dict.get("activeframes", None)
        # Some character attacks don't even have hitbox sections (?????)
        # so if there's no value assoc w/ the hitbox key, assign None so
        # the attack class can still be instantiated
        self.hitbox = attack_dict.get("hitboximg", None)