#!/usr/bin/env python

from flask import Flask, Response, request, render_template, url_for
from werkzeug.datastructures import Headers
import os

app = Flask(__name__)

import barnacles.views
import barnacles.api
