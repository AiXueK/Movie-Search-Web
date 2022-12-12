import React from 'react';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

// dropdown list to let user choose a sort by option
function SortByForm() {
  const [sortBy, setSortBy] = React.useState('');

  const handleChange = (event) => {
    setSortBy(event.target.value);
    localStorage.setItem('sortBy', event.target.value);
  };

  return (<>
      <FormControl required sx={{ m: 1, minWidth: 100 }}>
        <InputLabel id="demo-simple-select-helper-label">Sort By</InputLabel>
        <Select
          labelId="search-by-label"
          id="search-by-form"
          value={sortBy}
          label="Sort By"
          onChange={handleChange}
          defaultValue="Name ASC"
        >
          <MenuItem value={'Name ASC'}>Name ASC</MenuItem>
          <MenuItem value={'Name DESC'}>Name DESC</MenuItem>
          <MenuItem value={'Rating ASC'}>Rating ASC</MenuItem>
          <MenuItem value={'Rating DESC'}>Rating DESC</MenuItem>
        </Select>
      </FormControl>
    </>
  );
}

export default SortByForm;