import React from 'react';
import { useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';

import { Title, NormalText } from '../components/Style';

// error page, page not found
function Error () {
  const navigate = useNavigate();
  const toDashboard = () => {
    navigate('/dashboard');
  };

  return (<>
    <Box
      sx={{ m: 2 }}
    >
      <Title>Error</Title>
      <NormalText>Something went wrong, page not exist</NormalText>
      <br /><br /><br />
      <Button variant="outlined" onClick={() => toDashboard()}>Dashboard</Button>
    </Box>
  </>);
}

export default Error;