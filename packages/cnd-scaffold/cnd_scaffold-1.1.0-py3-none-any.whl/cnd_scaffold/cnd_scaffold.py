import yamale
import yaml
import json


class CndScaffold:
    step = {'init', 'build', 'runtime'}

    def __init__(self, source, target, data_to_replace, cnd_io, print):
        self._print = print
        self._source = source
        self._target = target
        self._cnd_io = cnd_io
        self._data_to_replace = data_to_replace

    def _load_schema(self):
        self.schema = self._cnd_io.pull_file(self._source['project_id'], 'schema.yml', branch=self._source['branch'])
        if self.schema is False:
            self._print.info_e(f"Cannot found file for schema : {self.schema}")
            raise NameError('Schema unreadable')
        return self.schema

    def _load_structure(self):
        self.structure = self._cnd_io.pull_file(self._source['project_id'], f'{self._source["definition"]}.yml', branch=self._source['branch'])
        if self.structure is False:
            self._print.info_e(f"Cannot found file for structure : {self.structure}")
            raise NameError('Structure unreadable')
        return self.structure
            

    def _validate_structure(self):
        self._load_schema()
        self._load_structure()
        schema = yamale.make_schema(content=self.schema)
        data = yamale.make_data(content=self.structure)
        yamale.validate(schema, data)
        content_yaml = yaml.safe_load(self.structure)
        self.yaml_structure = {'source_folder': content_yaml['source_folder']}
        for item in content_yaml['files']:
            for step in item['step']:
                if step not in self.yaml_structure:
                    self.yaml_structure[step] = []
                if 'step' in item:
                    del item['step']
                self.yaml_structure[step].append(item)
        return self.yaml_structure

    def _load_files(self, step):
        self.file_to_upload = []
        for item in self.yaml_structure[step]:
            repeat = {'values': [''], 'key': ''}
            target = item['name']
            content = self._cnd_io.pull_file(self._source['project_id'], f'{self.yaml_structure["source_folder"]}/{item["name"]}', branch=self._source['branch'])
            if content is False:
                self._print.info_e(f'Cannot found file for : {self._source["project_id"]} - {self.yaml_structure["source_folder"]}/{item["name"]}')
                raise NameError(f'File unreadable {self.yaml_structure["source_folder"]}/{item["name"]}')
            if 'target' in item:
                target = item['target']
            if 'repeat' in item:
                repeat = {'key': item['repeat'], 'values': self._data_to_replace[item['repeat']]}
            for value in repeat['values']:
                self._cnd_io.commit_file(
                    self._target['project_id'],
                    f"{self._target['folder']}/{self._replace_content(target, {repeat['key']: value})}",
                    self._replace_content(content, {repeat['key']: value}),
                    self._target['branch']
                )
        return len(self._cnd_io._files[self._target['project_id']][self._target['branch']])

    def _replace_content(self, content, local_var={}):
        for item in local_var:
            # content = content.replace(f"%{str_to_replace}%", local_var[item][key])
            if isinstance(local_var[item], dict) is True:
                for key in local_var[item]:
                    str_to_replace = f'{item}.{key}'
                    content = content.replace(f"%{str_to_replace}%", local_var[item][key])
            else:
                content = content.replace(f"%{item}%", local_var[item])
        for item in self._data_to_replace:
            if isinstance(self._data_to_replace[item], dict) is True or isinstance(self._data_to_replace[item], list) is True:
                content = content.replace(f"%{item}%", json.dumps(self._data_to_replace[item]))
            else:
                content = content.replace(f"%{item}%", self._data_to_replace[item])
        return content

    def _push_files(self):
        result = self._cnd_io.push_files(self._target['project_id'], commit_message="Pushing from CndScaffold", branch=self._target["branch"])
        if result is False:
            self._print.info_e(f'Cannot push content')
            self._print.trace_e(f'Content: {yaml.dump(self._cnd_io._files)}')
            raise NameError(f'Content cannot be pushed')
        return True
        
    def _apply_step(self, step):
        self._validate_structure()
        self._load_files(step)
        return self._push_files()
        
    def init(self):
        return self._apply_step('init')
            
    def build(self):
        return self._apply_step('build')
                
    def runtime(self):
        return self._apply_step('init')
