<%!from desktop.views import commonheader, commonfooter %>
<%!from django.http import HttpRequest %>
<%namespace name="shared" file="shared_components.mako" />
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">

<script src="${ static('js/jquery-2.1.1.min.js') }"></script>

<script type="text/javascript">

    function xx() {
        form = document.getElementById("form")
        hidden = document.getElementById("hidden")
        hidden.value = '1'
        form.submit()

    }

    function del() {
        form = document.getElementById("form")
        hidden = document.getElementById("hidden")
        hidden.value = '2'
        form.submit()

     }

</script>
<div id="pagewrap">
    <div class="navigator">
       %if not is_embeddable:
        ${commonheader("Dataexport", "DataExport", user,"25px") | n,unicode}
        %endif
    </div>
    <div class="navbar navbar-inverse ">
        <div class="navbar-inner">
            <div class="container-fluid">
                <div class="nav-collapse">
                    <ul class="nav">
                        <li role="presentation" class="currentApp">
                            <a href="/DataExport">
                                <img class="app-icon" src="${ static('DataExport/art/icon_DataExport_48.png') }">
                                DataExport</a></li>
                        <li role="presentation" class="">
                            <a href="/DataExport/">增加用户</a></li>
                        <li role="presentation" class="">
                            <a href="/DataExport/selectall">查看所有用户</a></li>
                         <li role="presentation" class="active">
                            <a href="/DataExport/deleteuser">删除用户</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
    <div id="yemian" class="container-fluid">
        <div class="card">
            <div class="row-fluid">
                <div class="span10 offset1 center error-wrapper">
                    <div class="card bg-success text-white">
                        <div class="card-body">
                         <h3 class="card-title">设置DataExport的执行权限</h3>
                            <form class="navbar-form navbar-left" role="search" method="post" id="form">
                                ${ csrf_token(request) | n,unicode }
                                <div class="form-group">
                                    用户名：
                                    <input type="text" class="form-control"  id="name" name="uname" placeholder="username">
                                </div>
                                 &nbsp;&nbsp; <input type="hidden" id="hidden" name="action" value="1">

                                <div class="form-group">
                                    <button onclick="del()" type="button"  id="deleteUser" name="deleteUser" value="2">删除用户</button>
                                     &nbsp;&nbsp;
                                    <button type="button" id="btn"   onclick="window.location.href=' ../../DataExport/selectall '">查看所有用户</button>
                                </div>
                                <div class="form-group" id="hidden" style="">
                                   % if True:
                                    <pre> ${output}</pre>
                                   % endif
                                </div>

                            </form>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>

</div>