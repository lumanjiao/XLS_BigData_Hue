<%!from desktop.views import commonheader, commonfooter %>
<%!from django.http import HttpRequest %>
<%namespace name="shared" file="shared_components.mako" />
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">

<script src="${ static('js/jquery-2.1.1.min.js') }"></script>

<script type="text/javascript">
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
                        <li role="presentation" class="active">
                            <a href="/DataExport/selectall">查看所有用户</a></li>
                        <li role="presentation" class="">
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
                         <h3 class="card-title">可操作数据导出模块的所有用户</h3>
                            % if True:
                                <pre> ${output}</pre>
                            % endif
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>

</div>



