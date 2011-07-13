import os
import logging
import hashlib

import zc.buildout
from zc.recipe.egg import Egg

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.exception import S3ResponseError


# mute the boto logger
logging.getLogger('boto').setLevel(logging.INFO)


class S3Sync(Egg):
    """
    Credit to Alexander Artemenko for code borrowed from his symlink recipe:
    https://github.com/svetlyak40wt/svetlyak40wt.recipe.symlinks
    """

    def __init__(self, buildout, name, options):
        self.logger = logging.getLogger(name)
        
        super(S3Sync, self).__init__(buildout, name, options)
        
        self.aws_access_key_id = self.options['aws_access_key_id']
        self.aws_secret_access_key = self.options['aws_secret_access_key']
        self.aws_bucket_name = self.options['aws_bucket_name']
        self.aws_bucket_location = self.options['aws_bucket_location']
        self.aws_bucket_root_path = self.options['aws_bucket_root_path']


    def install(self):
        self._sync_files()
        # we don't want buildout to delete files on s3, so return an empty list
        return []


    def update(self):
        self._sync_files()


    def _get_resource_filename(self, uri):
        self.logger.info('getting resource filename for uri "%s"' % uri)

        package, path = uri.split('://', 1)

        self.options['eggs'] = package
        ws = self.working_set()[1]
        distributions = ws.require(package)

        if not distributions:
            raise RuntimeError('Can\'t find package "%"' % package)

        package = distributions[0]

        result = os.path.join(package.location, path)
        self.logger.info('resource filename for uri "%s" is "%s"' % (uri, result))
        return result


    def _sync_files(self):
        # set up an s3 connector
        conn = S3Connection(self.aws_access_key_id, self.aws_secret_access_key)
        
        # get a reference to the bucket, create it if it does not exist
        try:
            bucket = conn.get_bucket(self.aws_bucket_name, validate=True)
        except S3ResponseError, e:
            if e.code == "NoSuchBucket":
                bucket = conn.create_bucket(self.aws_bucket_name, location=self.aws_bucket_location)
            else:
                raise
        
        # iterate through the paths and upload each
        for path in [path for path in self.options['paths'].split('\n') if path]:
            parts = path.split(None, 1)
            if len(parts) == 2:
                source, dest = parts
            else:
                source = parts[0]
                dest = os.path.basename(path)

            if '://' in source:
                source = self._get_resource_filename(source)

            # traverse the path and sync each file
            for dirname, dirnames, filenames in os.walk(source):
                for filename in filenames:
                    # get the fqn of the local file
                    local_fqn = os.path.join(dirname, filename)
                    
                    # construct the s3 key name
                    remote_fqn = os.path.join(self.aws_bucket_root_path, dirname.replace(source, dest), filename)
                    
                    # check if the key exists
                    key = bucket.get_key(remote_fqn)
                    if key:
                        # determine if we need to upload the file
                        md5 = hashlib.md5(file(local_fqn).read())
                        if md5.hexdigest() == key.etag.strip('"'):
                            self.logger.info('skipped: %s' % local_fqn)
                            continue
                        else:
                            self.logger.info('files differ: %s' % (local_fqn,))
                    
                    # create the new key and set contents from file
                    key = Key(bucket)
                    key.key = remote_fqn
                    key.set_contents_from_filename(local_fqn)
                    self.logger.info('uploaded %s to %s:%s' % (local_fqn, self.aws_bucket_name, key.key))

