from flask import Flask, render_template, request, redirect, url_for, Blueprint, session as http_session, jsonify

from routes.admin.login.index import app as index

app = Blueprint('admin', __name__, url_prefix='/admin')

app.register_blueprint(index)
