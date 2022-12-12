import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton'
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import FavoriteIcon from '@mui/icons-material/Favorite';
import StarBorderIcon from '@mui/icons-material/StarBorder';
import StarIcon from '@mui/icons-material/Star';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import SentimentSatisfiedAltIcon from '@mui/icons-material/SentimentSatisfiedAlt';
import SentimentNeutralIcon from '@mui/icons-material/SentimentNeutral';
import SentimentVeryDissatisfiedIcon from '@mui/icons-material/SentimentVeryDissatisfied';

import image_not_exist from '../components/Image_not_available.png'
import { MoviePageText, MovieDescriptionText, Title, Title3, PreviewRating, PreviewText, PreviewText2 } from '../components/Style';

// movie information page
function Movie () {
  const params = useParams();
  const [clicked, setClicked] = React.useState(false);
  const [clicked1, setClicked1] = React.useState(false);
  const [clicked2, setClicked2] = React.useState(false);
  const [clicked3, setClicked3] = React.useState(false);
  const [clicked4, setClicked4] = React.useState(false);
  const [clicked5, setClicked5] = React.useState(false);
  const [fetchedRating, setFetchedRating] = React.useState('');
  const [review, setReview] = React.useState('');
  const [reviewData, setReviewData] = React.useState([]);
  const textInput = React.useRef(null);
  const [movieData, setMovieData] = React.useState([]);
  const [suggestionData, setSuggestionData] = React.useState([]);

  const navigate = useNavigate();
  React.useEffect(() => {
    if (!localStorage.getItem('token')) {
      navigate('/login');
    }
  });

  React.useEffect(() => {
    fetchMovieInfo();
    fetchWishlistStatus();
    fetchRating();
    fetchReview();
    fetchSuggestion();
    fetchUserRating();
    // eslint-disable-next-line
  }, []);

  const toProfilePage = (username) => {
    navigate(`/profile/${username}`);
  }

  const refreshPage = () => {
    window.location.reload(false);
  }

  const moviePage = {
    display: 'flex',
    width: '100%',
    paddingRight: '20px',
  }

  const infoSection = {
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    width: '77%',
    paddingRight: '20px',
  }

  const detailSection = {
    display: 'flex',
  }

  const posterSection = {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    width: '160px',
  }

  const ratingSection = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '10px 0px 0px 0px',
  }

  const movieDetailSection = {
    display: 'flex',
    flexDirection: 'column',
    width: '100%',
    padding: '0px 0px 10px 20px',
  }

  const descriptionSection = {
    maxHeight: '100px',
    overflow: 'auto',
    margin: '0px 0px 10px 0px',
  }

  const reviewSection = {
    display: 'flex',
    flexDirection: 'column',
    width: '100%',
    height: '100vh',
  }

  const suggestionSection = {
    display: 'flex',
    flexDirection: 'column',
    height: '100vh',
    width:'160px',
    padding: '0px 0px 0px 5px',
  }

  const poster = {
    width: '150px',
    height: '190px',
    minHeight: '190px',
    borderRadius: '5px',
    objectFit: 'contain',
  }

  const writeReview = {
    display: 'flex',
    flexDirection: 'column',
    width: '100%',
    height: '130px',
    marginTop: '20px',
    padding: '0px 10px 0px 10px',
  }

  const writeRating = {
    display: 'flex',
  }

  const reviewInput = {
    width: '100%',
    margin: '5px 0px 5px 0px',
  }

  const submitBtn = {
    width: '100px',
    height: '30px',
    alignSelf: 'flex-end',
  }

  const displayReview = {
    width: '100%',
  }

  const reviewPreview = {
    display: 'flex',
    flexDirection: 'column',
    width: '100%',
    border: 'solid',
    borderRadius: '5px',
    borderColor: '#ede7f6',
    margin: '10px 0px 10px 0px',
    padding: '5px 5px 0px 5px',
  }

  const reviewHeader = {
    display: 'flex',
    width: '100%',
    margin: '0px 0px 5px 0px',
  }

  const reviewer = {
    color: '#7e57c2',
    margin: '0px 10px 0px 0px',
    maxWidth: '200px',
    wordWrap: 'nowrap',
    whiteSpace: 'nowrap',
    textOverflow: 'ellipsis',
    overflow: 'hidden',
  }

  const headerComponent = {
    margin: '0px 10px 0px 0px',
  }

  const reviewRating = {
    display: 'flex',
    margin: '0px 0px 5px 0px',
    height: '10px',
  }

  const reviewText = {
    width: '100%',
  }

  const moviePreview = {
    display: 'flex',
    flexDirection: 'column',
    position: 'relative',
    width: '150px',
    height: '220px',
    margin: '10px 0px 10px 0px',
    paddingBottom: '3px',
    backgroundColor: '#ede7f6',
    borderRadius: '5px',
    justifyContent: 'space-between',
  }

  const posterPreview = {
    width: '150px',
    height: '170px',
    minHeight: '170px',
    backgroundColor: '#d1c4e9',
    borderRadius: '5px',
    objectFit: 'contain',
  }

  // API - automatically fetch movie information to display on movie page
  const fetchMovieInfo = async () => {
    const movieId = params.movieId;
    const detail = await fetch(`http://localhost:5000/movieinfo`, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
        movieId,
      })
    });
    const movieInfo = await detail.json();
    console.log(movieInfo);
    if (!detail.ok) {
      alert(movieInfo.message);
    } else {
      setMovieData(movieInfo[0]);
    }
  }

  // API - automatically fetch wishlist status of a user on this movie to display on movie page
  const fetchWishlistStatus = async () => {
    const movieId = params.movieId;
    const username = localStorage.getItem('username');
    const detail = await fetch(`http://localhost:5000/movie/checkwishlist`, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
        username,
        movieId,
      })
    });
    const status = await detail.json();
    console.log(status);
    if (!detail.ok) {
      alert(status.message);
    } else {
      setClicked(status);
    }
  }

  // API - add a movie to wishlist
  const addWishlist = async () => {
    const movieId = params.movieId;
    const username = localStorage.getItem('username');
    const detail = await fetch(`http://localhost:5000/movie/addwishlist`, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
        movieId,
        username,
      })
    });
    const response = await detail.json();
    console.log(response);
    if (!detail.ok) {
      alert(response.message);
    } else {
      alert(response.message);
      setClicked(true);
    }
  }

  // API - automatically fetch movie rating to display on movie page
  const fetchRating = async () => {
    const movieId = params.movieId;
    const username = localStorage.getItem('username');
    const detail = await fetch(`http://localhost:5000/getrating`, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
        username,
        movieId,
      })
    });
    const response = await detail.json();
    console.log("getRating")
    console.log(response);
    if (!detail.ok) {
      alert(response.message);
    } else {
      setFetchedRating(response);
    }
  }

  // API - automatically fetch login user rating about this movie to display on movie page
  const fetchUserRating = async () => {
    const movieId = params.movieId;
    const username = localStorage.getItem('username');
    const detail = await fetch(`http://localhost:5000/getuserrating`, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
        username,
        movieId,
      })
    });
    const response = await detail.json();
    console.log(response);
    if (!detail.ok) {
      alert(response.message);
    } else {
      switch (response) {
        case 1:
          setClicked1(true);
          break;
        case 2:
          setClicked2(true);
          break;
        case 3:
          setClicked3(true);
          break;
        case 4:
          setClicked4(true);
          break;
        case 5:
          setClicked5(true);
          break;
        default:
          break;
      }
    }
  }

  // API - add a rating about the movie
  const addRating = async (rating) => {
    const movieId = params.movieId;
    const username = localStorage.getItem('username');
    const detail = await fetch(`http://localhost:5000/addrating`, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
        username,
        movieId,
        rating,
      })
    });
    const response = await detail.json();
    console.log(response);
    if (!detail.ok) {
      alert(response.message);
    } else {
      alert(response.message);
      switch (rating) {
        case 1:
          setClicked1(true);
          break;
        case 2:
          setClicked2(true);
          break;
        case 3:
          setClicked3(true);
          break;
        case 4:
          setClicked4(true);
          break;
        case 5:
          setClicked5(true);
          break;
        default:
          break;
      }
    }
  }

  // API - add a review about the movie
  const addReview = async (review) => {
    const movieId = params.movieId;
    const username = localStorage.getItem('username');
    const detail = await fetch(`http://localhost:5000/addreview`, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
        'username': username,
        'movieId': movieId,
        'content': review,
      })
    });
    const response = await detail.json();
    console.log(response);
    if (!detail.ok) {
      alert(response.message);
      textInput.current.value = '';
    } else {
      alert(response.message);
      textInput.current.value = '';
      refreshPage();
    }
  }

  // API - automatically fetch list of reviews on the movie to display on movie page
  const fetchReview = async () => {
    const movieId = params.movieId;
    const username = localStorage.getItem('username');
    const detail = await fetch(`http://localhost:5000/getmoviereview`, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
        movieId,
        username,
      })
    });
    const reviews = await detail.json();
    console.log(reviews);
    if (!detail.ok) {
      alert(reviews.message);
    } else {
      setReviewData(reviews);
    }
  }

  // API - automatically fetch suggestion list about the movie to display on movie page
  const fetchSuggestion = async () => {
    const movieId = params.movieId;
    const username = localStorage.getItem('username');
    const detail = await fetch(`http://localhost:5000/suggestion`, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
        movieId,
        username,
      })
    });
    const suggestions = await detail.json();
    console.log(suggestions);
    if (!detail.ok) {
      alert(suggestions.message);
    } else {
      setSuggestionData(suggestions);
    }
  }

  const toMovie = (movieId) => {
    navigate(`/movie/${movieId}`);
    refreshPage();
  }

  return (<>
    <Box
     style={moviePage}
    >
      <Box style={infoSection}>
        <Box style={detailSection}>
          <Box style={posterSection}>
            <img style={poster} src={movieData[5]} alt={`poster of ${movieData[0]} not available`}/>
            <Box style={ratingSection}>
              <MoviePageText>Rating: {fetchedRating}</MoviePageText>
              <IconButton 
                onClick={() => addWishlist()} 
                fontSize="large" 
                sx={{color: 'red', width: '50px'}}
              >
                { clicked ? <FavoriteIcon /> : <FavoriteBorderIcon />}
              </IconButton>
            </Box>
          </Box>
          <Box style={movieDetailSection}>
            <Title>{movieData[1]}</Title>
            <Box style={descriptionSection}>
              <MovieDescriptionText>{movieData[6]}</MovieDescriptionText>
            </Box>
            <MoviePageText>Director Name: {movieData[3]}</MoviePageText>
            <MoviePageText>Cast Name: {movieData[4]}</MoviePageText>
            <MoviePageText>Genre: {movieData[2]}</MoviePageText>
          </Box>
        </Box>
        <Box style={reviewSection}>
          <Box style={writeReview}>
            <Box style={writeRating}>
              <IconButton
                onClick={() => addRating(1)}
                fontSize="small"
                sx={{color: '#fdd835', p: '0'}}
              >
                { (clicked1 || clicked2 || clicked3 || clicked4 || clicked5 ) ? <StarIcon /> : <StarBorderIcon /> }
              </IconButton>
              <IconButton
                onClick={() => addRating(2)}
                fontSize="small"
                sx={{color: '#fdd835', p: '0'}}
              >
                { (clicked2 || clicked3 || clicked4 || clicked5 ) ? <StarIcon /> : <StarBorderIcon /> }
              </IconButton>
              <IconButton
                onClick={() => addRating(3)}
                fontSize="small"
                sx={{color: '#fdd835', p: '0'}}
              >
                { (clicked3 || clicked4 || clicked5 ) ? <StarIcon /> : <StarBorderIcon /> }
              </IconButton>
              <IconButton
                onClick={() => addRating(4)}
                fontSize="small"
                sx={{color: '#fdd835', p: '0'}}
              >
                { (clicked4 || clicked5 ) ? <StarIcon /> : <StarBorderIcon /> }
              </IconButton>
              <IconButton
                onClick={() => addRating(5)}
                fontSize="small"
                sx={{color: '#fdd835', p: '0'}}
              >
                { (clicked5 ) ? <StarIcon /> : <StarBorderIcon /> }
              </IconButton>
            </Box>
            <TextField
              style={reviewInput}
              id="add-review"
              variant="outlined"
              type="text"
              placeholder="Write a comment here"
              inputRef={textInput}
              onChange={event => setReview(event.target.value)}
            />
            <Button style={submitBtn} variant='outlined' onClick={() => addReview(review)}>Submit</Button>
          </Box>
          <Box style={displayReview}>
            { reviewData.length === 0 && <MoviePageText>No review found.</MoviePageText> }
            { reviewData.length > 0 && reviewData.map((review, index) => {
                return (
                  <Box style={reviewPreview} key={`movie-review-${index}`}>
                    <Box style={reviewHeader}>
                      <span style={reviewer} onClick={() => toProfilePage(review.username)}>{review.username}</span>
                      { review.sentimentAnalysis === 1 && <SentimentSatisfiedAltIcon style={headerComponent} /> }
                      { review.sentimentAnalysis === 0 && <SentimentNeutralIcon style={headerComponent} /> }
                      { review.sentimentAnalysis === -1 && <SentimentVeryDissatisfiedIcon style={headerComponent} /> }
                      { review.spam && <span style={headerComponent}>Likely spam!</span> }
                    </Box>
                    <Box style={reviewRating}>
                      { review.rating >= 1 ? <StarIcon sx={{color: '#fdd835'}} /> : <StarBorderIcon sx={{color: '#fdd835'}} /> }
                      { review.rating >= 2 ? <StarIcon sx={{color: '#fdd835'}} /> : <StarBorderIcon sx={{color: '#fdd835'}} /> }
                      { review.rating >= 3 ? <StarIcon sx={{color: '#fdd835'}} /> : <StarBorderIcon sx={{color: '#fdd835'}} /> }
                      { review.rating >= 4 ? <StarIcon sx={{color: '#fdd835'}} /> : <StarBorderIcon sx={{color: '#fdd835'}} /> }
                      { review.rating >= 5 ? <StarIcon sx={{color: '#fdd835'}} /> : <StarBorderIcon sx={{color: '#fdd835'}} /> }
                    </Box>
                    <p style={reviewText}>
                      {review.content}
                    </p>
                  </Box>
                )})
            }
          </Box>
        </Box>
      </Box>
      <Box style={suggestionSection}>
        <Title3>Suggestions</Title3>
        {suggestionData.length === 0 && <MoviePageText>No movie suggested.</MoviePageText>}
        {suggestionData.length > 0 && suggestionData.map((movie, index) => {
          return (
            <Box style={moviePreview} key={`suggestion-${index}`}>
              <PreviewRating>{movie[7]}</PreviewRating>
              <Box>
                <img
                  style={posterPreview}
                  src={movie[5] ? movie[5] : image_not_exist}
                  alt={`poster of ${movie[0]} not available`}
                  onError={({ currentTarget }) => {
                    currentTarget.onerror = null;
                    currentTarget.src=image_not_exist;
                  }}
                />
              </Box>
              <PreviewText onClick={() => toMovie(movie[0])}>Movie: {movie[1]}</PreviewText>
              <PreviewText2>Director: {movie[3]}</PreviewText2>
            </Box>
          )})
        }
      </Box>
    </Box>
  </>);
}

export default Movie;