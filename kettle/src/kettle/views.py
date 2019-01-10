#!/usr/bin/env python
# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from desktop.lib.django_util import render
import os
import json

def index(request):
  uname = request.GET.get('uname', None)
  pwd = request.GET.get('pwd', None)
  name = str(uname)
  password = str(pwd)
  print(uname)
  if uname != None:
    os.system('python /home/XLS_BigData/Data_ETL/kettlemaster.py %s %s' % (name, password))
  return render('index.mako', request, {'is_embeddable':request.GET.get('is_embeddable',False),'ip':request.META['REMOTE_ADDR']},)

def control(request):
  uname = request.POST.get('uname', None)
  pwd = request.POST.get('pwd', None)
  name = str(uname)
  password = str(pwd)
  print(uname)
  if uname != None:
    os.system('python /home/XLS_BigData/Data_ETL/kettlemaster.py %s %s' % (name, password))
  return render('control.mako', request, {'is_embeddable':request.GET.get('is_embeddable',False),'ip':request.META['REMOTE_ADDR']})
def over(request):
  return render('over.mako', request, {'is_embeddable':request.GET.get('is_embeddable',False),'ip':request.META['REMOTE_ADDR']})


