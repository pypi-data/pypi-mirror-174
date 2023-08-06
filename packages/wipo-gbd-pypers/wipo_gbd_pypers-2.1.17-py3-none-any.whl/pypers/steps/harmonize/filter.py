from pypers.steps.base.step_generic import EmptyStep
from .data_handler import GBDFormat
from .img_handler import GBDImage
from .dyncopy_handler import DynCopy
from .dynlive_handler import DynLive
from .analyze_handler import Analyze
from .idx_handler import IdxTransform

from pypers.core.interfaces.storage.backup import Backup
import json
import os


class Filter(EmptyStep):
    """
    Process manifets file files into subdirectories.
    Rename files and logos to appnum
    """
    spec = {
        "version": "2.0",
        "descr": [
            "Returns the directory with the extraction"
        ],
        "args":
        {
            "inputs": [
                {
                    "name": "manifest",
                    "descr": "the manifest list",
                    "iterable": True
                }
            ],
            "outputs": [
                {
                    "name": "gbd_extraction_date",
                    "descr": "the data gbd extracted the archive"
                },
                {
                    "name": "extraction_dir",
                    "descr": "the destination dir of the extraction"
                },
                {
                    "name": "data_files",
                    "descr": "the extracted data organized by appnum"
                },
                {
                    "name": "img_files",
                    "descr": "the extracted data organized by appnum"
                },
                {
                    "name": "media_files",
                    "descr": "the extracted data organized by appnum"
                }
            ]
        }
    }

    # self.manifest ORIFILES_DIR/run_id/type/collection/office_extraction_date/archive_name/manifest.json
    def process(self):
        collection = self.collection.replace('harmonize_', '')
        self.extraction_dir = os.path.dirname(self.manifest)
        self.backup_processor = Backup(self.pipeline_type, collection)

        params = {
            'collection': collection,
            'pipeline_type':self.pipeline_type,
            'extraction_dir': self.extraction_dir,
            'run_id': self.run_id,
            'output_dir': self.output_dir,
            'logger': self.logger,
            'backup_handler': self.backup_processor
        }

        self.processors = [GBDFormat(**params), GBDImage(**params), DynCopy(**params), DynLive(**params), Analyze(**params),
                           IdxTransform(**params)]

        with open(self.manifest, 'r') as f:
            manifest_data = json.load(f)
        data_files = self._filter_missing_files(manifest_data.get('files', {}))
        appnum_files_flat = [(data, appnum) for appnum, data in data_files.items()][0:20]
        idx_paths = []
        for entry in self.worker_parallel(appnum_files_flat, self._process_record):
            if entry:
                idx_paths.append(entry)
        print('\n'.join(idx_paths))
        raise Exception('foobar')





        self.media_files = manifest_data.get('media_files', {})
        
    def _process_record(self, item):
        data_file, appnum = item
        for processor in self.processors:
            getattr(processor, 'process')(data_file, appnum)
        return data_file.get('doc', {}).get('idx', None)

    def postprocess(self):
        self.extraction_dir = [self.extraction_dir]
        self.gbd_extraction_date = [self.gbd_extraction_date]

        self.data_files = [self.data_files]
        self.img_files = [self.img_files]
        self.media_files = [self.media_files]

    def _file_exists(self, file):
        file_path = os.path.join(self.extraction_dir, file)
        return os.path.exists(file_path)

    def _filter_missing_files(self, unfiltered):
        filtered = {}
        for key, item in unfiltered.items():
            item_present = True
            if 'data' in item.keys():
                item_present = item_present and self._file_exists(item['data']['ori'])
            if 'imgs' in item.keys():
                for logo in item['imgs']:
                    if not logo.get('ori', None):
                        continue
                    item_present = item_present and self._file_exists(logo['ori'])
            if item_present:
                filtered[key] = item
        return filtered




