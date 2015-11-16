from flask.ext.restplus import fields

class Responses():
    general = {
        'status': fields.String,
        'description': fields.String
    }

    status = {
        'status': fields.String,
        'description': fields.String,
        'agent': fields.String,
        'docker': fields.String,
        'crane': fields.String
    }

    error = {
        'error': fields.String,
        'description': fields.String
    }
