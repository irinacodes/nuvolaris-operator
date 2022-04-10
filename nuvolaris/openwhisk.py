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
import nuvolaris.kustomize as kus
import nuvolaris.kube as kube
import nuvolaris.config as cfg
import os, os.path
import urllib.parse
import logging
import kopf

WHISK_IMG = os.environ.get("STANDALONE_IMAGE", "ghcr.io/nuvolaris/openwhisk-standalone")
WHISK_TAG = os.environ.get("STANDALONE_TAG", "latest")
WHISK_SPEC = "state.openwhisk.spec"

# this functtions returns
def apihost(apiHost):
    url = urllib.parse.urlparse("https://pending")
    if len(apiHost) > 0 and "hostname" in apiHost[0]:
        url = url._replace(netloc = apiHost[0]['hostname'])
    if cfg.exists("nuvolaris.apihost"):
        url =  url._replace(netloc = cfg.get("nuvolaris.apihost"))
    if cfg.exists("nuvolaris.protocol"):
        url = url._replace(scheme = cfg.get("nuvolaris.protocol"))
    if cfg.exists("nuvolaris.apiport"):
        url = url._replace(netloc = f"{url.hostname}:{cfg.get('nuvolaris.apiport')}")
    return url.geturl()

def create():
    config = kus.image(WHISK_IMG, newTag=WHISK_TAG)
    data = {
        "admin_user": cfg.get("couchdb.admin.user"),
        "admin_password": cfg.get("couchdb.admin.password")
    }
    #config += kus.configMapTemplate("standalone-kcf", "openwhisk-standalone",  "standalone-kcf.conf", data)
    spec = kus.kustom_list("openwhisk-standalone", config, templates=["standalone-kcf.yaml"], data=data)
    cfg.put(WHISK_SPEC, spec)
    return kube.apply(spec)

def delete():
    if cfg.exists(WHISK_SPEC):
        res = kube.delete(cfg.get(WHISK_SPEC))
        cfg.delete(WHISK_SPEC)
        return res
    return "not found"

def cleanup():
    return kube.kubectl("delete", "pod", "--all")

def annotate(keyval):
    kube.kubectl("annotate", "cm/config",  keyval, "--overwrite")