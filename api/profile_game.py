"""
profile_game.py - Game Profile API

Endpoints for the CS Pathway Game profile persistence system.
Authenticated users can store/retrieve their game progress in the
_game_profile JSON column of the users table.

Routes (all require JWT auth):
  GET    /api/profile/game   - Load current user's game profile
  POST   /api/profile/game   - Create game profile (first save)
  PUT    /api/profile/game   - Update game profile (merge)
  DELETE /api/profile/game   - Clear game data (preserves identity)

Data model: users._game_profile (JSON)
{
  "version": "1.0",
  "localId": "local_...",
  "createdAt": "...",
  "updatedAt": "...",
  "lastModified": <timestamp>,
  "identity-forge":    { "preferences": {...}, "progress": {...}, "completedAt": null },
  "wayfinding-world":  { "preferences": {...}, "progress": {...}, "completedAt": null },
  "mission-tooling":   { "progress": {...}, "completedAt": null }
}
"""

from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from api.authorize import token_required
from __init__ import db

profile_game_api = Blueprint('profile_game_api', __name__, url_prefix='/api')
api = Api(profile_game_api)


class ProfileGameAPI:

    class _Game(Resource):

        @token_required()
        def get(self):
            """Load the current user's game profile."""
            user = g.current_user
            if user.game_profile is None:
                return {'message': 'No game profile found'}, 404
            return jsonify(user.game_profile)

        @token_required()
        def post(self):
            """Create a new game profile (first-time save)."""
            user = g.current_user
            body = request.get_json()
            if not body:
                return {'message': 'Request body is required'}, 400

            game_profile = body.get('_game_profile')
            if not game_profile:
                return {'message': '_game_profile field is required'}, 400

            if user.game_profile is not None:
                return {'message': 'Game profile already exists — use PUT to update'}, 409

            user.game_profile = game_profile
            db.session.commit()
            return jsonify(user.game_profile)

        @token_required()
        def put(self):
            """Update (merge) the current user's game profile."""
            user = g.current_user
            body = request.get_json()
            if not body:
                return {'message': 'Request body is required'}, 400

            game_profile = body.get('_game_profile')
            if not game_profile:
                return {'message': '_game_profile field is required'}, 400

            # Timestamp conflict guard: only save if incoming data is newer
            incoming_ts = game_profile.get('lastModified', 0)
            existing_ts = (user.game_profile or {}).get('lastModified', 0)
            if incoming_ts and incoming_ts < existing_ts:
                # Backend already has newer data — return it so client can reconcile
                return jsonify({'stale': True, 'game_profile': user.game_profile}), 409

            if user.game_profile is None:
                # No existing profile — treat as first save
                user.game_profile = game_profile
            else:
                # Deep merge: keep existing keys, overwrite with incoming
                merged = {**user.game_profile, **game_profile}
                # Merge nested level blobs individually to avoid full overwrites
                for level in ('identity-forge', 'wayfinding-world', 'mission-tooling'):
                    if level in game_profile and level in user.game_profile:
                        existing_level = user.game_profile[level]
                        incoming_level = game_profile[level]
                        merged[level] = {
                            **existing_level,
                            **incoming_level,
                            'preferences': {
                                **(existing_level.get('preferences') or {}),
                                **(incoming_level.get('preferences') or {}),
                            },
                            'progress': {
                                **(existing_level.get('progress') or {}),
                                **(incoming_level.get('progress') or {}),
                            },
                        }
                user.game_profile = merged

            # SQLAlchemy needs an explicit flag for JSON mutation
            from sqlalchemy.orm.attributes import flag_modified
            flag_modified(user, '_game_profile')
            db.session.commit()
            return jsonify(user.game_profile)

        @token_required()
        def delete(self):
            """Clear game progress while preserving identity columns."""
            user = g.current_user
            if user.game_profile is None:
                return {'message': 'No game profile to clear'}, 404

            # Preserve metadata (localId, createdAt) for analytics continuity
            existing = user.game_profile
            user.game_profile = {
                'version': '1.0',
                'localId': existing.get('localId'),
                'createdAt': existing.get('createdAt'),
                'updatedAt': None,
                'lastModified': 0,
                'identity-forge': {
                    'preferences': {},
                    'progress': {'identityUnlocked': False, 'avatarSelected': False},
                    'completedAt': None,
                },
                'wayfinding-world': {
                    'preferences': {},
                    'progress': {'worldThemeSelected': False, 'navigationComplete': False},
                    'completedAt': None,
                },
                'mission-tooling': {
                    'progress': {'toolsUnlocked': False},
                    'completedAt': None,
                },
            }
            from sqlalchemy.orm.attributes import flag_modified
            flag_modified(user, '_game_profile')
            db.session.commit()
            return {'message': 'Game profile cleared (identity preserved)'}, 200


# Register resource
api.add_resource(ProfileGameAPI._Game, '/profile/game')
