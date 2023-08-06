import json
import requests 

from tabulate import tabulate 


__all__ = ["Dione"]

class Dione:
    def __init__(self, callisto=None, org=None):
        self.callisto = callisto
        self.org = org

    def create_experiment(self, experiment):
        assert self.org, "No org slug passed"
        assert "projectId" in experiment, "No projectId given"
        assert experiment["projectId"], "No projectId given"
        assert "exportId" in experiment, "No exportId given"
        assert experiment["exportId"], "No exportId given"

        url = f'{self.callisto.host}/dione/api/v1/experiments?orgId={self.org}'
        response = requests.post(url=url, data=json.dumps(experiment), 
                                 headers=self.callisto.headers)

        if response.status_code == 200:
            experiment_id = response.json()["experiment"]["id"]
            return experiment_id
        else:
            print (response.json())
            print ("Failed to create experiment")
            return None

    def add_best_model(self, experimentId, model_path):
        assert self.org, "No org slug passed"
        url = f'{self.callisto.host}/dione/api/v1/experiments/{experimentId}?orgId={self.org}'
        data = json.dumps({ "bestModel": model_path})
        response = requests.put(
                                url=url,
                                data=data,
                                headers=self.callisto.headers
                                )  
        if response.status_code == 200:
            print ("Experiment updated with best model path")
        else:
            print ("Failed to update experiment with best model path!")

    def experiment_done(self, experimentId):
        assert self.org, "No org slug passed"
        url = f'{self.callisto.host}/dione/api/v1/experiments/{experimentId}?orgId={self.org}'
        response = requests.put(
                                url=url,
                                data=json.dumps({ "status": "success"}),
                                headers=self.callisto.headers
                                )  
        if response.status_code != 200:
            print ("Failed to update experiment status")

    def get_experiments(self, projectId):
        assert self.org, "No org slug passed"
        assert projectId, "No projectId given"

        get_experiment_url = f'{self.callisto.host}/dione/api/v1/experiments?orgId={self.org}&projectId={projectId}'
        response = requests.get(get_experiment_url, headers=self.callisto.headers)

        if response.status_code == 200:
            experiments = response.json()['results']
            headers = ["ID", "ExportId", "Name", "Tags", "Status"]
            table = [[experiment["id"], experiment["exportId"],
                    experiment["name"], ','.join(experiment["tags"]), 
                    experiment["status"]] for experiment in experiments]

            print(f'\nList of experiments for GeoEngine project {projectId}:\n')
            print(tabulate(table, headers=headers, tablefmt='pretty'))
            print()
        else:
            print(f'All experiments for GeoEngine project {projectId} cannot be retrieved')
            print(f'Experiments endpoint {get_experiment_url} returned with HTTP status code : {response.status_code}\n')


    def create_artifact(self, artifact):
        assert self.org, "No org slug passed"
        assert artifact, "No artifact passed"

        url = f'{self.callisto.host}/dione/api/v1/artifacts?orgId={self.org}'

        response = requests.post(url=url, data=json.dumps(artifact), 
                                headers=self.callisto.headers)

        if response.status_code == 200:
            artifact_id = response.json()["artifact"]["id"]
            return artifact_id
        else:
            print ("Failed to create artifact")
            return None