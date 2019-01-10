<%!from desktop.views import commonheader, commonfooter %>
<%!from django.http import HttpRequest %>
<%namespace name="shared" file="shared_components.mako" />
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">


## Use double hashes for a mako template comment
## Main body
<script type="text/javascript">
window.onload=function(){
var a = window.location.href;
var ipold = a.replace("8000/SparkState/","");
var ipnew = ipold.replace("http://","");
var url1 = "http://" + ipnew + "7070";
//alert(url1);
document.getElementById("spark").href=url1;
}
</script>

<div id="pagewrap">
    <div class="navigator">
       %if not is_embeddable:
       ${commonheader("Sparkstate", "SparkState", user,"25px") | n,unicode}
        %endif
    </div>
    <div class="navbar navbar-inverse ">
        <div class="navbar-inner">
            <div class="container-fluid">
                <div class="nav-collapse">
                    <ul class="nav">
                        <li role="presentation" class="currentApp">
                            <a href="/SparkState/">
                                <img class="app-icon" src="${ static('SparkState/art/icon_SparkState_48.png') }">
                                Sparkstate</a></li>
                        <li role="presentation" class="active">
                            <a href="/SparkState/">spark</a></li>
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
                            <h3 class="card-title">spark集群job概况</h3>
                            <p class="card-text">点击下面链接可查看spark集群job状态.</p>
                            <a href="http://${ip}:7070" id="spark" target="_blank" class="card-link">Spark Overview</a>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>

</div>


