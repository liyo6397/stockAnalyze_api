import React, {Component, useEffect, useState} from 'react';
import axios from 'axios';

function EM_Results(props) {
    {/*constructor(props){
        super(props);
        this.state = {isLoaded: false, items: []};
    }

    componentDidMount()
     {
         const token = this.props.token;
         const isLoaded = this.props.isLoaded;
         const url='http://localhost:5000/info/'+token;


         axios.get(url)
           .then(res => {this.setState({isLoaded: true,items: res.data})})
           .catch(function (error) {
             // handle error
             console.log(error);
           });
     }*/}

     const [error, setError] = useState(null);
     const [isLoaded, setIsLoaded] = useState(false);
     const [items, setItems] = useState([]);
     const url='http://localhost:5000/info/'+props.token;

     // Note: the empty deps array [] means
       // this useEffect will run once
       // similar to componentDidMount()
       useEffect(() => {
         axios.get(url)
               .then(res => {
               setIsLoaded(true);
               setItems(res.data);
               })
               .catch(function (error) {
                      // handle error
                 console.log(error);
               });
       }, [])


    //const {items, isLoaded, error} = this.state;
    //const token = this.props.token;

    if (!isLoaded)
    {
        return <h5>Loading...</h5>;
    }
    else
        return(
        <div>
            <h5> Token: {props.token} </h5>
            <h5> From {items.min_price} to {items.max_price}</h5>
            <h5> The volatility: {items.std} </h5>
        </div>
        );

    }



function Forecast(props){
    const token = props.token;
    return (
        <div>
        <h1> The forecast price of {token}</h1>
        <EM_Results token={token}/>
        </div>
    );


} export default Forecast;