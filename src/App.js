import { useState } from 'react';
import './App.css';
import Login from './Login';
import Budgeter from './Budgeter';

function App() {

  const [username, setUsername] = useState('')
  const [gameOver, setGameOver] = useState(false)

  const setUser = (user) => {
    setUsername(user)
  }

  const lose = () => {
    setGameOver(true)
  }

  return (
    <div className="App">
      <header className="App-header">
        {gameOver ? <h1>You Lose</h1> : (username === '') ? <Login setUser={setUser}/> : <Budgeter lose={lose} user={username}/>}
      </header>
    </div>
  );
}

export default App;
