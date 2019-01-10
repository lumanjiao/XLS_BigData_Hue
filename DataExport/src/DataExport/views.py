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

def index(request):
  uname = request.POST.get('uname', None)
  pwd = request.POST.get('pwd', None)
  actionUser = request.POST.get('action',None)
  name = str(uname)
  password = str(pwd)
  action = str (actionUser)
  print uname
  print action
  out = ""
  if uname != "":
    if pwd != "":
      if action == "1":
        print "add==============="
        #os.system('python /home/register.py %s %s' % (name, password))
        #python /home/kettlemaster.py %s %s' % (name, password)
        t_f = os.popen("python3 /home/XLS_BigData/Data_Export/usersAdd.py %s %s" % (name, password))
        global out
        out = str(t_f.read())
        print out
    else:
      out = "password null"
  else:
     print "name null"
     out = "username null"
  return render('index.mako', request, {'is_embeddable': request.GET.get('is_embeddable', False),'output': out,}, )

def selectall(request):
  UserAndPwd = "lmj"
  #os.system('python /home/selectAll.py')
  t_f = os.popen("cat /home/XLS_BigData/Data_Export/usernames.txt")
  tf = str(t_f.read())
  print tf

  return render('selectall.mako', request, {'is_embeddable': request.GET.get('is_embeddable', False), 'output': tf, }, )

def deleteuser(request):
  uname = request.POST.get('uname', None)
  actionUser = request.POST.get('action',None)
  name = str(uname)
  action = str (actionUser)
  print uname
  print action
  out = ""
  if uname != "":
      if action == "2":
        print "delete ===================="
        t_f = os.popen("python3 /home/XLS_BigData/Data_Export/userDel.py %s" % (name))
        global out
        out = str(t_f.read())
        print out
  else:
     print "name null"
     out = "username null"
  return render('deleteuser.mako', request, {'is_embeddable': request.GET.get('is_embeddable', False),'output': out,}, )



