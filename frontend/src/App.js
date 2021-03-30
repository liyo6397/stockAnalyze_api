import './App.css';
import React, {Component, useState, useEffect, useRef, useCallback} from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import { PersistGate } from 'redux-persist/integration/react'

import EM_Results from './components/forecast';

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Routes,
  Link,
  useHistory,
  withRouter,
  useRouteMatch,
  useLocation,
} from "react-router-dom";



function SubmitButton(props) {

    let history = useHistory();
    function handleClick(event){
        history.push("/forecast");
    }
    return (
          <button type="button" onClick={handleClick}>
            Search
          </button>
    );
  }

function useLocalStorage(keyValue){

    const [value, setValue] = useState(
     localStorage.getItem(keyValue) ||'');

    useEffect(() => {
        localStorage.setItem(keyValue, value);
    }, [value]);

    return [value, setValue];
}




export default function App(){

    const [token, setToken] = useLocalStorage(null);
    const [clicked, setClick] = useState(true);
    const inputRef = useRef(null);
    const resetClick = () => setClick(false);

    function handleSubmit(event){
        inputRef.current.click();
        event.preventDefault();

        alert('A name was submitted: '+ token);
      }

    function handleChange(event){
        event.preventDefault();
        setToken(event.target.value);

    }

    return (
          <Router>
          <div className="App">
            <h1> Stock Price Forecast </h1>
            <label>
              Stock Token:
              <input type="text" value={token} onChange={handleChange} />
            </label>
            <Link to="/forecast" >
                <input type='submit' value="Search" onClick={() => setClick(true)}/>
            </Link>
            <Switch>

                    <Route path="/forecast" >

                        <EM_Results token={token} clicked={clicked} resetClick={resetClick}/>

                    </Route>

            </Switch>
          </div>
          </Router>



        );

}


