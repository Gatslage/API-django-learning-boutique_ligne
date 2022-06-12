from urllib import response
import requests


ECOSCORE_GRADE='d'

def call_success_ecoscore(self,method,url):

    def monkey_json():
        return {
        'product':{
            'ecoscore_grade':ECOSCORE_GRADE
        }
    }
    response=requests.Response()
    #maintenant on s'arrange à ce que les sorties soit validé par notre call_extend qui est dans la model de product 
    response.status_code=200
    response.json=monkey_json
    return response