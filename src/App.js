import { useState } from 'react';
import './App.css';
import Login from './Login';
import Budgeter from './Budgeter';

function App() {

  const [username, setUsername] = useState('')

  const setUser = (user) => {
    setUsername(user)
  }

  return (
    <div className="App">
      <header className="App-header">
        {(username === '') ? <Login setUser={setUser}/> : <Budgeter user={username}/>}
      </header>
    </div>
  );
}

export default App;
