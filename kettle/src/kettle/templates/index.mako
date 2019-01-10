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
    function xx(){
        $.ajax({
            url:'../kettle',
            type:'get',
            data:{uname:$('#name').val(),pwd:$('#pwd').val()},
            dataType:'json',
            success:function(){
                alert("用户" + $('#name').val()  + "成功在kettle中创建!!!")
            },
            error:function(){
                alert("error")
            }
        });


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
                        <li role="presentation" class="active">
                            <a href="/kettle/control">kettle</a></li>
                        <li role="presentation" class="">
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
                             <h3 class="card-title">设置kettle的执行权限：请添加用户</h3>
                            <form class="navbar-form navbar-left" role="search" method="post">
                                ${ csrf_token(request) | n,unicode }
                                <div class="form-group">
                                    用户名：
                                    <input type="text" class="form-control"  id="name" name="uname" placeholder="username">
                                </div>

                                <div class="form-group">
                                    密 &nbsp;&nbsp;码：
                                    <input type="text" class="form-control"  id="pwd" name="pwd" placeholder="password">
                                </div>
                                 &nbsp;&nbsp;

                                <div class="form-group">
                                     &nbsp;&nbsp;
                                    <button onclick="xx()" type="button" id="btn"   >提交</button>
                                </div>


                            </form>

                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>

</div>

