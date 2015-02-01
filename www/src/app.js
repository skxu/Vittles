var App = React.createClass({
  getInitialState: function() {
    return {
      rankings: '',
    }
  },
  
  componentDidMount: function() {
    /**load stuff*/
  },
  
  render: function() {
    var _this = this;
    
    return (
      <div>
        <p>Coming Soon.</p>
      </div>
    );
  }
});
  
React.renderComponent(
  <App />,
  document.body
);