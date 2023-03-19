

import json
import time

import requests

#!/usr/bin/env python
# coding=utf-8
import rethinkdb as r
from flask import request
from flask_login import LoginManager, UserMixin

from webapp import app

from ..lib.flask_rethink import RethinkDB


db = RethinkDB(app)
db.init_app(app)
import traceback

from ..lib.log import *

<<<<<<< HEAD
from licensing import * 
=======
from licensing.models import *
from licensing.methods import Key, Helpers

>>>>>>> 0a086dbf871d6ddc233992a2169d8c8ea61efc1f


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "remote_logout"

ram_users = {}


class LocalUsers:
    def __init__(self):
        None

    def getUser(self, username):
        with app.app_context():
            usr = r.table("users").get(username).run(db.conn)
            if usr is None:
                return None
            usr["group_uid"] = (
                r.table("groups").get(usr["group"]).pluck("uid").run(db.conn)["uid"]
            )
        return usr

    def getUserWithGroup(self, usr):
        with app.app_context():
            if usr is None:
                return None
            usr["group_uid"] = (
                r.table("groups").get(usr["group"]).pluck("uid").run(db.conn)["uid"]
            )
        return usr


class User(UserMixin):
    def __init__(self, dict):
        self.id = dict["id"]
        self.provider = dict["provider"]
        self.category = dict["category"]
        self.uid = dict["uid"]
        self.username = dict["username"]
        self.name = dict["name"]
        self.role = dict["role"]
        self.group = dict["group"]
        self.path = (
            dict["category"]
            + "/"
            + dict["group_uid"]
            + "/"
            + dict["provider"]
            + "/"
            + dict["uid"]
            + "-"
            + dict["username"]
            + "/"
        )
        self.email = dict["email"]
        self.quota = dict["quota"]
        self.auto = dict["auto"] if "auto" in dict.keys() else False
        self.is_admin = True if self.role == "admin" else False
        self.active = dict["active"]
        self.tags = dict.get("tags", [])
        self.photo = dict.get("photo")

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False


def get_authenticated_user():
    """Check if session is authenticated by jwt

    :returns: User object if authenticated
    """

    auth = request.headers.get("Authorization", None)
    if not auth:
        return None

    response = requests.get(
        "http://isard-api:5000/api/v3/user", headers={"Authorization": auth}
    )
    if response.status_code == 200:
        user = app.localuser.getUserWithGroup(json.loads(response.text))
        if user:
            return User(user)
    return None


def logout_ram_user(username):
    del ram_users[username]


@login_manager.user_loader
def user_loader(username):
    if username not in ram_users:
        user = app.localuser.getUser(username)
        if user is None:
            return
        ram_users[username] = user
    return User(ram_users[username])


def user_reloader(username):
    user = app.localuser.getUser(username)
    if user is None:
        return
    ram_users[username] = user
    return User(ram_users[username])


"""
LOCAL AUTHENTICATION AGAINS RETHINKDB USERS TABLE
"""


class auth(object):
    def __init__(self):
        None

    def check(self, username, password):
        RSAPubKey = "<RSAKeyValue><Modulus>vD0LrQaKZa0eyV30YQJUikvUlTQsgKAjylMUO/aH5fA+7d30Yn66ziqrRxAzLStQ4MPvUDVltJr+szOq9V5B6otlotzJpDbIhq9hjqsOZsgJ4D9nsJz5NC92/oRKHEBQIbOJVInFWkAnHI4DACg/At23MUIakGMe56WiSXUYJ6faXHAt30/3+zet6akwmdg+zrs1PfNtD/Qv5ck9KcCCBdFToQtFK1282mLgZMBO9mGTt8TNk+T/1Ti9XvuGpA7KCf/pjJ9eYs/zCQuB0CkCMmUr8P6xUGbjqScEMPNdFh3Yz6pKDKlIVC4I2AFSlXHyYF5GeT5cCAZnDgDSlgncZw==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
        myauth = "WyI0MDk2NzQwMiIsIjdTMHhNbWhYcDR5c2QrY0pJeWxHNGMxNVVreGpHeHJUdTFmQWVzTGQiXQ=="               
        result = Key.activate(token=myauth,\
            rsa_pub_key=RSAPubKey,\
            product_id=19299, \
            key="FMAII-RTQTZ-SDAHH-QMGVH",\
            machine_code=Helpers.GetMachineCode(v=2))
        if result[0] == None or not Helpers.IsOnRightMachine(result[0], v=2):
            return False
        
        if username == "admin":
            user_validated = self.authentication_local(username, password)
            if user_validated:
                self.update_access(username)
                return user_validated

        
        with app.app_context():
            cfg = r.table("config").get(1).run(db.conn)
        if cfg is None:
            return False
        
        local_auth = cfg["auth"]["local"]
        
        with app.app_context():
            local_user = r.table("users").get(username).run(db.conn)
        if local_user != None:
            if local_user["provider"] == "local" and local_auth["active"]:
                user_validated = self.authentication_local(username, password)
                if user_validated:
                    self.update_access(username)
                    return user_validated
        
        return False

    def authentication_local(self, username, password):
