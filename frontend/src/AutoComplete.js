import PropTypes from 'prop-types';
import {useEffect, useState} from 'react';


function show_option_list(options){
}

function useGetData(){

        const [items, setItems] = useState([]);

        axios.get('stockSymbols.json')
        .then(res => {
              setItems(res.data);
              })

        return items
    }


export default function AutoComplete(searchItem){

    const options = useGetData();
    const [results, setResults] = useState([]);

    useEffect(() => {

        const temp_results = options.filter(option =>
              option.toLowerCase().includes(searchTerm)
            );
            setResults(results);
          }, [searchTerm]);


    }, [searchItem]);

    return (

        <div>
            {search_results.map( item => (
                <li>{item}</li>
            ))
            }
        </div>
    );
}