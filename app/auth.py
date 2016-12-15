import json
from flask import url_for, session, request, redirect, render_template
from flask_oauthlib.client import OAuth, OAuthException
from flask_login import login_user, current_user, login_required, logout_user
from app.redirects import get_redirect_target
from app.models import User

from app import app, dao

oauth = OAuth()
facebook = oauth.remote_app('facebook',
    'facebook',
    consumer_key='1878748359026711',
    consumer_secret='10f6f8023d2bab9f96779d1f61e11e01',
    base_url='https://graph.facebook.com',
    access_token_url='/oauth/access_token',
    access_token_method='GET',
    authorize_url='https://www.facebook.com/dialog/oauth',
    request_token_params={'display': 'popup'}
)

@app.route('/login')
def login():
    print "login?"
    callback = url_for(
        'facebook_authorized',
        next=get_redirect_target(),
        _external=True
    )
    return facebook.authorize(callback=callback)

@app.route('/login/authorized')
def facebook_authorized():
    resp = facebook.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, OAuthException):
        return 'Access denied: %s' % resp.message

    me = facebook.get('/me', token=(resp['access_token'], ''))

    user = dao.get_user_by_fb(me.data['id'])

    if user and user.fb_token != resp['access_token']:
        user = dao.update_user_fb_token(user, resp['access_token'])
    if not user:
        user = dao.create_user(me.data['id'], me.data['name'], resp['access_token'])

    login_user(user)
    return redirect("/profile")

@facebook.tokengetter
def get_facebook_oauth_token():
    if current_user.is_authenticated():
        return (current_user.fb_token, '')
    return None

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