<<<<<<< HEAD

=======
        RSAPubKey = "<RSAKeyValue><Modulus>vD0LrQaKZa0eyV30YQJUikvUlTQsgKAjylMUO/aH5fA+7d30Yn66ziqrRxAzLStQ4MPvUDVltJr+szOq9V5B6otlotzJpDbIhq9hjqsOZsgJ4D9nsJz5NC92/oRKHEBQIbOJVInFWkAnHI4DACg/At23MUIakGMe56WiSXUYJ6faXHAt30/3+zet6akwmdg+zrs1PfNtD/Qv5ck9KcCCBdFToQtFK1282mLgZMBO9mGTt8TNk+T/1Ti9XvuGpA7KCf/pjJ9eYs/zCQuB0CkCMmUr8P6xUGbjqScEMPNdFh3Yz6pKDKlIVC4I2AFSlXHyYF5GeT5cCAZnDgDSlgncZw==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
        auth = "WyI0MDk2NzQwMiIsIjdTMHhNbWhYcDR5c2QrY0pJeWxHNGMxNVVreGpHeHJUdTFmQWVzTGQiXQ=="
        result = Key.activate(token=auth,\
                   rsa_pub_key=RSAPubKey,\
                   product_id=19239, \
                   key="LLKPQ-ZGGWH-EZUHO-RNNBJ",\
                   machine_code=Helpers.GetMachineCode(v=2))

        if result[0] == None or not Helpers.IsOnRightMachine(result[0], v=2):
            return False
>>>>>>> 0a086dbf871d6ddc233992a2169d8c8ea61efc1f
        # an error occurred or the key is invalid or it cannot be activated
        # (eg. the limit of activated devices was achieved)
        #    print("The license does not work: {0}".format(result[1]))
        # else:
        # everything went fine if we are here!
            # print("The license is valid!")
            # license_key = result[0]
            # print("Feature 1: " + str(license_key.f1))
            # print("License expires: " + str(license_key.expires))
        
        with app.app_context():
            dbuser = r.table("users").get(username).run(db.conn)
            # log.info('USER:'+username)
            if dbuser is None or dbuser["active"] is not True:
                return False
            dbuser["group_uid"] = (
                r.table("groups").get(dbuser["group"]).pluck("uid").run(db.conn)["uid"]
            )
        pw = Password()
        if pw.valid(password, dbuser["password"]):
            # ~ TODO: Check active or not user
            return User(dbuser)
        else:
            return False

    def update_access(self, username):
        with app.app_context():
            r.table("users").get(username).update({"accessed": int(time.time())}).run(
                db.conn
            )


"""
PASSWORDS MANAGER
"""
import random
import string

import bcrypt


class Password(object):
    def __init__(self):
        None

    def valid(self, plain_password, enc_password):
        try:
            return bcrypt.checkpw(
                plain_password.encode("utf-8"), enc_password.encode("utf-8")
            )
        except:
            # If password is too short could lead to 'Invalid salt' Exception
            return False

    def encrypt(self, plain_password):
        return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        )

    def generate_human(self, length=6):
        chars = string.ascii_letters + string.digits + "!@#$*"
        rnd = random.SystemRandom()
        return "".join(rnd.choice(chars) for i in range(length))
