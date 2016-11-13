#!/usr/bin/env python

from flask import Flask

app = Flask(__name__)

import barnacles.views
import barnacles.api
