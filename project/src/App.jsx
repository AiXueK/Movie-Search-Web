import React from 'react';
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
} from 'react-router-dom';

import Register from './pages/Register';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import ForgetPassword from './pages/ForgetPassword';
import SearchByForm from './components/SearchByForm';
import SortByForm from './components/SortByForm';
import SearchForm from './components/SearchForm';
import Movie from './pages/Movie';
import Search from './pages/Search';
import EditProfile from './pages/EditProfile';
import Error from './pages/Error';

function App() {
  const page = {
    display: 'flex',
    flexDirection: 'column',
    fontFamily: 'Arial',
    margin: '0px',
    padding: '0px',
    width: '100vw',
    height: '100vh',
    position: 'relative',
    overflow: 'scroll',
  };

  const header = {
    display: 'flex',
    margin: '0px',
    padding: '0px 20px 0px 20px',
    height: '80px',
    width: '100%',
    minWidth: '800px',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#ede7f6',
    fontSize: '18pt',
    opacity: '0.8',
  };

  const brandname = {
    wordWrap: 'break-word',
  }

  const username = {
    margin: '0px 35px 0px 0px',
  }

  const body = {
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    width: '100%',
    padding: '0px 20px 0px 20px',
  }

  return (
    <>
      <BrowserRouter style={page}>
        <header style={header}>
          { localStorage.getItem('token') && <nav><Link to="/dashboard" style={brandname}>Rotten Potatoes</Link></nav> }
          { localStorage.getItem('token') && <SearchByForm /> }
          { localStorage.getItem('token') && <SearchForm /> }
          { localStorage.getItem('token') && <SortByForm /> }
          { localStorage.getItem('token') && "|" }
          <nav>
            { localStorage.getItem('token') && localStorage.getItem('username') && <Link to={`/profile/${localStorage.getItem('username')}`} style={username}>{localStorage.getItem('username')}</Link> }
          </nav>
        </header>
        <div style={body}>
          <Routes>
            <Route path='/' element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/profile" element={<Error />} />
            <Route path="/profile/:username" element={<Profile />} />
            <Route path="/editprofile/:username" element={<EditProfile />} />
            <Route path="/profile:100" element={<Profile />} />
            <Route path="/forgetpassword" element={<ForgetPassword />} />
            <Route path="/movie/:movieId" element={<Movie />} />
            <Route path="/movie" element={<Error />} />
            <Route path="/search" element={<Search />} />
            <Route path="/*" element={<Error />} />
          </Routes>
        </div>
      </BrowserRouter>
    </>
  );
}


export default App;
