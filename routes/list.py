from flask import Blueprint, request, jsonify
from models.list import List
from main import db
from ai.recommendations import RecommendationEngine

list_routes = Blueprint('list', __name__)

recommendation_engine = RecommendationEngine([])

@list_routes.route('/create', methods=['POST'])
def create_list():
    data = request.json
    if not data or not data.get('name') or not data.get('description') or not data.get('creator_id'):
        return jsonify({"error": "Name, description, and creator_id are required"}), 400
    
    new_list = List(
        name=data['name'],
        description=data['description'],
        creator_id=data['creator_id']
    )
    
    db.session.add(new_list)
    db.session.commit()
    
    # Update recommendation engine
    recommendation_engine.lists.append({
        'id': new_list.id,
        'description': new_list.description
    })
    
    return jsonify({"message": "List created successfully!", "list_id": new_list.id}), 201

@list_routes.route('/', methods=['GET'])
def get_lists():
    lists = List.query.all()
    return jsonify([{'id': lst.id, 'name': lst.name, 'description': lst.description} for lst in lists]), 200

@list_routes.route('/<int:list_id>', methods=['GET'])
def get_list(list_id):
    list_item = List.query.get(list_id)
    if not list_item:
        return jsonify({"error": "List not found"}), 404
    return jsonify({'id': list_item.id, 'name': list_item.name, 'description': list_item.description}), 200

@list_routes.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    if not data or not data.get('input'):
        return jsonify({"error": "Input is required"}), 400
    
    recommendations = recommendation_engine.recommend(data['input'])
    return jsonify([{'id': lst['id'], 'description': lst['description']} for lst in recommendations]), 200
