import React from 'react';
import PropTypes from 'prop-types';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';

import { NormalText } from './Style';

// form to let user login to account
function LoginForm ({ submit }) {
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');

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
        id="login-email"
        variant="outlined"
        type="text"
        onChange={event => setEmail(event.target.value)}
      />
      <br />
      <NormalText>Password</NormalText>
      <br />
      <TextField
        sx={{ fontSize: 15 }}
        id="login-password"
        variant="outlined"
        type="password"
        onChange={event => setPassword(event.target.value)}
      />
      <br />
      <Button variant='outlined' onClick={() => submit(email, password)}>Login</Button>
    </Box>
  </>);
}

LoginForm.propTypes = {
  submit: PropTypes.func,
};

export default LoginForm;