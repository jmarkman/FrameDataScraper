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
        self.special_attacks = CharacterSpecialAttacks(special)
        self.throw_attacks = CharacterThrowAttacks(throw)
        self.dodges = CharacterDodgeAttributes(dodges)
        self.misc_data = CharacterMiscAttributes(misc)

class CharacterGroundAttacks(object):
    def __init__(self, moves):
        self.jabs = [j for j in moves if "jab" in j.name.lower()]
        self.tilts = [a for a in moves if "air" in a.name.lower()]
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
    def __init__(self, action_dict):
        self.name = action_dict["movename"]
        self.total_frames = action_dict["totalframes"]
        self.landing_lag = action_dict["landinglag"]
        self.notes = action_dict["notes"]

class CharacterDodge(CharacterAction):
    """Represents the data for possible dodges a characterr could make while in combat"""
    def __init__(self, dodge_dict):
        super().__init__(dodge_dict)

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