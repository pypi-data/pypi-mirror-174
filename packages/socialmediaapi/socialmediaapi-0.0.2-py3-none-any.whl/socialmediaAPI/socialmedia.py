import requests


class FacbookAPI:
    def __init__(self,accesstoken,pageID):
        self.accesstoken=accesstoken
        self.pageID=pageID
    def post_image(self,imageLINK,message):
        self.imageLINK=imageLINK
        self.message=message
        request=f'https://graph.facebook.com/{self.pageID}/photos?url={self.imageLINK}&message={self.message}&access_token={self.accesstoken}'
        response=requests.post(request)
        print(response.json())


        
