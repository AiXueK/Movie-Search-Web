import React from 'react';
import { useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';

import { Title } from '../components/Style';
import ForgetPasswordForm from '../components/ForgetPasswordForm';

// forget password page
function Forgetpassword () {
  const navigate = useNavigate();

  const toLogin = () => {
    navigate('/login');
  };

  return (<>
    <Box
      sx={{ m: 2 }}
    >
      <Title style={{margin: '10px'}} >Forgot your password?</Title>
      <ForgetPasswordForm submit={async (email, verificationCode, password, password2) => {
        // API - submit request to forgot password and change a new password
        try {
          const response = await fetch('http://localhost:5000/api/forgetpassword', {
            method: 'POST',
            headers: {
              'Content-type': 'application/json',
            },
            body: JSON.stringify({
              email,
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
            alert(data.message);
            navigate('/dashboard');
          }
        } catch(error) {
          alert(error);
        }
      }} />
      <Button variant="outlined" style={{width: '300px', margin: '10px'}} onClick={() => toLogin()}>Back to login page</Button>
    </Box>
  </>);
}

export default Forgetpassword;