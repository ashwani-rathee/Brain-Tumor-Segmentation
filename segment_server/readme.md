This is the brain tumor segmentation rest api flask server that is supposed to be deployed on heroku or gcp.

There is only essential endpoint that's is `/predict` that is supposed to be used to predict the segmentation of the brain tumor. Predict works on two end points:

- https://brain-segment-api.herokuapp.com/predict
- https://brain-tumor-segment-api.as.r.appspot.com/predict


#### Local run:

```
cd segment_server
pip install -r requirements.txt
FLASK_ENV=development FLASK_APP=app.py flask run
```

That would hopefully output something like below:
```
(base) ashwani@user:~/annotater/segment_server$ FLASK_ENV=development FLASK_APP=app.py flask run
 * Serving Flask app "app.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with inotify reloader
 * Debugger is active!
 * Debugger PIN: 671-247-288
```
This means that the server is running on localhost:5000 and is ready to take up request on point `/predict`

Server run can be tested by used request_test.py script.
```
python request_test.py
```

which will hopefully return 
```
(py36) ashwani@user:~/annotater/segment_server$ python request_test.py
[[False False False ... False False False]
 [False False False ... False False False]
 [False False False ... False False False]
 ...
 [False False False ... False False False]
 [False False False ... False False False]
 [False False False ... False False False]]
```


#### Heroku deployement:

The following setups should help when you deplyoying server on herok, I have made changes in order to make the model run on cpu and with only 512 mb of ram.
```
heroku login
heroku create brain-segment-api
heroku git:remote -a brain-segment-api
git init
git add . 
git commit -m "Initial commit"
git push heroku master
```
After it's all said and done,build log will log like this:
```
-----> Building on the Heroku-20 stack
-----> Using buildpack: heroku/python
-----> Python app detected
-----> No Python version was specified. Using the same version as the last build: python-3.9.7
       To use a different version, see: https://devcenter.heroku.com/articles/python-runtimes
-----> No change in requirements detected, installing from cache
-----> Using cached install of python-3.9.7
-----> Installing pip 20.2.4, setuptools 47.1.1 and wheel 0.36.2
-----> Installing SQLite3
-----> Installing requirements with pip
       Looking in links: https://download.pytorch.org/whl/torch_stable.html
-----> Discovering process types
       Procfile declares types -> web
-----> Compressing...
       Done: 256.1M
-----> Launching...
       Released v5
       https://brain-segment-api.herokuapp.com/ deployed to Heroku

```

and `heroku logs --tail -a brain-segment-api` will look something like this:
```
2021-10-16T08:25:20.409519+00:00 heroku[web.1]: Unidling
2021-10-16T08:25:20.729795+00:00 heroku[web.1]: State changed from down to starting
2021-10-16T08:25:32.690977+00:00 heroku[web.1]: Starting process with command `gunicorn app:app`
2021-10-16T08:25:33.719029+00:00 app[web.1]: [2021-10-16 08:25:33 +0000] [4] [INFO] Starting gunicorn 20.1.0
2021-10-16T08:25:33.720943+00:00 app[web.1]: [2021-10-16 08:25:33 +0000] [4] [INFO] Listening at: http://0.0.0.0:49245 (4)
2021-10-16T08:25:33.720986+00:00 app[web.1]: [2021-10-16 08:25:33 +0000] [4] [INFO] Using worker: sync
2021-10-16T08:25:33.724123+00:00 app[web.1]: [2021-10-16 08:25:33 +0000] [7] [INFO] Booting worker with pid: 7
2021-10-16T08:25:33.809586+00:00 app[web.1]: [2021-10-16 08:25:33 +0000] [8] [INFO] Booting worker with pid: 8
2021-10-16T08:25:34.343649+00:00 heroku[web.1]: State changed from starting to up
2021-10-16T08:25:44.675249+00:00 app[web.1]: /app/.heroku/python/lib/python3.9/site-packages/torch/nn/functional.py:1709: UserWarning: nn.functional.sigmoid is deprecated. Use torch.sigmoid instead.
2021-10-16T08:25:44.675263+00:00 app[web.1]: warnings.warn("nn.functional.sigmoid is deprecated. Use torch.sigmoid instead.")
2021-10-16T08:25:45.635462+00:00 heroku[router]: at=info method=POST path="/predict" host=brain-segment-api.herokuapp.com request_id=6c0aa03e-d394-4b5a-b7fd-cb1c0f70f742 fwd="49.36.228.88" dyno=web.1 connect=0ms service=8809ms status=200 bytes=1825909 protocol=https
2021-10-16T08:25:45.627361+00:00 app[web.1]: 10.1.63.15 - - [16/Oct/2021:08:25:45 +0000] "POST /predict HTTP/1.1" 200 1825751 "-" "python-requests/2.25.1"

```


