<%!from desktop.views import commonheader, commonfooter %>
<%!from django.http import HttpRequest %>
<% import os %>
<%namespace name="shared" file="shared_components.mako" />
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">


## Use double hashes for a mako template comment
## Main body
<script src="${ static('js/jquery-2.1.1.min.js') }"></script>
<script type="text/javascript">
    window.onload=function(){
    var a = window.location.href;
    var ipold = a.replace("8000/kettle/over","");
    var ipnew = ipold.replace("http://","");
    var url1 = "http://" + ipnew + "8080";
    //alert(url1);
    document.getElementById("kettle").href=url1;
}
</script>

<div id="pagewrap">
    <div class="navigator">
       %if not is_embeddable:
       ${commonheader("Kettle", "kettle", user, "25px") | n,unicode}
        %endif
    </div>
    <div class="navbar navbar-inverse ">
        <div class="navbar-inner">
            <div class="container-fluid">
                <div class="nav-collapse">
                    <ul class="nav">
                        <li role="presentation" class="currentApp">
                            <a href="/kettle/">
                                <img class="app-icon" src="${ static('kettle/art/icon_kettle_48.png') }">
                                Kettle</a></li>
                        <li role="presentation" class="">
                            <a href="/kettle/control">kettle</a></li>
                        <li role="presentation" class="active">
                            <a href="/kettle/over">overview</a></li>
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

                              <div class="form-group">
                                <h3 class="card-title">kettle集群job概况</h3>
                                <p class="card-text">点击下面链接可查看kettle集群job状态.</p>
                                <a href="http://${ip}:8080" id="kettle" target="_blank" class="card-link">kettle Overview</a>
                               </div>

                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>

</div>

