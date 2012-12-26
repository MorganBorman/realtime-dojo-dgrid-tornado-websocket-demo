realtime-dojo-dgrid-tornado-websocket-demo
==========================================

A demo user management widget using realtime dojo stores and dgrid connected over websockets with a tornado backend.

Dependencies
------------
tornado
sqlalchemy

Installing dgrid
----------------

First make sure _cpm_ is installed: https://github.com/kriszyp/cpm

Then run:
```bash
cd demo/static/lib/
cpm install dgrid
rm -rf dojo/
```

Running
---------------

To run:
```bash
cd demo/
python main.py
```
