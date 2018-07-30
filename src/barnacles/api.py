
from barnacles import app
from flask import jsonify, url_for

import barnacles.data


@app.route("/v1")
def api_base():
    return jsonify(
        elements=[{"url": url_for('video_player', path=file), "name": file} for file in barnacles.data.get_files()]
    )
