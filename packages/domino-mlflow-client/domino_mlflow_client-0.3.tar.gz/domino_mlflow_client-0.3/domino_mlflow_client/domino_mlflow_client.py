import jwt
import os

class DominoMLFlowClient:
    def init(mlflow_tracking_uri=None,
            domino_api_key=None,
            domino_project_name=None,
            domino_run_id=None,
            tags={}):
        if(mlflow_tracking_uri is not None):
            os.environ['MLFLOW_TRACKING_URI']=mlflow_tracking_uri
        if(domino_api_key is None):
            domino_api_key=os.environ.get('DOMINO_USER_API_KEY')
        if(domino_project_name is None):
            domino_project_name=os.environ.get('DOMINO_PROJECT_NAME')
        if(domino_run_id is None):
            domino_run_id=os.environ.get('DOMINO_RUN_ID')
        domino_json={"domino_api_key": domino_api_key,"domino_project_name":domino_project_name,
                                "domino_run_id":domino_run_id,"tags":tags}

        encoded_jwt = jwt.encode(domino_json,
                                "secret", algorithm="HS256")
        os.environ['MLFLOW_TRACKING_TOKEN']=encoded_jwt
        return encoded_jwt

    def update_tags(self,tags={}):
        domino_attributes = self.decode_jwt(os.environ['MLFLOW_TRACKING_TOKEN'])
        return self.init(domino_attributes['domino_api_key'],
                    domino_attributes['domino_project_name'],
                    domino_attributes['domino_run_id'],tags)


    def decode_jwt(encoded_jwt=None):
        return jwt.decode(encoded_jwt.encode(), "secret", algorithms=["HS256"])


# Testings
if __name__ == "__main__":
    from domino_mlflow_client import DominoMLFlowClient as dmc
    domino_api_key = "1"
    domino_project_name = "2"
    domino_runid = "3"
    domino_project_id = "4"
    key = dmc.init(
        "x",
        domino_api_key,
        domino_project_name,
        domino_runid,
        tags={"a": "b"},
    )
    print("---")
    print(key)
    print("---")
    print(dmc.decode_jwt(key))



