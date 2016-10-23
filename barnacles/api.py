
from barnacles import app, url_for
from flask import jsonify

import barnacles.data

@app.route("/v1")
def api_base():
    return jsonify(
        elements=[{"url": url_for('video_player', path=file), "name": file} for file in barnacles.data.get_files()]
    )
