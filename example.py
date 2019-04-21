# Copyright (c) 2016, Patrick Uiterwijk <patrick@puiterwijk.org>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import json
import logging
import requests

from flask import Flask, g, request
from flask_oidc import OpenIDConnect

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'SomethingNotEntirelySecret',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_SCOPES': [
        "openid",
        "offline_access",
        "profile",
        "launch/patient",
        "veteran_status.read",
        "patient/Patient.read"
    ],
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_INSTROSPECTION_AUTH_METHOD': 'client_secret_basic',
    'OIDC_RESOURCE_CHECK_AUD': True,
    'OIDC_CALLBACK_ROUTE': '/varedirect'
})
oidc = OpenIDConnect(app)


@app.route('/')
def hello_world():
    if oidc.user_loggedin:
        return ('Hello, %s, <a href="/private">See private</a> '
                '<a href="/logout">Log out</a>') % \
            oidc.user_getfield('email')
    else:
        return 'Welcome anonymous, <a href="/private">Log in</a>'


@app.route('/private')
@oidc.require_login
def hello_me():
    info = oidc.user_getinfo(['email', 'openid_id'])
    token = oidc.get_access_token()
    refresh = oidc.get_refresh_token()
    tokenfile = open("accesstoken.txt", "w")
    tokenfile.write(oidc.get_access_token())
    tokenfile.close()
    html = 'Token saved in accesstoken.txt</br><a href="/">Return</a></br></br>'
    html += "Credentials: </br></br>" + str(oidc.credentials_store)
    return html

@app.route('/savetoken')
def hello_save():
    tokenfile = open("accesstoken.txt", "w")
    tokenfile.write(oidc.get_access_token())
    tokenfile.close()
    return('Token saved in accesstoken.txt</br><a href="/">Return</a>')

@app.route('/api')
@oidc.accept_token(True, ['openid'])
def hello_api():
    return json.dumps({'hello': 'Welcome %s' % g.oidc_token_info['sub']})


@app.route('/logout')
def logout():
    oidc.logout()
    return 'Hi, you have been logged out! <a href="/">Return</a>'

@app.route('/token')
def retrieve_token():
    return "Credentials: </br></br>" + str(oidc.credentials_store)

if __name__ == '__main__':
    app.run()
