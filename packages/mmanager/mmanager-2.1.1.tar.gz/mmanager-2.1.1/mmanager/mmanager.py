import os
import json
import requests
import traceback
from .dataresource import *
from .serverequest import *
from .log_keeper import *

class ModelManager:
    def  __init__(self, secret_key, base_url):
        self.base_url = base_url
        self.project_data = {}
        self.secret_key = secret_key
    
    def _get_headers(self, **kwargs):
        '''Returns headers for request
        '''
        headers = {'Authorization': 'secret-key {0}'.format(self.secret_key)}

        return headers

class Usecase(ModelManager):

    def create_response(self, resp):
        json_data = resp
        output_response = {
            "ID": json_data.get("id", None),
            "Type": json_data.get("usecase_type", None),
            "Name": json_data.get("name", None),
            "Description": json_data.get("description", None),
            "link": "%s/analytic/usecase/%s/detail/"%(self.base_url,json_data.get("id", None))
        }
        return output_response
  
    def post_usecase(self, usecase_data):
        '''Post Usecase
        '''
        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/projects/" % self.base_url
        
        image_p = usecase_data.get('image', None)
        banner_p = usecase_data.get('banner', None)
        
        #for usecase_data
        data = {
            "name": usecase_data['name'],
            "author": usecase_data['author'],
            "description": usecase_data['description'],
            "source": usecase_data['source'],
            "contributor": usecase_data['contributor'],  
            "transparency": usecase_data['transparency'],
            "usecase_type": usecase_data['usecase_type'],
        }

        #for images
        if image_p and banner_p:
            files={
                "image":open(image_p, 'rb'),
                "banner":open(banner_p, 'rb')
            }
        elif image_p:
            files={
                "image":open(image_p, 'rb'),
            }
        else:
            files = {}
    
        try:
            usecase = requests.post(url,
                    data=data, files=files, headers=kwargs['headers'])
        except Exception as e:
            logger.error(str(e))

        if usecase.status_code == 201:
            logger.info("Post usecase succeed with status code %s" % usecase.status_code)
        else:
            logger.error("Post usecase failed with status code %s" % usecase.status_code)
            if usecase.json()['name'][0]:
                logger.error(usecase.json()['name'][0])
            
        return usecase

    def patch_usecase(self, usecase_data, usecase_id):
        '''Update Usecase
        '''

        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/projects/%s/" % (self.base_url, usecase_id)
        image_p = usecase_data['image']
        banner_p = usecase_data['banner']
        
        #for usecase_data
        data = {
            # "name": usecase_data['name'],
            "author": usecase_data['author'],
            "description": usecase_data['description'],
            "source": usecase_data['source'],
            "contributor": usecase_data['contributor'],  
        }

        #for images
        files={
             "image":open(image_p, 'rb'),
             "banner":open(banner_p, 'rb')
        }
        try:
            usecase = requests.patch(url,
                    data=data, files=files, headers=kwargs['headers'])
        except Exception as e:
            logger.error(str(e))

        if usecase.status_code == 200:
            logger.info("Update usecase succeed with status code %s" % r.status_code)
        else:
            logger.error("Update usecase failed with status code %s" % usecase.status_code)
            if usecase.json()['name'][0]:
                logger.error(usecase.json()['name'][0])

        return usecase

    def delete_usecase(self, usecase_id):
        '''Delete Usecase
        '''

        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/projects/%s/" % (self.base_url, usecase_id)
        
        try:
            usecase = requests.delete(url, headers=kwargs['headers'])
        except Exception as e:
            logger.error(str(e))

        if usecase.status_code == 204:
            print("Delete usecase succeed with status code %s" % r.status_code)
        else:
            print("Delete usecase failed with status code %s" % r.status_code)
            if usecase.json()['name'][0]:
                logger.error(usecase.json()['name'][0])
            
        return self

    def get_usecases(self):

        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/projects/get_usecases/" % self.base_url
        try:
            usecases = requests.get(url, headers=kwargs['headers'])
        except Exception as e:
            logger.error(str(e))
        return usecases.json()
    
    def get_detail(self, usecase_id):

        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/projects/%s/" % (self.base_url, usecase_id)
        try:
            usecases = requests.get(url, headers=kwargs['headers'])
        except Exception as e:
            logger.error(str(e))

        return usecases.json()

    def get_models(self, usecase_id):

        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/projects/getmodels/?usecase_id=%s" % (self.base_url, usecase_id)

        try:
            usecases = requests.get(url, headers=kwargs['headers'])
        except Exception as e:
            logger.error(str(e))
        return usecases.json()
            
