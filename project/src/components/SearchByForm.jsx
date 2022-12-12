import React from 'react';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

// dropdown list to let user to select serach by optioin
function SearchByForm () {
  const [searchBy, setSearchBy] = React.useState('');

  const handleChange = async(event) => {
    setSearchBy(event.target.value);
    localStorage.setItem('searchBy', event.target.value);
  };

  return (<>
      <FormControl required sx={{ m: 1, minWidth: 120 }}>
        <InputLabel id="demo-simple-select-helper-label">Search By</InputLabel>
        <Select
          labelId="search-by-label"
          id="search-by-form"
          value={searchBy}
          label="Search By"
          onChange={handleChange}
        >
          <MenuItem value={'Movie'}>Movie</MenuItem>
          <MenuItem value={'Director'}>Director</MenuItem>
          <MenuItem value={'Genre'}>Genre</MenuItem>
        </Select>
      </FormControl>
  </>
  );
}

export default SearchByForm;