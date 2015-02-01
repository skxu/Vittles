var App = React.createClass({
  getInitialState: function() {
    
    return {
      userid: '',
    }
  },
  
  componentDidMount: function() {
    /**load stuff*/
    var _this = this;
    var xmlHttp = null;
    xmlHttp = new XMLHttpRequest();
    xmlHttp.open(
      "POST", 
      "http://vittles.code.io/api/users",
      true
    );
    
    data = new FormData();
    data.append('username','test5');
    data.append('password','password');
    
    
    xmlHttp.onload = function(e) {
      console.log(xmlHttp.responseText);
      _this.setState({'userid': xmlHttp.responseText.userid});
    }.bind(this);
    
    xmlHttp.send(data);
      
      
  },
  
  render: function() {
    var _this = this;
    
    return (
      <div>
        <p>Coming Soon.</p>
        <p>User ID: {this.state.userid}</p>
      </div>
    );
  }
});
  
React.renderComponent(
  <App />,
  document.body
);