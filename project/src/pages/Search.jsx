import React from 'react';
import { useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';

import { NormalText, PreviewText, PreviewText2, PreviewRating } from '../components/Style';
import image_not_exist from '../components/Image_not_available.png'

// search page
function Search () {
  const navigate = useNavigate();
  const [searchData, setSearchData] = React.useState([]);

  React.useEffect(() => {
    if (!localStorage.getItem('token')) {
      navigate('/login');
    }
  });

  React.useEffect(() => {
    fetchSearchResult();
  }, []);

  const searchPage = {
    display: 'flex',
    minWidth: '800px',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
  }

  const searchTitle = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    margin: '20px 0px 20px 0px',
  }

  const movieSection = {
    display: 'flex',
    width: '800px',
    height: '550px',
    borderRadius: '5px',
    flexWrap: 'wrap',
    overflow: 'scroll',
  }

  const moviePreview = {
    display: 'flex',
    flexDirection: 'column',
    position: 'relative',
    width: '150px',
    height: '220px',
    minHeight: '220px',
    margin: '0px 3px 20px 3px',
    backgroundColor: '#ede7f6',
    borderRadius: '5px',
    justifyContent: 'space-between',
  }

  const poster = {
    width: '150px',
    height: '170px',
    minHeight: '170px',
    backgroundColor: '#d1c4e9',
    borderRadius: '5px',
    objectFit: 'contain',
  }

  // API - submit request to get search result with input text
  const fetchSearchResult = async () => {
    let search = localStorage.getItem('searchBy');
    if (!search) {
      search = 'Movie';
    }
    let sort = localStorage.getItem('sortBy');
    if (!sort) {
      sort = 'Name ASC';
    }
    let searchInput = localStorage.getItem('searchInput');
    const username = localStorage.getItem('username');
    try {
      const response = await fetch('http://localhost:5000/search', {
        method: 'POST',
        headers: {
          'Content-type': 'application/json',
        },
        body: JSON.stringify({
          'searchOption': search,
          'keyword': searchInput,
          'sortOption': sort,
          'username': username,
        })
      });
      console.log(response);
      const data = await response.json();
      console.log(data);
      if (!response.ok) {
        alert(data.message);
      } else {
        setSearchData(data);
        localStorage.removeItem('searchInput');
      }
    } catch(error) {
      alert(error);
    }
  }

  return (<>
    <Box
      sx={{width: '100%', height: '100%'}}
      style={searchPage}
    >
      <NormalText style={searchTitle}>Search result:</NormalText>
      <Box style={movieSection} >
        {console.log(searchData)}
        {searchData.length > 0 && searchData.map((movie, index) => {
          return (
            <Box style={moviePreview} key={`search-${index}`}>
              <PreviewRating>{movie[7]}</PreviewRating>
              <Box>
                <img
                  style={poster}
                  src={movie[5] ? movie[5] : image_not_exist}
                  alt={`poster of ${movie[0]} not available`}
                  onError={({ currentTarget }) => {
                    currentTarget.onerror = null;
                    currentTarget.src=image_not_exist;
                  }}
                />
              </Box>
              <PreviewText onClick={() => navigate(`/movie/${movie[0]}`)}>Movie: {movie[1]}</PreviewText>
              <PreviewText2>Director: {movie[3]}</PreviewText2>
            </Box>
          )})
        }
      </Box>
    </Box>
  </>);
}

export default Search;