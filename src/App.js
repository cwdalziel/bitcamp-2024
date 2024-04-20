import { useState } from 'react';
import './App.css';
import CreateAccount from './CreateAccount'

function App() {

  const [accountID, setAccountID] = useState('')

  const formSubmit = (res) => {
    setAccountID(res.data.data.objectCreated._id)
  }

  return (
    <div className="App">
      <header className="App-header">
        {(accountID === '') ? <CreateAccount formSubmit={formSubmit} /> : <div>Logged In!</div>}
      </header>
    </div>
  );
}

export default App;
