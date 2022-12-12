import React from 'react';
import { useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';

import { Title } from '../components/Style';
import LoginForm from '../components/LoginForm';

// login page
function Login () {
  const navigate = useNavigate();

  const toRegister = () => {
    navigate('/register');
  };
  const toForgotPassword = () => {
    navigate('/forgetpassword');
  }

  const refreshPage = () => {
    window.location.reload(false);
  }

  return (<>
    <Box
      sx={{ m: 2 }}
    >
      <Button variant="outlined" style={{width: '300px', margin: '10px'}} onClick={() => toRegister()}>{'-> Register'}</Button>
      <Title style={{margin: '10px'}} >Login</Title>
      <LoginForm submit={async (email, password) => {
        // API - submit request to login to an account
        try {
          const response = await fetch('http://localhost:5000/api/auth', {
            method: 'POST',
            headers: {
              'Content-type': 'application/json',
            },
            body: JSON.stringify({
              email,
              password,
            })
          });
          console.log(response);
          const data = await response.json();
          console.log(data);
          if (!response.ok) {
            alert(data.message);
          } else {
            localStorage.setItem('email', email)
            localStorage.setItem('username', data.username);
            localStorage.setItem('token', data.token);
            navigate('/dashboard');
            refreshPage();
          }
        } catch(error) {
          alert(error);
        }
      }} />
      <Button variant="outlined" style={{width: '300px', margin: '10px'}} onClick={() => toForgotPassword()}>Forgot password?</Button>
    </Box>
  </>);
}

export default Login;