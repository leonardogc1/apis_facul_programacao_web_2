from flask import request, current_app

class request_handler:

    def __init__(self, request_obj):
        self.request = request_obj
    
    def get_system(self):
        url = request.path
        url = url.split("/")
        return url[1]
    
    def get_version(self):
        url = request.path
        url = url.split("/")
        return url[2]

    def get_language(self):
        lang = request.accept_language.best_match(current_app.config.get('ACCEPTED_LANGUAGES'))
        return lang
    
    def get_args(self):
        if request.method == 'POST':
            return request.form
        if request.method == 'GET':
            return request.args
        if request.method == 'DELETE':
            return request.form
        if request.method == 'PUT':
            return request.form
        
    def self_url(self):
        return request.url