class Model(ModelManager):

    def post_model(self, model_data, ml_options={}):
        '''Post Model
        '''
        url = "%s/api/models/" % self.base_url

        kwargs = {
            'headers': self._get_headers()
        }

        #for model_data
        model_data.update(ml_options)
        data = get_model_data(model_data)

        #for model_files
        files = get_files(model_data)

        try:
            model = model_request(url, kwargs, data, ml_options, files)
        except Exception as e:
            logger.error(str(e))

        if model.status_code == 201:
            logger.info("Model creation succeed with status code %s" % model.status_code)
        else:
            logger.error("Model creation failed with status code %s" % (model.status_code))
            if model.json()['name'][0]:
                logger.error(model.json()['name'][0])
        
        return model
    
    def delete_model(self, model_id):

        '''Delete Model
        '''

        kwargs = {
            'headers': self._get_headers()
        }
        
        url = "%s/api/models/%s/" % (self.base_url, model_id)
        
        try:
            model = requests.delete(url, headers=kwargs['headers'])
        except Exception as e:
            logger.error(str(e))

        if model.status_code == 204:
            logger.info("Delete model succeed with status code %s" % model.status_code)
        else:
            logger.error("Delete model failed with status code %s" % model.status_code)
            if model.json()['name'][0]:
                logger.error(model.json()['name'][0])
            
        return self

    def patch_model(self, model_data, model_id):

        '''Update Model
        '''

        url = "%s/api/models/%s/" % (self.base_url, model_id)

        kwargs = {
            'headers': self._get_headers()
        }

        #for model_data
        data = {
            "transformerType": model_data['transformerType'],
            "target_column": model_data['target_column'],
            "note": model_data['note'],
            "model_area": model_data.get('model_area', None),
            "model_dependencies": model_data.get('model_dependencies', None),
            "model_usage": model_data.get('model_usage', None),
            "model_adjustments": model_data.get('model_adjustments', None),
            "model_developer": model_data.get('model_developer', None),
            "model_approver": model_data.get('model_approver', None),
            "model_maintenance": model_data.get('model_maintenance', None),
            "documentation_code": model_data.get('documentation_code', None),
            "implementation_plateform": model_data.get('implementation_plateform', None),
            "production": model_data.get('production', None),
        }

        model_file_path = model_data['model_file_path']
        scoring_file_path = model_data['scoring_file_path']
        training_dataset = model_data['training_dataset']
        pred_dataset = model_data['pred_dataset']
        actual_dataset = model_data['actual_dataset']
        test_dataset = model_data['test_dataset']

        files={
                "training_dataset": open(training_dataset, 'rb'),
                "test_dataset": open(test_dataset, 'rb'),
                "pred_dataset": open(pred_dataset, 'rb'),
                "actual_dataset": open(actual_dataset, 'rb'),
                "model_file_path": open(model_file_path, 'rb'),
                "scoring_file_path": open(scoring_file_path, 'rb'),
                }

        try:
            model = requests.patch(url,
                        data=data, files=files, headers=kwargs['headers'])
        except Exception as e:
            logger.error(str(e))

        if model.status_code == 200:
            logger.info("Update model succeed with status code %s" % model.status_code)
        else:
            logger.error("Update model failed with status code %s" % model.status_code)
            if model.json()['name'][0]:
                logger.error(model.json()['name'][0])

        return model

    def generate_report(self, model_id):
        '''Generate Model Report
        '''

        kwargs = {
            'headers': self._get_headers()
        }


        url = "%s/api/govrnreport/%s/generateReport/" % (self.base_url, model_id)

        try:
            model = requests.post(url, headers=kwargs['headers'])
        except Exception as e:
            logger.error(str(e))

        if model.status_code == 201:
            logger.info("Report Generation succeed with status code %s" % model.status_code)
        else:
            logger.error("Report Generation failed with status code %s" % model.status_code)
            if model.json()['name'][0]:
                logger.error(model.json()['name'][0])

        return model

    def get_details(self, model_id):
        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/models/%s/" % (self.base_url, model_id)
        try:
            model = requests.get(url, headers=kwargs['headers'])
        except Exception as e:
            logger.error(str(e))

        return model.json()
    
    def get_latest_metrics(self, model_id, metric_type):
        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/models/get_latest_metrics/?model_id=%s&&metric_type=%s" % (self.base_url, model_id, metric_type)
        try:
            model = requests.get(url, headers=kwargs['headers'])
        except Exception as e:
            logger.error(str(e))

        return model.json()

    def get_all_reports(self, model_id):
        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/models/get_all_reports/?model_id=%s" % (self.base_url, model_id)
        try:
            model = requests.get(url, headers=kwargs['headers'])
        except Exception as e:
            logger.error(str(e))

        return model.json()