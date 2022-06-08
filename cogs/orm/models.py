import os
import json
from conf import conf
import datetime
from ext.help import localnow
from marshmallow import Schema, fields, pprint, post_load


# class PokemonSchema(Schema):
#     pokemonname = fields.String(required=True)
#     dexnumber = fields.Integer(required=True)
#
#     @post_load
#     def make_obj(self, data, **kwargs):
#         return Pokemon(**data)

class ProfileSchema(Schema):
    username = fields.String(required=True)
    userid = fields.Integer(required=True)
    balance = fields.Integer(required=True)
    lastTime = fields.DateTime(allow_none=True)
    dailyLastTime = fields.DateTime(allow_none=True)
    userDebt = fields.Integer(required=True)
    acl = fields.Dict()


    @post_load
    def make_obj(self, data, **kwargs):
        return Profiles(**data)

class SlotsSchema(Schema):
    jackpot = fields.Integer(required=True)

    @post_load
    def make_obj(self, data, **kwargs):
        return Slots(**data)

class PlayerSchema(Schema):
    userid = fields.Integer(required=True)
    character = fields.String(required=True)
    current_exp = fields.Integer(required=True)
    hp = fields.Integer(allow_none=True)
    mp = fields.Integer(allow_none=True)
    atk = fields.Integer(allow_none=True)
    rpg_channel = fields.Integer(allow_none=True)

    @post_load
    def make_obj(self, data, **kwargs):
        return PlayerData(**data)


    def __init__(self, user, **kwargs):
        self.user = user
        self.number = kwargs['number'] if 'number' in kwargs else None


    def save(self):
        try:
            os.makedirs(conf.orm.memberDir)
        except FileExistsError:
            pass
        with open(os.path.join(conf.orm.memberDir, str(self.user) + "_" + self.__class__.__name__ + ".json"), "w", encoding="utf-8") as file:
            json.dump(MemberSchema().dump(self), file)

# class Pokemon:
#     @classmethod
#     def obtain(cls, name=None, number=None):
#         try:
#             number = "0" * (4 - len(number)) + number
#         except TypeError:
#             pass
#         try:
#             name = name.lower()
#         except AttributeError:
#             pass
#         filepath = None
#         for root, dirs, files in os.walk(os.path.join(Linkconfig.mainDir, "cogs/dex/")):
#             for file in files:
#                 if file.endswith(".json"):
#                     if name and not number:
#                         if name in file:
#                             filepath = os.path.join(root, file)
#                             break
#                     elif number and not name:
#                         if str(number) in file:
#                             filepath = os.path.join(root, file)
#                             break
#                     else:
#                         raise ValueError("Pokemon.obtain() must either have kwargs 'name' or 'number' defined, but neither were found.")
#         if not filepath:
#             raise FileNotFoundError("No pokemon was found using the specified kwargs.")
#
#         with open(filepath, "r", encoding="utf-8") as file:
#             return PokemonSchema().load(json.load(file))
#
#     def __init__(self, pokemonname, dexnumber, **kwargs):
#         self.pokemonname = pokemonname
#         self.dexnumber = dexnumber
#
#     def save(self):
#         try:
#             os.makedirs(Linkconfig.mainDir + "cogs/dex/")
#         except FileExistsError:
#             pass
#         with open(os.path.join(Linkconfig.mainDir + "cogs/dex/", str(self.dexnumber) + "_" + self.pokemonname + "_" + self.__class__.__name__ + ".json"), "w", encoding="utf-8") as file:
#             json.dump(PokemonSchema().dump(self), file, sort_keys=True, indent=4, separators=(',', ': '))

