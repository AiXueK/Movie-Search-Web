import React from 'react';
import PropTypes from 'prop-types';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import { NormalText } from './Style';

// form to let user register a new account
function RegisterForm ({ submit }) {
  const [email, setEmail] = React.useState('');
  const [username, setUsername] = React.useState('');
  const [verificationCode, setVerificationCode] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [password2, setPassword2] = React.useState('');
  const [disabled, setDisabled] = React.useState(false);

  return (<>
    <Box
      component="form"
      sx={{
        '& > :not(style)': { m: 1, width: '300px' },
      }}
      noValidate
      autoComplete="off"
    >
      <NormalText>Email</NormalText>
      <br />
      <TextField
        sx={{ fontSize: 15 }}
        id="register-email"
        variant="outlined"
        type="text"
        onChange={event => setEmail(event.target.value)}
      />
      <br />
      <NormalText>User name</NormalText>
      <br />
      <TextField
        sx={{ fontSize: 15 }}
        id="register-name"
        variant="outlined"
        type="text"
        onChange={event => setUsername(event.target.value)}
      />
      <br />
      <NormalText>Verification Code</NormalText>
      <br />
      <TextField
        sx={{ fontSize: 15 }}
        id="register-code"
        variant="outlined"
        type="text"
        onChange={event => setVerificationCode(event.target.value)}
      />
      <Button variant='outlined' style={{width: '100px', height: '55px'}}  disabled={disabled} onClick={async () => {
        try {
          const response = await fetch('http://localhost:5000/api/register/otc', {
            method: 'POST',
            headers: {
              'Content-type': 'application/json',
            },
            body: JSON.stringify({
              'email': email,
            })
          });
          console.log(response);
          const data = await response.json();
          console.log(data);
          if (!response.ok) {
            alert(data.message);
          } else {
            setDisabled(true);
            alert('verification code sent');
            setTimeout(() => setDisabled(false), 15000);
          }
        } catch(error) {
          alert(error);
        }
      }}>
      Send</Button>
      <br />
      <NormalText>Password</NormalText>
      <br />
      <TextField
        sx={{ fontSize: 15 }}
        id="register-password"
        variant="outlined"
        type="password"
        onChange={event => setPassword(event.target.value)}
      />
      <br />
      <NormalText>Confirm Password</NormalText>
      <br />
      <TextField
        sx={{ fontSize: 15 }}
        id="register-password2"
        variant="outlined"
        type="password"
        onChange={event => setPassword2(event.target.value)}
      />
      <br />
      <Button variant='outlined' onClick={() => submit(email, username, verificationCode, password, password2)}>Register</Button>
    </Box>
  </>);
}

RegisterForm.propTypes = {
  submit: PropTypes.func,
};

export default RegisterForm;