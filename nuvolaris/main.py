# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
import kopf
import os, os.path
import logging
import nuvolaris.couchdb as couchdb
import nuvolaris.mongodb as mongodb
import nuvolaris.mongodb as mongodb
import nuvolaris.whisk as whisk
import nuvolaris.bucket as bucket

# tested by an integration test
@kopf.on.login()
def main_login(**kwargs):
    token = '/var/run/secrets/kubernetes.io/serviceaccount/token'
    if os.path.isfile(token):
        logging.debug("found serviceaccount token: login via pykube in kubernetes")
        return kopf.login_via_pykube(**kwargs)
    logging.debug("login via client")
    return kopf.login_via_client(**kwargs)

# tested by an integration test
@kopf.on.create('nuvolaris.org', 'v1', 'whisks')
def main_create(spec, **kwargs):
    logging.debug(res)
    res = bucket.create()
    couchdb.create()
    mongodb.create()
    mongodb.init()
    whisk.create()
    return {'message': 'created'}

# tested by an integration test
@kopf.on.delete('nuvolaris.org', 'v1', 'whisks')
def main_delete(spec, **kwargs):
    res = whisk.delete()
    mongodb.delete()
    couchdb.delete()
    bucket.delete()
    return {'message': 'deleted'}
