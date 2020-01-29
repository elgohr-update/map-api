from flask import request
from flask_restful import Resource
import requests
from werkzeug.exceptions import BadRequest, NotFound

from map.couch import CouchPatientDB
from map.fhir import HapiRequest, ResourceType


class Sync(Resource):
    """Trigger sync between HAPI and Couch stores
    """

    def get(self, resource_type):
        ResourceType.validate(resource_type)
        if resource_type != 'Patient':
            raise BadRequest("Only syncing Patient resources at this time")
        params = {'_pretty': 'true', '_format': 'json'}
        params.update(request.args)
        hapi_pat = requests.get(HapiRequest.build_request(
            resource_type),
            params=params)

        # Search returns bundle - if one was found, extract and sync
        hapi_pat.raise_for_status()
        bundle = hapi_pat.json()
        assert bundle.get('resourceType') == 'Bundle'
        if bundle.get('total') == 1:
            patient_fhir = bundle['entry'][0]['resource']
            return CouchPatientDB(patient_fhir).patient_fhir
        else:
            raise NotFound()
