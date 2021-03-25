import './App.css';
import React, {Component, useState} from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';

import Forecast from './components/forecast';

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Routes,
  Link,
  useHistory,
  withRouter
} from "react-router-dom";

function SubmitButton(props) {
    let history = useHistory();

    function handleClick() {
      history.push("/forecast");
    }

    return (
      <button type="button" onClick={handleClick}>
        Search
      </button>
    );
  }

export default function App(){

    const [token, setToken] = useState(null);

    function handleSubmit(event){
        alert('A name was submitted: '+ token);
        event.preventDefault();
      }

    function handleChange(event){
        setToken(event.target.value);
    }



    return (
    <Router>
          <form onSubmit={handleSubmit} className="App">
            <h1> Stock Price Forecast </h1>
            <label>
              Stock Token:
              <input type="text" value={token} onChange={handleChange} />
            </label>
            <SubmitButton />
            <Route path="/forecast">
                <Forecast token={token} />
            </Route>
          </form>
    </Router>
        );

}

//const rootElement = document.getElementById("root");
//ReactDOM.render(<App />, document.getElementById('root'));


{/*class SubForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {token: '', isSubmit: false, update_token: ''};

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleClick = this.handleClick.bind(this);
  }

  handleChange(event) {
    this.setState({token: event.target.value});
  }

  handleSubmit(event) {
    alert('A name was submitted: ' + this.state.token);
    event.preventDefault();

  }

  handleClick(){
              //let history = useHistory();
              console.log(this.props.history);

              this.setState({update_token: this.state.token});
              const data = {token: this.state.token};

                  axios.post('http://localhost:5000/search',
                                    data)
                                    .then(function (response){
                                    console.log(response);
                                    })
                                    .catch(function (error){
                                    console.log(error);
                                    });
              this.props.history.push("/forecast");


          }

  render() {



    return (
      <form onSubmit={this.handleSubmit} className="App">
        <h1> Stock Price Forecast </h1>
        <label>
          Stock Token:
          <input type="text" value={this.state.token} onChange={this.handleChange} />
        </label>
        <button onClick={this.handleClick} >
            <b>submit</b>

        </button>

        <Route path="/forecast">
            <Forecast token={this.state.token} />
        </Route>


      </form>
    );
  }
}

const AppWithRouter = withRouter(SubForm);


const App = () => {
          return (
            <Router>
              <AppWithRouter />
            </Router>
          );
        } ;
export default App;*/}

