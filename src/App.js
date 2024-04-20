import './App.css';
import CreateAccount from './CreateAccount'

function App() {

  const formSubmit = () => {
    
  }

  return (
    <div className="App">
      <header className="App-header">
        <CreateAccount formSubmit={formSubmit} />
      </header>
    </div>
  );
}

export default App;
