import React, {Component, useEffect, useState, useCallback} from 'react';
import axios from 'axios';



function EM_Results({ token, clicked, resetClick }) {

     const [error, setError] = useState(null);
     const [isLoaded, setIsLoaded] = useState(false);
     const [items, setItems] = useState([]);



     function postData()
     {

        axios.post('http://localhost:5000/search',
                    {tk : token})
                   .then(function (response){
                    console.log(response);
                    })
                    .catch(function (error){
                    console.log(error);
                });
     }

     const getData = useCallback( async () =>{
        postData();
        const url='http://localhost:5000/info/'+token;
        axios.get(url)
             .then(res => {
               setIsLoaded(true);
               setItems(res.data);
               })
             .catch(function (error) {
                              // handle error
               console.log(error);
             });
     }, [token]);

     // Note: the empty deps array [] means
       // this useEffect will run once
       // similar to componentDidMount()
     useEffect(() => {
        if (clicked){
            getData().then(resetClick);
            }
         {/*postData(token);
         const url='http://localhost:5000/info/'+token;
         axios.get(url)
               .then(res => {
               setIsLoaded(true);
               setItems(res.data);
               })
               .catch(function (error) {
                      // handle error
                 console.log(error);
               });*/}

       }, [clicked, getData])


    //const {items, isLoaded, error} = this.state;
    //const token = this.props.token;

    if (!isLoaded)
    {
        return <h5>Loading...</h5>;
    }
    else
        return(
        <div >
            <h1> The forecast price of {token}</h1>
            <h5> From {items.min_price} to {items.max_price}</h5>
            <h5> The volatility: {items.std} </h5>
            <h5>Compaired to last day price: {items.last_c} </h5>
        </div>
        );

    } export default React.memo(EM_Results);



