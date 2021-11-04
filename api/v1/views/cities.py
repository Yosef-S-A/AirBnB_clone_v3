#!/usr/bin/python3
"""
a view for City objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities', methods=['GET', 'POST'])
def get_add_cities(state_id):
    """
    get city information for all cities in a specified state otherwise 404
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        cities = []
        for city in state.cities:
            cities.append(city.to_dict())
        return jsonify(cities)

    if request.method == 'POST':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'name' not in request.get_json():
            return make_response(jsonify({'error': 'Missing name'}), 400)
        kwargs = request.get_json()
        kwargs['state_id'] = state_id
        city = City(**kwargs)
        city.save()
        return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['GET', 'DELETE', 'PUT'])
def cities(city_id):
    """
    manipulate city information for specified city
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        city.delete()
        storage.save()
        return (jsonify({}))

    if request.method == 'PUT':
        if not request.get_json():
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for attr, val in request.get_json().items():
            if attr not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, attr, val)
        city.save()
        return jsonify(city.to_dict())
