import React from 'react';
import { useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';

import { Title } from '../components/Style';
import EditProfileForm from '../components/EditProfileForm';

// edit profile page
function EditProfile () {
  const navigate = useNavigate();
  React.useEffect(() => {
    if (!localStorage.getItem('token')) {
      navigate('/login');
    }
  });

  const refreshPage = () => {
    window.location.reload(false);
  }

  return (<>
    <Box
      sx={{ m: 2 }}
    >
      <Title style={{margin: '10px'}} >Edit Profile</Title>
      <EditProfileForm submit={async (oldPassword, password, password2) => {
        // API - submit request to edit profile information
        try {
          const token = localStorage.getItem('token');
          const username = localStorage.getItem('username');
          const response = await fetch('http://localhost:5000/api/updateprofile', {
            method: 'POST',
            headers: {
              'Content-type': 'application/json',
            },
            body: JSON.stringify({
              'token': token,
              'oldPassword': oldPassword,
              'newPassword': password,
              'confirmedPassword': password2,
            })
          });
          console.log(response);
          const data = await response.json();
          console.log(data);
          if (!response.ok) {
            alert(data.message);
          } else {
            alert(data.message);
            navigate(`/profile/${username}`);
            refreshPage();
          }
        } catch(error) {
          alert(error);
        }
      }} />
    </Box>
  </>);
}

export default EditProfile;