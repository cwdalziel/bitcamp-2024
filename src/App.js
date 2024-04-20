import './App.css';
import CreateAccount from './CreateAccount'

function App() {

  const formSubmit = (values) => {
    console.log(values)
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
