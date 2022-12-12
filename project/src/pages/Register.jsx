import React from 'react';
import { useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';

import { Title } from '../components/Style';
import RegisterForm from '../components/RegisterForm';

// register page
function Register () {
  const navigate = useNavigate();
  const toLogin = () => {
    navigate('/login');
  };
  
  const refreshPage = () => {
    window.location.reload(false);
  }

  return (<>
    <Box
      sx={{ m: 2 }}
    >
      <Button variant="outlined" style={{width: '300px', margin: '10px'}} onClick={() => toLogin()}>{'-> Login'}</Button>
      <Title style={{margin: '10px'}} >Register</Title>
      <RegisterForm submit={async (email, username, verificationCode, password, password2) => {
        // API - submit request to register a new user on register page
        try {
          const response = await fetch('http://localhost:5000/api/register', {
            method: 'POST',
            headers: {
              'Content-type': 'application/json',
            },
            body: JSON.stringify({
              email,
              username,
              verificationCode,
              password,
              password2,
            })
          });
          console.log(response);
          const data = await response.json();
          console.log(data);
          if (!response.ok) {
            alert(data.message);
          } else {
            localStorage.setItem('email', email);
            localStorage.setItem('username', username);
            localStorage.setItem('token', data.token);
            navigate('/dashboard');
            refreshPage();
          }
        } catch(error) {
          alert(error);
        }
      }} />
    </Box>
  </>);
}

export default Register;