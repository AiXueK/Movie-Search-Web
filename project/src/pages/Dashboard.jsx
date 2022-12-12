import React from 'react';
import { useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';

import { NormalText, PreviewText, PreviewText2, PreviewRating } from '../components/Style';
import image_not_exist from '../components/Image_not_available.png'

// dashboard page
function Dashboard () {
  const navigate = useNavigate();
  const [dashboardData, setDashboardData] = React.useState([]);

  React.useEffect(() => {
    if (!localStorage.getItem('token')) {
      navigate('/login');
    }
  });

  React.useEffect(() => {
    fetchMovieList();
  }, []);

  const dashboardPage = {
    display: 'flex',
    minWidth: '800px',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
  }

  const dashboardTitle = {
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
    justifyContent: 'space-between',
    overflow: 'scroll',
  }

  const moviePreview = {
    display: 'flex',
    flexDirection: 'column',
    position: 'relative',
    width: '150px',
    height: '220px',
    paddingBottom: '3px',
    backgroundColor: '#ede7f6',
    borderRadius: '5px',
    justifyContent: 'space-between',
    overflow: 'hidden',
  }

  const poster = {
    width: '150px',
    height: '170px',
    minHeight: '170px',
    backgroundColor: '#d1c4e9',
    borderRadius: '5px',
    objectFit: 'contain',
  }

  // API - automatically fetch top 10 ranked movie to display on dashboard
  const fetchMovieList = async () => {
    const token = localStorage.getItem('token');
    const username = localStorage.getItem('username');
    const detail = await fetch(`http://localhost:5000/home`, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
        token,
        username,
      })
    });
    const movieLists = await detail.json();
    console.log(movieLists);
    if (!detail.ok) {
      alert(movieLists.message);
    } else {
      setDashboardData(movieLists);
    }
  }

  return (<>
    <Box
      sx={{width: '100%', height: '100%'}}
      style={dashboardPage}
    >
      <NormalText style={dashboardTitle}>Top 10 Movies Across All Genre</NormalText>
      <Box style={movieSection}>
        {console.log(dashboardData)}
        {dashboardData.length > 0 && dashboardData.map((movie, index) => {
          return (
            <Box style={moviePreview} key={`dashboard-${index}`}>
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

export default Dashboard;