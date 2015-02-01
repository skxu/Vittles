var App = React.createClass({
  getInitialState: function() {
    
    return {
      userid: '',
    }
  },
  
  componentDidMount: function() {
    /**load stuff*/
    var xmlHttp = null;
    xmlHttp = new XMLHttpRequest();
    xmlHttp.open(
      "POST", 
      "http://vittles.code.io/api/users",
      true
    );
    
    params = "username=test&password=test"
    
    xmlHttp.onload = function(e) {
      console.log(xmlHttp.responseText);
      this.setState({'userid': xmlHttp.responseText.userid});
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