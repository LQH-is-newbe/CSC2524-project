import React, { useState, useRef } from 'react';
import FrontPage from './FrontPage';
import MainPage from './MainPage';

const App = () => {
    const [page, setPage] = useState('frontPage')
    const mainPageInit = useRef(null)
    const onFrontPageSubmit = (init) => {
      mainPageInit.current = init
      setPage('mainPage')
    }

    return (
      <>
        { page === 'frontPage' ? 
          <FrontPage onFrontPageSubmit={onFrontPageSubmit}/> 
          : 
          <MainPage init={mainPageInit.current} onNewProject={()=>setPage('frontPage')}/> 
        }
      </>
    );
};
export default App;
