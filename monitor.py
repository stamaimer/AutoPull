# -*- coding: utf-8 -*-

import subprocess
import binascii
import logging
import hashlib
import base64
import json
import hmac
import os

import requests as sender

from flask import Flask
from flask import request

app = Flask(__name__)

global secret, path, url

logging.basicConfig(filename="push.log", level=logging.INFO, format="%(asctime)s %(message)s")


def verify(data, hash):

    digest = hmac.new(str(secret), str(data), hashlib.sha1).digest()

    signature = binascii.b2a_hex(digest)

    signature = "sha1=" + signature

    result = True if hash == signature else False

    return result


def notify(title, data):

    pusher = data["pusher"]

    head_commit = data["head_commit"]

    committer = head_commit["committer"]

    message = head_commit["message"]

    modified = head_commit["modified"]

    repository = data["repository"]["full_name"]

    notification = "repository: %s\n\ncommitter.name: %s\n\ncommitter.email: %s\n\ncommit.message: %s\n\ncommit.modified: %s\n\npusher.name: %s\n\npusher.email: %s"\
                    % (repository, committer["name"], committer["email"], message, ','.join(modified), pusher["name"], pusher["email"])

    logging.info(notification)

    payload = {"text": title, "desp": notification}

    response = sender.post(url, data=payload)

    print response.json()


def pull(path):

    os.chdir(path)

    subprocess.call(["pwd"])

    return subprocess.call(["git", "pull"])


@app.route("/", methods=["POST"])
def index():

    hash = request.headers.get("X-Hub-Signature")

    data = request.data

    if verify(data, hash):

        data = json.loads(data)

        if not pull(path[data["repository"]["name"]]):

            notify("New Push", data)

        else:

            notify("New Push Execute Failed", data)
    else:

        notify("New Push Verify Failed", data)

    return ('', 204)


if __name__ == "__main__":

    with open("config", 'r') as config:

        configuration = json.load(config)

    secret = configuration["secret"]

    port = configuration["port"]

    path = configuration["path"]

    url = configuration["url"]

    app.run(host="0.0.0.0", port=port, debug=True)
