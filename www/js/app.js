var App = React.createClass({
  getInitialState: function() {
    
    return {
      userid: '',
    }
  },
  
  componentDidMount: function() {
    /**load stuff*/
    console.log("testtttt");
    var xmlHttp = null;
    xmlHttp = new XMLHttpRequest();
    xmlHttp.open(
      "POST", 
      "http://vittles.code.io/api/users",
      true
    );
    
    params = "username=test&password=test"
    
    http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    http.setRequestHeader("Content-length", params.length);
    http.setRequestHeader("Connection", "close");

    
    xmlHttp.onload = function(e) {
      console.log(xmlHttp.response); 
      this.setState({'userid': xmlHttp.response});
    };
    
    xmlHttp.send(params);
      
      
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