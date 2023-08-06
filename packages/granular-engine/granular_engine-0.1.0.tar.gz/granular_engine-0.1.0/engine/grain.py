import os
import yaml
from datetime import datetime

from engine.connections import Callisto, Europa, Dione


__all__ = ["Engine"]

class Engine():
    def __init__(self, yaml_file=None):
        assert yaml_file, "Please pass a configuration YAML file for this project"
        fp = open(yaml_file, 'r')
        meta = dict(yaml.safe_load(fp.read()))
        assert "org" in meta, "Please provide organization slug"
        assert "projectId" in meta, "No GeoEngine projectId passed"
        assert "exportId" in meta, f"No exportId for GeoEngine project {meta['projectId']} passed"

        self.callisto = Callisto()
        self.org_id = self.callisto.get_org_id_from_slug(org_slug=meta['org'])
        self.europa = Europa(self.callisto, self.org_id)
        project = self.europa.get_project_details(id=meta['projectId'], verbose=False)
        assert "bucketPath" in project, "No bucketPath in the project"

        self.version = f"{meta['name'].replace(' ', '_')}-{datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S')}"

        meta['experimentUrl'] = f"{project['bucketPath']}/experiments/{self.version}"

        self.meta = meta

        if 'logsDir' not in meta:
            meta['logsDir'] = 'logs'
        elif meta['logsDir'] == '':
            meta['logsDir'] = 'logs'
        if 'weightsDir' not in meta:
            meta['weightsDir'] = 'weights'
        elif meta['weightsDir'] == '':
            meta['weightsDir'] = 'weights'

        if not os.path.exists(meta['logsDir']):
            os.makedirs(meta['logsDir'])
        if not os.path.exists(meta['weightsDir']):
            os.makedirs(meta['weightsDir'])

        proper_meta = {}
        proper = ['metaInfo', 'name', 'description', 'tags', 
                  'exportId', 'projectId', 'gitUrl', 
                  'framework', 'params', 'inputs',
                  'outputs', 'experimentUrl', 'readme']
        for k in meta.keys():
            if k in proper:
                proper_meta[k] = meta[k] or ''

        # Register the experiment on dione
        self.dione = Dione(self.callisto, self.org_id)
        self.experimentId = self.dione.create_experiment(proper_meta)

    def log(self, step, best=False, checkpoint_path=None, **kwargs):
        artifact = {"experimentId": self.experimentId,
                    "metadata": kwargs,
                    "step": step}
        if checkpoint_path:
            dst_state_path = f"{self.meta['experimentUrl']}/weights/"
            os.system(f"gsutil cp {checkpoint_path} {dst_state_path} 2> /dev/null")
            artifact["metadata"]["checkpoint"] = f"{dst_state_path}/{checkpoint_path.split('/')[-1]}"
            
            if best:
                self.dione.add_best_model(self.experimentId, artifact["metadata"]["checkpoint"])


        # Register the artifact on dione 
        artifact_id = self.dione.create_artifact(artifact)

    def done(self):
        self.dione.experiment_done(self.experimentId)