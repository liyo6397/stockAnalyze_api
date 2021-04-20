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

function useSessionStorage(keyValue){

    const [value, setValue] = useState(
     sessionStorage.getItem(keyValue) ||'');

    useEffect(() => {
        sessionStorage.setItem(keyValue, value);
    }, [value]);

    return [value, setValue];
}

export default function App(){

    const [token, setToken] = useSessionStorage(null);
    const [searchItem, setSearchItems] = useState(null);


    const [clicked, setClick] = useState(true);
    const resetClick = () => setClick(false);






    function handleSubmit(event){
        //inputRef.current.click();
        event.preventDefault();
        //setOptionSelected(false);
        alert('A name was submitted: '+ token);
      }

    function handleChange(event){
        setSearchItems(event.currentTarget.value);
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
                <input type='submit' value="Search" placeholder="Search for symbols or companies."onClick={() => setClick(true)}/>
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


