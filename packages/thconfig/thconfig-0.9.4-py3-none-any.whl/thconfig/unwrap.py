__all__ = ['FileConfig', 'CouchConfig', 'EtcdConfig', 'HTTPConfig']

from thresult import auto_unwrap

import thconfig.file
import thconfig.http


FileConfig = auto_unwrap(thconfig.file.file_config.FileConfig)
CouchConfig = auto_unwrap(thconfig.http.couch_config.CouchConfig)
EtcdConfig = auto_unwrap(thconfig.http.etcd_config.EtcdConfig)
HTTPConfig = auto_unwrap(thconfig.http.http_config.HTTPConfig)
