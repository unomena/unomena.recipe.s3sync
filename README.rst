A buildout recipe that syncs static media with AWS S3.

Based loosely on Alexander Artemenko's symlink recipe at https://github.com/svetlyak40wt/svetlyak40wt.recipe.symlinks

Sample config:

::
    
    [buildout]
        ...
        find-links = http://github.com/unomena/unomena.recipe.s3sync/tarball/0.0.1#egg=unomena.recipe.s3sync-0.0.1
    
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
    

