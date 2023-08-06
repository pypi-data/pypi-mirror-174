import os
import subprocess

from pypers.core.interfaces import db
from pypers.core.interfaces.storage.backup import Backup
from pypers.utils.utils import clean_folder, delete_files
from . import BaseHandler

class IndexHandler(BaseHandler):


    # "files" : {
    #     "st13" : {
    #         "idx" : "000/st13/idx.json",
    #         "latest" : "000/st13/latest.json"
    #     },
    #     ...
    # }
    def process(self, data_file, appnum):
        from pprint import pprint
        #pprint(data_file)
        if not len(data_file.get('doc', None)):
            return
        record = data_file.get('doc', {})
        st13 = data_file.get('st13', None)

        # index the files
        failed_log = os.path.join(os.path.dirname(record['idx']), 'failed.index')
        jar_file = os.environ.get('INDEXER_JAR').strip()

        # write fofn file
        fofn_file = os.path.join(os.path.dirname(record['idx']), 'findex.fofn')

        with open(fofn_file, 'w') as f:
            f.write(record['idx'])
        cmd = 'java -jar %s --fofn %s --logFile %s --collection %s --type %s --extension .json'
        cmd = cmd % (jar_file,
                     fofn_file,
                     failed_log,
                     self.collection,
                     self.pipeline_type)

        proc = subprocess.Popen(cmd.split(' '),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                close_fds=True)
        stdout, stderr = proc.communicate()

        rc = proc.returncode
        if rc != 0:
            self.logger.error(str(stderr))
            db.get_db_error().send_error(self.run_id,
                                         self.collection,
                                         {'source': 'indexer'},
                                         str(stderr))
            return
        print(failed_log)
        if os.path.exists(failed_log):
           self.logger.info("Failed indexing on %s" % st13)
        else:
            self.backup.store_doc_idx(record['idx'], st13, hard=True)

            # publish what has been indexed of latest files



