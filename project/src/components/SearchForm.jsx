import React from 'react';
import { useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import SearchIcon from '@mui/icons-material/Search';

// form to let user to search movie with input text
function SearchForm () {
  const navigate = useNavigate();
  const [searchInput, setSearchInput] = React.useState('');

  const refreshPage = () => {
    window.location.reload(false);
  }

  const alignCenter = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  }

  const getSearchInput = () => {
    localStorage.setItem('searchInput', searchInput);
    console.log(localStorage.getItem('searchInput'));
    if (window.location.href === 'http://localhost:3000/search') {
      refreshPage();
    }
    navigate('/search');
  }

  return (<>
    <Box
      component="form"
      noValidate
      autoComplete="off"
      alignItems="center"
      justify="center"
      style={alignCenter}
    >
      <TextField
        sx={{ fontSize: 15, width: '300px' }}
        id="search-input"
        variant="outlined"
        type="text"
        inputProps={{ maxLength: 40 }}
        onChange={event => setSearchInput(event.target.value)}
      />
      <SearchIcon 
        onClick={() => getSearchInput()} 
        color="secondary" 
        fontSize="large" 
        sx={{width: '50px'}}
      />
    </Box>
  </>);
}

export default SearchForm;