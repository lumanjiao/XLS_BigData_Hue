<%!from desktop.views import commonheader, commonfooter %>
<%!from django.http import HttpRequest %>
<%namespace name="shared" file="shared_components.mako" />
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<script type="text/javascript">
window.onload=function(){
var a = window.location.href;
var ipold = a.replace(":8000/NodeState/","");
var ipnew = ipold.replace("http://","");
var url1 = "http://" + ipnew + ":50070";
//alert(url1);
var url2 = "http://" + ipnew + ":50070" + "/dfshealth.html#tab-datanode";
document.getElementById("hadoop").href=url1;
document.getElementById("data").href=url2;
}
</script>
<div id="pagewrap">
    <div class="navigator">
       %if not is_embeddable:
        ${commonheader("Node State", "Node_state", user, "25px") | n,unicode}
        %endif
    </div>
    <div class="navbar navbar-inverse ">
        <div class="navbar-inner">
            <div class="container-fluid">
                <div class="nav-collapse">
                    <ul class="nav">
                        <li role="presentation" class="currentApp">
                            <a href="/NodeState">
                                <img class="app-icon" src="${ static('art/icon_NodeState_48.png') }">
                                NodeState</a></li>
                        <li role="presentation" class="active">
                            <a href="/NodeState/">node</a></li>
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
                            <h3 class="card-title">hadoop集群概况</h3>
                            <p class="card-text">点击下面链接可查看hadoop集群状态.</p>
                            <a href="http://${ip}:50070" id="hadoop" target="_blank" class="card-link">Hadoop Overview</a>

                            <h4 > </h4>
                            <a href="http://${ip}:50070/dfshealth.html#tab-datanode" id="data"target="_blank" class="card-link">Datanodes Information</a>
                            <h2> <p class+"card-text"> </p></h2>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>
</div>
