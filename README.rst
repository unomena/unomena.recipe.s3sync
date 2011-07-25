A buildout recipe that syncs static media with AWS S3.

Based loosely on Alexander Artemenko's symlink recipe at https://github.com/svetlyak40wt/svetlyak40wt.recipe.symlinks

New or changed local files are uploaded to s3.  Files are never removed from s3.

All files created or updated on s3 have permissions set to 'public-read' by default.  This can be changed using the buidout option "default_acl".

Files already existing on s3 are md5-ed and the hash compared to the hash reported by s3.  Only changed files are uploaded.

By default, permissions are only set on s3 when creating or updating files.  To also set permissions for skipped files, set the buildout option "set_acl_on_skip" to True.


Sample config:

::
    
    [buildout]
        ...
        find-links = http://github.com/unomena/unomena.recipe.s3sync/tarball/0.0.3#egg=unomena.recipe.s3sync-0.0.3
    
    [sync-static]
    recipe = unomena.recipe.s3sync
    aws_bucket_name = my.bucket.name
    aws_bucket_location = EU
    aws_bucket_root_path = static
    aws_access_key_id = ${buildout:aws-access-key-id}
    aws_secret_access_key = ${buildout:aws-secret-access-key}
    paths = ${buildout:parts-directory}/django/django/contrib/admin/media admin
            ${buildout:directory}/src/${buildout:app-name}/static/${buildout:app-name}
            django-ckeditor://ckeditor/media/ckeditor
    

