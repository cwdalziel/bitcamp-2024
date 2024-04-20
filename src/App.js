import { useState } from 'react';
import './App.css';
import Login from './Login';

function App() {

  const [accountID, setAccountID] = useState('')

  const setID = (ID) => {
    setAccountID(ID)
  }

  return (
    <div className="App">
      <header className="App-header">
        {(accountID === '') ? <Login setID={setID}/> : <div>Logged In!</div>}
      </header>
    </div>
  );
}

export default App;