class Profiles:
    @classmethod
    def obtain(cls, uid):
        try:
            with open(os.path.join(conf.orm.memberDir, str(uid) + "_" + cls.__name__ + ".json"), 'r', encoding='utf-8') as file:
                return ProfileSchema().load(json.load(file))
        except FileNotFoundError:
            return cls(userid=uid)

    def __init__(self, **kwargs):
        self.username = kwargs['username'] if 'username' in kwargs else 'unknown'
        self.userid = kwargs['userid']
        self.balance = kwargs['balance'] if 'balance' in kwargs else 5000
        self.lastTime = kwargs['lastTime'] if 'lastTime' in kwargs else localnow() - datetime.timedelta(days=365.25 * 20)
        self.dailyLastTime = kwargs['dailyLastTime'] if 'dailyLastTime' in kwargs else localnow() - datetime.timedelta(days=365.25 * 20)
        self.userDebt = kwargs['userDebt'] if 'userDebt' in kwargs else 0
        self.acl = kwargs['acl'] if 'acl' in kwargs else {}

    def process_dailies(self):
        delta = localnow() - self.lastTime
        if delta.total_seconds() >= 86400:
            self.currency += 500
            self.save()
            return True
        else:
            return False


    def save(self):
        try:
            os.makedirs(conf.orm.memberDir)
        except FileExistsError:
            with open(os.path.join(conf.orm.memberDir, str(self.userid) + "_" + self.__class__.__name__ + ".json"), "w", encoding="utf-8") as file:
                json.dump(ProfileSchema().dump(self), file)

class Slots:
    @classmethod
    def obtain(cls):
        try:
            with open(os.path.join(conf.orm.botDir, "jackpot_" + cls.__name__ + ".json"), 'r', encoding='utf-8') as file:
                return SlotsSchema().load(json.load(file))
        except FileNotFoundError:
            return cls()

    def __init__(self, **kwargs):
        self.DEFAULT_JACKPOT = 5000
        self.jackpot = kwargs['jackpot'] if 'jackpot' in kwargs else self.DEFAULT_JACKPOT

    def save(self):
        try:
            os.makedirs(conf.orm.botDir)
        except FileExistsError:
            with open(os.path.join(conf.orm.botDir, "jackpot_" + self.__class__.__name__ + ".json"), "w", encoding="utf-8") as file:
                json.dump(SlotsSchema().dump(self), file)

class PlayerData:
    @classmethod
    def obtain(cls, uid):
        try:
            with open(os.path.join(Linkconfig.rpgPlayerDir, str(uid) + "_" + cls.__name__ + ".json"), 'r', encoding='utf-8') as file:
                return PlayerSchema().load(json.load(file))
        except FileNotFoundError:
            return cls(userid=uid)

    def __init__(self, **kwargs):
        self.userid = kwargs['userid']
        self.character = kwargs['character'] if 'character' in kwargs else 'unknown'
        self.current_exp = kwargs['current_exp'] if 'current_exp' in kwargs else 0
        self.hp = kwargs['hp'] if 'hp' in kwargs else None
        self.mp = kwargs['mp'] if 'mp' in kwargs else None
        self.atk = kwargs['atk'] if 'atk' in kwargs else None
        self.rpg_channel = kwargs['rpg_channel'] if 'rpg_channel' in kwargs else None



    def save(self):
        try:
            os.makedirs(Linkconfig.rpgPlayerDir)
        except FileExistsError:
            with open(os.path.join(Linkconfig.rpgPlayerDir, str(self.userid) + "_" + self.__class__.__name__ + ".json"), "w", encoding="utf-8") as file:
                json.dump(PlayerSchema().dump(self), file, sort_keys=True, indent=4, separators=(',', ': '))

                # f(x) = 12.5 * (x**2) + 87.5 * x
                # x = level

                #current_level = ((-35) + sqrt((8 * x) + 1225)) / 10
                #exp_granted  = 1/5 * (current_level)









#orcs
#Dragons
#spriggans
#Cthulu
#Sentiniel
#7 deadly sins
#Hydra
#Fallen angels
#Bokoblin
#Moblin
#Hinox
#Lynels
#Demons
#warlocks
#withces
#zombies
#Harpies
#Lizalfos
#Succubus
#Bandits
#Demigods
#DOOM Guy
#Dick Kickem

#penis monster from persona (Most likely a joke)
#Link
#Wolves
#Fox
#bIRD
#cAT
#Opposing kingdoms
#dEER
#dOG
#Shrek
