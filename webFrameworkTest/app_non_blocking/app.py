#! /usr/bin/env python
# A test for asyncio usage in flask app
import asyncio
import threading

from flask import Flask, current_app, jsonify, request

# from flask import g, request
import os
import sys
from loguru import logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"base dir {BASE_DIR}")
sys.path.append(f"{BASE_DIR}/app_async")
from works.dummy_work import delay, fake_work

app = Flask(__name__)


@app.route("/test", methods=["GET"])
def index():
    """
    Test api
    """
    delay(fake_work, current_app, num=request.args.get("num"))
    # delay(async_work, current_app, num=request.args.get('num'))
    return jsonify({"msg": "ok"})


@app.route("/t")
def thread_count():
    count = len(threading.enumerate())
    return jsonify({"count": count})


app.event_loop = asyncio.get_event_loop()
if __name__ == "__main__":
    # app.event_loop = asyncio.get_event_loop()
    try:
        app.run(debug=True)
    except Exception as e:
        logger.error(f"Error happened: {e}")
    finally:
        app.event_loop.stop()
        app.event_loop.run_until_complete(app.event_loop.shutdown_asyncgens())
        app.event_loop.close()
