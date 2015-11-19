#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import settings
from settings import GENERAL_DEBUG

from flask import Flask, request
from flask.ext.restplus import Api, apidoc, Resource, reqparse, fields
from werkzeug.datastructures import FileStorage

from models import Responses
from tools import initializator

from controllers import Installator, Check, Deploy, ControllerError

app = Flask(__name__)
api = Api(app, version='1', title='comcloud-node-agent',
    description='An unified API to all Docker operations.',)

## Response models
generalResponseModel = api.model('General', Responses.error)
statusResponseModel = api.model('Status', Responses.error)
errorResponseModel = api.model('Error', Responses.error)

# Common

def not_implemented():
    result = {'error':'not_implemented', 'description':'Feature not implemented yet'}
    return result, 500

def not_found():
    result = {'error':'not_found', 'description':'Resource not found'}
    return result, 404

def process_error(text):
    result = {'error':'process_error', 'description':'Error while processing request.'}
    if GENERAL_DEBUG:
        result['description'] = result['description']+' '+text
    return result, 500

def controller_error(text):
    result = {'error':'controller_error', 'description':text}
    return result, 400

def not_started():
    result = {'error':'not_started', 'description':'The process has not stated yet.'}
    return result, 400

# Install

install_ns = api.namespace('install', description='Install operations.')

@install_ns.route('/docker')
class DockerInst(Resource):
    @api.doc(description='Install docker daemon')
    @api.response(500, 'Error processing the request', errorResponseModel)
    @api.response(200, 'OK', generalResponseModel)
    def get(self):
        try:
            return Installator.docker()
        except ControllerError as e:
            return controller_error(e.message)
        except Exception as e:
            return process_error(str(e))

@install_ns.route('/crane')
class CraneInst(Resource):
    @api.doc(description='Install docker-crane')
    @api.response(500, 'Error processing the request', errorResponseModel)
    @api.response(200, 'OK', generalResponseModel)
    def get(self):
        try:
            return Installator.crane()
        except ControllerError as e:
            return controller_error(e.message)
        except Exception as e:
            return process_error(str(e))

# Deploy

deployArgs = api.parser()
deployArgs.add_argument('package', type=FileStorage, help='Package to be deployed' , location='files')

deploy_ns = api.namespace('deploy', description='Deploy packages.')

@deploy_ns.route('/')
class DeployService(Resource):
    @api.doc(description='Deploy service', parser=deployArgs)
    @api.response(500, 'Error processing the request', errorResponseModel)
    @api.response(200, 'OK', generalResponseModel)
    def post(self):
        try:
            return Deploy.new(request.files['package'])
        except ControllerError as e:
            return controller_error(e.message)
        except Exception as e:
            return process_error(str(e))


# Status

status_ns = api.namespace('status', description='Check the status.')

@status_ns.route('/')
class GeneralStatus(Resource):
    @api.doc(description='Deployment status')
    @api.response(500, 'Error processing the request', errorResponseModel)
    @api.response(200, 'OK', statusResponseModel)
    def get(self):
        try:
            return Check.general()
        except Exception as e:
            return str(e)
            return not_started()

@status_ns.route('/docker')
class DockerStatus(Resource):
    @api.doc(description='Docker installation status')
    @api.response(500, 'Error processing the request', errorResponseModel)
    @api.response(200, 'OK', generalResponseModel)
    def get(self):
        try:
            return Check.docker()
        except Exception as e:
            return not_started()

@status_ns.route('/crane')
class CraneStatus(Resource):
    @api.doc(description='Crane installation status')
    @api.response(500, 'Error processing the request', errorResponseModel)
    @api.response(200, 'OK', generalResponseModel)
    def get(self):
        try:
            return Check.crane()
        except Exception as e:
            return not_started()

@status_ns.route('/deploy')
class DeployStatus(Resource):
    @api.doc(description='Deploy status')
    @api.response(500, 'Error processing the request', errorResponseModel)
    @api.response(200, 'OK', generalResponseModel)
    def get(self):
        try:
            return Check.deploy()
        except Exception as e:
            return not_started()

if __name__ == '__main__':
    initializator()
    app.run(host=settings.WS_BIND_IP, port=settings.WS_BIND_PORT, debug=GENERAL_DEBUG)
