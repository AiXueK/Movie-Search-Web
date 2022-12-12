import React from 'react';
import PropTypes from 'prop-types';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import { NormalText } from './Style';
import { useParams, useNavigate } from 'react-router-dom';

// form to let user edit profile
function EditProfileForm ({ submit }) {
  const navigate = useNavigate();
  const params = useParams();
  const [oldPassword, setOldPassword] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [password2, setPassword2] = React.useState('');

  const toProfile = () => {
    navigate(`/profile/${params.username}`);
  };

  return (<>
    <Box
      component="form"
      sx={{
        '& > :not(style)': { m: 1, width: '300px' },
      }}
      noValidate
      autoComplete="off"
    >
      <NormalText>Old Password</NormalText>
      <br />
      <TextField
        sx={{ fontSize: 15 }}
        id="edit-old-password"
        variant="outlined"
        type="password"
        onChange={event => setOldPassword(event.target.value)}
      />
      <br />
      <NormalText>New Password</NormalText>
      <br />
      <TextField
        sx={{ fontSize: 15 }}
        id="edit-new-password"
        variant="outlined"
        type="password"
        onChange={event => setPassword(event.target.value)}
      />
      <br />
      <NormalText>Confirm Password</NormalText>
      <br />
      <TextField
        sx={{ fontSize: 15 }}
        id="edit-new-password2"
        variant="outlined"
        type="password"
        onChange={event => setPassword2(event.target.value)}
      />
      <br />
      <Button variant='outlined' onClick={() => submit(oldPassword, password, password2)}>Confirm</Button>
      <br />
      <Button variant='outlined' onClick={() => toProfile()}>Cancel</Button>
    </Box>
  </>);
}

EditProfileForm.propTypes = {
  submit: PropTypes.func,
};

export default EditProfileForm;