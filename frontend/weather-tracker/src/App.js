import './App.css';
import {HashRouter as Router, Routes, Route} from 'react-router-dom'
import Home from "./pages/Home"
import Account from './pages/Account';
import Country from './pages/Country';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />}/>
        <Route path="/account" element={<Account />}/>
        <Route path="/country/:name" element={<Country />}/>
      </Routes>
    </Router>
  );
}

export default App;