#### GCP deployement:

Create a project by name brain-tumor-segment-api and enable app engine+other api use by adding the billiing account(also use those credits by verifying debit card). Then start the cloud shell on top right corner of the project page. Then do the following steps in shell. app.yaml file is essential to the deployement and not Procfile.
```
git clone https://github.com/ashwani-rathee/annotater.git
cd annotater/segment_server
gcloud app deploy
```

Then it will prompt you to add some yes/no options and the whole log will look something like below:
```
ab669522@cloudshell:~/annotater/segment_server (brain-tumor-segment-api)$ gcloud app deploy
Services to deploy:

descriptor:                  [/home/ab669522/annotater/segment_server/app.yaml]
source:                      [/home/ab669522/annotater/segment_server]
target project:              [brain-tumor-segment-api]
target service:              [default]
target version:              [20211016t090551]
target url:                  [https://brain-tumor-segment-api.as.r.appspot.com]
target service account:      [App Engine default service account]


Do you want to continue (Y/n)?  y

Enabling service [appengineflex.googleapis.com] on project [brain-tumor-segment-api]...
Operation "operations/acf.p2-8487703108-0d5e5af3-6686-4533-bd84-65a6b24e0372" finished successfully.
Beginning deployment of service [default]...
Building and pushing image for service [default]
Started cloud build [70e08e85-9894-48f4-a700-1e01d4081ed2].
To see logs in the Cloud Console: https://console.cloud.google.com/cloud-build/builds/70e08e85-9894-48f4-a700-1e01d4081ed2?project=8487703108
---------------------------------------------------------------------------------------------------------- REMOTE BUILD OUTPUT -----------------------------------------------------------------------------------------------------------
starting build "70e08e85-9894-48f4-a700-1e01d4081ed2"

FETCHSOURCE
Fetching storage object: gs://staging.brain-tumor-segment-api.appspot.com/asia.gcr.io/brain-tumor-segment-api/appengine/default.20211016t090551:latest#1634375227536439
Copying gs://staging.brain-tumor-segment-api.appspot.com/asia.gcr.io/brain-tumor-segment-api/appengine/default.20211016t090551:latest#1634375227536439...
- [1 files][  6.9 MiB/  6.9 MiB]
Operation completed over 1 objects/6.9 MiB.
BUILD
Starting Step #0
Step #0: Pulling image: gcr.io/gcp-runtimes/python/gen-dockerfile@sha256:ac444fc620f70ff80c19cde48d18242dbed63056e434f0039bf939433e7464aa
Step #0: gcr.io/gcp-runtimes/python/gen-dockerfile@sha256:ac444fc620f70ff80c19cde48d18242dbed63056e434f0039bf939433e7464aa: Pulling from gcp-runtimes/python/gen-dockerfile
Step #0: Digest: sha256:ac444fc620f70ff80c19cde48d18242dbed63056e434f0039bf939433e7464aa
Step #0: Status: Downloaded newer image for gcr.io/gcp-runtimes/python/gen-dockerfile@sha256:ac444fc620f70ff80c19cde48d18242dbed63056e434f0039bf939433e7464aa
Step #0: gcr.io/gcp-runtimes/python/gen-dockerfile@sha256:ac444fc620f70ff80c19cde48d18242dbed63056e434f0039bf939433e7464aa
Finished Step #0
Starting Step #1
Step #1: Pulling image: gcr.io/cloud-builders/docker@sha256:08c5443ff4f8ba85c2114576bb9167c4de0bf658818aea536d3456e8d0e134cd
Step #1: gcr.io/cloud-builders/docker@sha256:08c5443ff4f8ba85c2114576bb9167c4de0bf658818aea536d3456e8d0e134cd: Pulling from cloud-builders/docker
Step #1: 75f546e73d8b: Already exists
Step #1: 0f3bb76fc390: Already exists
Step #1: 3c2cba919283: Already exists
Step #1: 4d168e97939c: Pulling fs layer
Step #1: 4d168e97939c: Verifying Checksum
Step #1: 4d168e97939c: Download complete
Step #1: 4d168e97939c: Pull complete
Step #1: Digest: sha256:08c5443ff4f8ba85c2114576bb9167c4de0bf658818aea536d3456e8d0e134cd
Step #1: Status: Downloaded newer image for gcr.io/cloud-builders/docker@sha256:08c5443ff4f8ba85c2114576bb9167c4de0bf658818aea536d3456e8d0e134cd
Step #1: gcr.io/cloud-builders/docker@sha256:08c5443ff4f8ba85c2114576bb9167c4de0bf658818aea536d3456e8d0e134cd
Step #1: Sending build context to Docker daemon   7.79MB
Step #1: Step 1/9 : FROM gcr.io/google-appengine/python@sha256:c6480acd38ca4605e0b83f5196ab6fe8a8b59a0288a7b8216c42dbc45b5de8f6
Step #1: gcr.io/google-appengine/python@sha256:c6480acd38ca4605e0b83f5196ab6fe8a8b59a0288a7b8216c42dbc45b5de8f6: Pulling from google-appengine/python
Step #1: 6c5b97b864a6: Already exists
Step #1: 8ca77d5ce166: Pulling fs layer
Step #1: 3c2cba919283: Pulling fs layer
Step #1: ebeccf37c57f: Pulling fs layer
Step #1: 42ebf62db3f5: Pulling fs layer
Step #1: c0c3f74f3f7c: Pulling fs layer
Step #1: 6d5fad3b20f0: Pulling fs layer
Step #1: 906c5911ea69: Pulling fs layer
Step #1: 3c18b1c18dfc: Pulling fs layer
Step #1: 0360f916794e: Pulling fs layer
Step #1: e90908c49002: Pulling fs layer
Step #1: 392df4c613fd: Pulling fs layer
Step #1: c0c3f74f3f7c: Waiting
Step #1: 6d5fad3b20f0: Waiting
Step #1: 906c5911ea69: Waiting
Step #1: 3c18b1c18dfc: Waiting
Step #1: 0360f916794e: Waiting
Step #1: e90908c49002: Waiting
Step #1: 392df4c613fd: Waiting
Step #1: 42ebf62db3f5: Waiting
Step #1: ebeccf37c57f: Verifying Checksum
Step #1: ebeccf37c57f: Download complete
Step #1: 3c2cba919283: Verifying Checksum
Step #1: 3c2cba919283: Download complete
Step #1: 42ebf62db3f5: Verifying Checksum
Step #1: 42ebf62db3f5: Download complete
Step #1: 8ca77d5ce166: Verifying Checksum
Step #1: 8ca77d5ce166: Download complete
Step #1: 6d5fad3b20f0: Verifying Checksum
Step #1: 6d5fad3b20f0: Download complete
Step #1: 3c18b1c18dfc: Verifying Checksum
Step #1: 3c18b1c18dfc: Download complete
Step #1: 0360f916794e: Verifying Checksum
Step #1: 0360f916794e: Download complete
Step #1: e90908c49002: Verifying Checksum
Step #1: e90908c49002: Download complete
Step #1: 392df4c613fd: Verifying Checksum
Step #1: 392df4c613fd: Download complete
Step #1: 906c5911ea69: Verifying Checksum
Step #1: 906c5911ea69: Download complete
Step #1: 8ca77d5ce166: Pull complete
Step #1: c0c3f74f3f7c: Verifying Checksum
Step #1: c0c3f74f3f7c: Download complete
Step #1: 3c2cba919283: Pull complete
Step #1: ebeccf37c57f: Pull complete
Step #1: 42ebf62db3f5: Pull complete
Step #1: c0c3f74f3f7c: Pull complete
Step #1: 6d5fad3b20f0: Pull complete
Step #1: 906c5911ea69: Pull complete
Step #1: 3c18b1c18dfc: Pull complete
Step #1: 0360f916794e: Pull complete
Step #1: e90908c49002: Pull complete
Step #1: 392df4c613fd: Pull complete
Step #1: Digest: sha256:c6480acd38ca4605e0b83f5196ab6fe8a8b59a0288a7b8216c42dbc45b5de8f6
Step #1: Status: Downloaded newer image for gcr.io/google-appengine/python@sha256:c6480acd38ca4605e0b83f5196ab6fe8a8b59a0288a7b8216c42dbc45b5de8f6
Step #1:  ce284ab20159
Step #1: Step 2/9 : LABEL python_version=python3.6
Step #1:  Running in 5be356249ab0
Step #1: Removing intermediate container 5be356249ab0
Step #1:  9a539e15af9a
Step #1: Step 3/9 : RUN virtualenv --no-download /env -p python3.6
Step #1:  Running in 842dc034b716
Step #1: created virtual environment CPython3.6.10.final.0-64 in 998ms
Step #1:   creator CPython3Posix(dest=/env, clear=False, global=False)
Step #1:   seeder FromAppData(download=False, pip=bundle, wheel=bundle, setuptools=bundle, via=copy, app_data_dir=/root/.local/share/virtualenv)
Step #1:     added seed packages: pip==20.2.2, setuptools==49.6.0, wheel==0.35.1
Step #1:   activators PythonActivator,FishActivator,XonshActivator,CShellActivator,PowerShellActivator,BashActivator
Step #1: Removing intermediate container 842dc034b716
Step #1:  d35f58e671a3
Step #1: Step 4/9 : ENV VIRTUAL_ENV /env
Step #1:  Running in 9e66a6618cf8
Step #1: Removing intermediate container 9e66a6618cf8
Step #1:  5abfb9c8f3fd
Step #1: Step 5/9 : ENV PATH /env/bin:$PATH
Step #1:  Running in a07595800142
Step #1: Removing intermediate container a07595800142
Step #1:  8df74c16598f
Step #1: Step 6/9 : ADD requirements.txt /app/
Step #1:  5c1460f582d8
Step #1: Step 7/9 : RUN pip install -r requirements.txt
Step #1:  Running in cecf37bd6076
Step #1: Looking in links: https://download.pytorch.org/whl/torch_stable.html
Step #1: Collecting flask
Step #1:   Downloading Flask-2.0.2-py3-none-any.whl (95 kB)
Step #1: Collecting gunicorn
Step #1:   Downloading gunicorn-20.1.0-py3-none-any.whl (79 kB)
Step #1: Collecting numpy
Step #1:   Downloading numpy-1.19.5-cp36-cp36m-manylinux2010_x86_64.whl (14.8 MB)
Step #1: Collecting Pillow
Step #1:   Downloading Pillow-8.4.0-cp36-cp36m-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.1 MB)
Step #1: Collecting torch==1.8.1+cpu
Step #1:   Downloading https://download.pytorch.org/whl/cpu/torch-1.8.1%2Bcpu-cp36-cp36m-linux_x86_64.whl (169.1 MB)
Step #1: Collecting torchvision==0.9.1+cpu
Step #1:   Downloading https://download.pytorch.org/whl/cpu/torchvision-0.9.1%2Bcpu-cp36-cp36m-linux_x86_64.whl (13.3 MB)
Step #1: Collecting Werkzeug>=2.0
Step #1:   Downloading Werkzeug-2.0.2-py3-none-any.whl (288 kB)
Step #1: Collecting click>=7.1.2
Step #1:   Downloading click-8.0.3-py3-none-any.whl (97 kB)
Step #1: Collecting itsdangerous>=2.0
Step #1:   Downloading itsdangerous-2.0.1-py3-none-any.whl (18 kB)
Step #1: Collecting Jinja2>=3.0
Step #1:   Downloading Jinja2-3.0.2-py3-none-any.whl (133 kB)
Step #1: Requirement already satisfied: setuptools>=3.0 in /env/lib/python3.6/site-packages (from gunicorn->-r requirements.txt (line 2)) (49.6.0)
Step #1: Collecting typing-extensions
Step #1:   Downloading typing_extensions-3.10.0.2-py3-none-any.whl (26 kB)
Step #1: Collecting dataclasses; python_version < "3.7"
Step #1:   Downloading dataclasses-0.8-py3-none-any.whl (19 kB)
Step #1: Collecting importlib-metadata; python_version < "3.8"
Step #1:   Downloading importlib_metadata-4.8.1-py3-none-any.whl (17 kB)
Step #1: Collecting MarkupSafe>=2.0
Step #1:   Downloading MarkupSafe-2.0.1-cp36-cp36m-manylinux2010_x86_64.whl (30 kB)
Step #1: Collecting zipp>=0.5
Step #1:   Downloading zipp-3.6.0-py3-none-any.whl (5.3 kB)
Step #1: Installing collected packages: dataclasses, Werkzeug, typing-extensions, zipp, importlib-metadata, click, itsdangerous, MarkupSafe, Jinja2, flask, gunicorn, numpy, Pillow, torch, torchvision
Step #1: Successfully installed Jinja2-3.0.2 MarkupSafe-2.0.1 Pillow-8.4.0 Werkzeug-2.0.2 click-8.0.3 dataclasses-0.8 flask-2.0.2 gunicorn-20.1.0 importlib-metadata-4.8.1 itsdangerous-2.0.1 numpy-1.19.5 torch-1.8.1+cpu torchvision-0.9.1+cpu typing-extensions-3.10.0.2 zipp-3.6.0
Step #1: WARNING: You are using pip version 20.2.2; however, version 21.3 is available.
Step #1: You should consider upgrading via the '/env/bin/python -m pip install --upgrade pip' command.
Step #1: Removing intermediate container cecf37bd6076
Step #1:  b75c85f9bc20
Step #1: Step 8/9 : ADD . /app/
Step #1:  7f0e717d865a
Step #1: Step 9/9 : CMD exec gunicorn -b :$PORT app:app --capture-output
Step #1:  Running in 17b148cda67e
Step #1: Removing intermediate container 17b148cda67e
Step #1:  545c81b69432
Step #1: Successfully built 545c81b69432
Step #1: Successfully tagged asia.gcr.io/brain-tumor-segment-api/appengine/default.20211016t090551:latest
Finished Step #1
PUSH
Pushing asia.gcr.io/brain-tumor-segment-api/appengine/default.20211016t090551:latest
The push refers to repository [asia.gcr.io/brain-tumor-segment-api/appengine/default.20211016t090551]
843f6b170822: Preparing
462ce3349a91: Preparing
ee91a095a4d0: Preparing
b44377bc1943: Preparing
087d7553d285: Preparing
16919ab89eca: Preparing
74bcef7f7402: Preparing
bc9e931c388e: Preparing
20896f2c3dd8: Preparing
7b80c69caf34: Preparing
3bbec54fac0c: Preparing
4006ffa4c683: Preparing
844d958e8cbe: Preparing
84ff92691f90: Preparing
b49bce339f97: Preparing
dcb7197db903: Preparing
16919ab89eca: Waiting
74bcef7f7402: Waiting
bc9e931c388e: Waiting
20896f2c3dd8: Waiting
7b80c69caf34: Waiting
3bbec54fac0c: Waiting
4006ffa4c683: Waiting
844d958e8cbe: Waiting
84ff92691f90: Waiting
b49bce339f97: Waiting
dcb7197db903: Waiting
087d7553d285: Layer already exists
16919ab89eca: Layer already exists
74bcef7f7402: Layer already exists
bc9e931c388e: Layer already exists
20896f2c3dd8: Layer already exists
ee91a095a4d0: Pushed
7b80c69caf34: Layer already exists
3bbec54fac0c: Layer already exists
844d958e8cbe: Layer already exists
4006ffa4c683: Layer already exists
843f6b170822: Pushed
b44377bc1943: Pushed
b49bce339f97: Layer already exists
dcb7197db903: Layer already exists
84ff92691f90: Layer already exists
462ce3349a91: Pushed
latest: digest: sha256:4edf28bc68a8a62dcd84eb949df639b38306acfe2ffbc6d02b66b6df0c6dfa16 size: 3674
DONE
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Updating service [default] (this may take several minutes)...working.. 
Updating service [default] (this may take several minutes)...done.     
Setting traffic split for service [default]...done.   
Deployed service [default] to [https://brain-tumor-segment-api.as.r.appspot.com]

You can stream logs from the command line by running:
  $ gcloud app logs tail -s default

To view your application in the web browser run:
  $ gcloud app browse
```
Now the website can be found there on link provided above.