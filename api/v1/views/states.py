#!/usr/bin/python3
"""states module"""
from api.v1.views import app_views
from flask import jsonify, Flask, abort, request, make_response
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def all_states():
    """return json"""
    list_state = []
    for state in storage.all(State).values():
        list_state.append(state.to_dict())
    return jsonify(list_state)


@app_views.route("/states/<string:state_id>", methods=['GET'],
                 strict_slashes=False)
def all_states_by_id(state_id):
    """return json"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<string:state_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_states_by_id(state_id):
    """return json"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def post_states():
    """return json"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    state = request.get_json()
    st = State(**state)
    st.save()
    return make_response(jsonify(st.to_dict()), 201)


@app_views.route("/states/<string:state_id>", methods=['PUT'],
                 strict_slashes=False)
def put_states_by_id(state_id):
    """return json"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if not request.get_json():
        abort(400, description='Not a JSON')

    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
