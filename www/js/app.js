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
    data.append('username','test7');
    data.append('password','password');
    
    
    xmlHttp.onload = function(e) {
      console.log(xmlHttp.responseText);
      id = JSON.parse(xmlHttp.responseText).userid
      _this.setState({'userid': id});
    };
    
    xmlHttp.send(data);
      
      
  },
  
  
  register: function() {
    var _this = this;
    var xmlHttp = null;
    xmlHttp = new XMLHttpRequest();
    xmlHttp.open(
      "POST", 
      "http://vittles.code.io/api/users",
      true
    );
    
    data = new FormData();
    data.append('username','test6');
    data.append('password','password');
    
    
    xmlHttp.onload = function(e) {
      console.log(xmlHttp.responseText);
      console.log(xmlHttp.responseText.userid);
      _this.setState({'userid': 'lol'+xmlHttp.responseText.userid});
    };
    
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