
<%!
def is_selected(section, matcher):
  if section == matcher:
    return "active"
  else:
    return ""
%>

<%def name="menubar(section='')">
  <div class="navbar navbar-inverse navbar-fixed-top nokids">
    <div class="navbar-inner">
      <div class="container-fluid">
        <div class="nav-collapse">
          <ul class="nav">
            <li class="currentApp">
              <a href="/NodeState">
                <img src="${ static('art/icon_NodeState_48.png') }" class="app-icon" />
                NodeState
              </a>
<%!
def is_selected(section, matcher):
  if section == matcher:
    return "active"
  else:
    return ""
%>

<%def name="menubar(section='')">
  <div class="navbar navbar-inverse navbar-fixed-top nokids">
    <div class="navbar-inner">
      <div class="container-fluid">
        <div class="nav-collapse">
          <ul class="nav">
            <li class="currentApp">
              <a href="/NodeState">
                <img src="${ static('art/icon_NodeState_48.png') }" class="app-icon" />
                NodeState
              </a>
             </li>
             <li class="${is_selected(section, 'mytab')}"><a href="#">Tab 1</a></li>
             <li class="${is_selected(section, 'mytab2')}"><a href="#">Tab 2</a></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</%def>

             </li>
             <li class="${is_selected(section, 'mytab')}"><a href="#">Tab 1</a></li>
             <li class="${is_selected(section, 'mytab2')}"><a href="#">Tab 2</a></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</%def>
