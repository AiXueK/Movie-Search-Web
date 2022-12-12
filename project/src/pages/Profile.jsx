import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import { EmailText, UsernameText } from '../components/Style';
import { NormalText, PreviewText, PreviewText2, PreviewRating } from '../components/Style';
import FavoriteIcon from '@mui/icons-material/Favorite';
import CloseIcon from '@mui/icons-material/Close';

import { Title3 } from '../components/Style';

// profile page
function Profile() {
  const navigate = useNavigate();
  const params = useParams();
  const [reviewData, setReviewData] = React.useState([]);
  const [wishlistData, setWishlistData] = React.useState([]);
  const [banlistData, setBanlistData] = React.useState([]);
  const [disabled, setDisabled] = React.useState(false);

  React.useEffect(() => {
    if (!localStorage.getItem('token')) {
      navigate('/login');
    }
  });

  React.useEffect(() => {
    checkBanlist();
    fetchReview();
    fetchWishlist();
    fetchBanlist();
    // eslint-disable-next-line
  }, []);

  const refreshPage = () => {
    window.location.reload(false);
  }

  const toEditProfile = () => {
    const username = localStorage.getItem('username');
    navigate(`/editprofile/${username}`);
  }

  const toMoviePage = (movieId) => {
    navigate(`/movie/${movieId}`);
  }

  const toProfile = (username) => {
    navigate(`/profile/${username}`);
  }

  const movieSection = {
    display: 'flex',
    width: '800px',
    height: '275px',
    borderRadius: '5px',
    flexWrap: 'nowrap',
    justifyContent: 'flex-start',
    overflow: 'auto',
  }

  const reviewSection = {
    display: 'flex',
    width: '800px',
    height: '100px',
    flexWrap: 'nowrap',
    justifyContent: 'flex-start',
    overflow: 'auto',
  }

  const banlistSection = {
    display: 'flex',
    width: '800px',
    height: '50px',
    borderRadius: '5px',
    flexWrap: 'nowrap',
    justifyContent: 'flex-start',
    overflow: 'auto',
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
  }

  const poster = {
    width: '150px',
    height: '170px',
    backgroundColor: '#d1c4e9',
    borderRadius: '5px',
    objectFit: 'contain',
  }

  const userDetails = {
    display: 'flex',
    height: '70px',
    padding: '0px 20px 0px 0px',
    justifyContent: 'space-between',
  }

  const userInformation = {
    display: 'flex',
    alignItems: 'flex-end',
    justifyContent: 'center',
    padding: '5px 0px 5px 0px',
  }

  const name = {
    height: '100%',
    padding: '0px',
    maxWidth: '600px',
    wordWrap: 'nowrap',
    whiteSpace: 'nowrap',
    textOverflow: 'ellipsis',
    overflow: 'hidden',
    alignSelf: 'center',
    justifySelf: 'center',
  }

  const profileButtons = {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
  }

  const profilePage = {
    width: '100%',
    minWidth: '800px',
  }
  
  const likeIcon = {
    position: 'absolute',
    color: 'red',
  }

  const reviewPreview = {
    display: 'flex',
    position: 'relative',
    flexDirection: 'column',
    width: '156px',
    padding: '0px 3px 0px 3px',
    height: '100%',
    borderRadius: '3px',
    backgroundColor: '#ede7f6',
    margin: '0px 20px 0px 0px',
  }

  const closeReviewBtn = {
    position: 'absolute',
    left: '138px',
  }

  const reviewTitle = {
    width: '140px',
    height: '30%',
    fontSize: '17px',
    padding: '0px',
    margin: '0px',
    wordWrap: 'nowrap',
    whiteSpace: 'nowrap',
    textOverflow: 'ellipsis',
    overflow: 'hidden',
    color: '#673ab7',
  }

  const reviewContent = {
    width: '156px',
    height: '70%',
    fontSize: '10px',
    wordWrap: 'break-word',
    textOverflow: 'ellipsis',
    overflow: 'hidden',
  }

  const banlistPreview = {
    display: 'flex',
    position: 'relative',
    flexDirection: 'column',
    width: '160px',
    padding: '3px 3px 0px 3px',
    height: '30px',
    borderRadius: '3px',
    backgroundColor: '#ede7f6',
    margin: '0px 20px 0px 0px',
  }

  const banlistContent = {
    width: '130px',
    fontSize: '18px',
    padding: '0px',
    margin: '0px',
    wordWrap: 'nowrap',
    whiteSpace: 'nowrap',
    textOverflow: 'ellipsis',
    overflow: 'hidden',
  }

  const banlistLayout = {
    width: '150px',
  }

  const closeBanlistBtn = {
    position: 'absolute',
    left: '130px',
  }

  // API - automatically fetch this user is already been added to login user's banlist
  const checkBanlist = async () => {
    const username = localStorage.getItem('username');
    const banuser = params.username;
    const detail = await fetch(`http://localhost:5000/banlist/check`, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
        'username': username,
        'ban_name': banuser,
      })
    });
    const response = await detail.json();
    console.log(response);
    if (!detail.ok) {
      alert(response.message);
    } else {
      setDisabled(response);
    }
  }

  // API - add a user to login user's banlist
  const addToBanlist = async () => {
    const username = localStorage.getItem('username');
    const banuser = params.username;
    const detail = await fetch(`http://localhost:5000/banlist/add`, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
        'username': username,
        'ban_name': banuser,
      })
    });
    const response = await detail.json();
    console.log(response);
    if (!detail.ok) {
      alert(response.message);
    } else {
      setDisabled(true);
      alert(response.message);
    }
  }

  // API - automatically fetch review information to display on profile page
  const fetchReview = async () => {
    const username = params.username;
    const detail = await fetch(`http://localhost:5000/getusereview`, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
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

  // API - delete review from review history display on login user's profile page
  const deleteReview = async(movieId, reviewId) => {
    const username = params.username;
    const detail = await fetch(`http://localhost:5000/deletereview`, {
      method: 'DELETE',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
        username,
        movieId,
        reviewId,
      })
    });
    const response = await detail.json();
    console.log(response);
    if (!detail.ok) {
      alert(response.message);
    } else {
      alert(response.message);
      fetchReview();
    }
  }

  // API - automatically fetch wishlist to display on profile page
  const fetchWishlist = async () => {
    const username = params.username;
    const detail = await fetch(`http://localhost:5000/wishlistinfo`, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
        username,
      })
    });
    const wishlist = await detail.json();
    console.log(wishlist);
    if (!detail.ok) {
      alert(wishlist.message);
    } else {
      setWishlistData(wishlist);
    }
  }

  // API - remove a movie from wishlist on login user's profile page
  const removeWishlist = async (movieId) => {
    const username = localStorage.getItem('username');
    const detail = await fetch(`http://localhost:5000/wishlist/removewishlist`, {
      method: 'DELETE',
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
      alert(response.message);
      fetchWishlist();
    }
  }

  // API - automatically fetch banlist information to display on profile page
  const fetchBanlist = async () => {
    const username = localStorage.getItem('username');
    const detail = await fetch(`http://localhost:5000/banlist/info`, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
        username,
      })
    });
    const banlist = await detail.json();
    console.log(banlist);
    if (!detail.ok) {
      alert(banlist.message);
    } else {
      setBanlistData(banlist);
    }
  }

  // API - delete a user from login user's profile page
  const deleteBanUser = async (banUser) => {
    const username = localStorage.getItem('username');
    const detail = await fetch(`http://localhost:5000/banlist/remove`, {
      method: 'DELETE',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
        'username': username,
        'ban_name': banUser,
      })
    });
    const response = await detail.json();
    console.log(response);
    if (!detail.ok) {
      alert(response.message);
    } else {
      alert(response.message);
      fetchBanlist();
    }
  }

  // API - logout the login user
  const logout = async () => {
    const token = localStorage.getItem('token');
    const detail = await fetch(`http://localhost:5000/api/logout`, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
        token
      })
    });
    const response = await detail.json();
    console.log(response);
    if (!detail.ok) {
      alert(response.message);
    } else {
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      localStorage.removeItem('email');
      navigate('/login');
      refreshPage();
      alert(response.message);
    }
  }

  return (<>
    <Box style={profilePage}>
      <Box style={userDetails}>
        <Box style={userInformation}>
          <UsernameText style={name}>{params.username}</UsernameText>
          {localStorage.getItem('username') === params.username && <EmailText>{localStorage.getItem('email')}</EmailText>}
        </Box>
        <Box style={profileButtons}>
          { localStorage.getItem('username') === params.username && 
            <Button
              sx={{ fontSize: 14, minWidth:"120px"}}
              size="small"
              variant="outlined"
              onClick={() => logout()}
            >
              Logout
            </Button> 
          }
          { localStorage.getItem('username') !== params.username && 
            <Button
              sx={{ fontSize: 14, minWidth:"120px"}}
              size="small"
              variant="outlined"
              disabled={disabled}
              onClick={() => addToBanlist()}
            >
              Add to Banlist
            </Button> 
          }
          { localStorage.getItem('username') === params.username && 
            <Button
              sx={{ fontSize: 14, alignContent:"center" }} 
              size="small"
              variant="outlined"
              onClick={() => toEditProfile()}
            >
              Edit Profile
            </Button> 
          }
        </Box>
      </Box>
      <Title3>Review History</Title3>
      <Box style={reviewSection}>
        { reviewData.length === 0 && <NormalText>No review found.</NormalText> }
        { reviewData.length > 0 && reviewData.map((review, index) => {
          return (
            <Box style={reviewPreview} key={`review-${index}`}>
              { localStorage.getItem('username') === params.username &&  
                <CloseIcon style={closeReviewBtn} onClick={() => deleteReview(review.movieId, review.reviewId)}/>
              }
              <p style={reviewTitle} onClick={() => toMoviePage(review.movieId)}>
                {review.movieName}
              </p>
              <span style={reviewContent}>{review.content}</span>
            </Box>
          )
        })}
      </Box>
      <Title3>Wishlist</Title3>
      <Box style={movieSection}>
        {wishlistData.length === 0 && <NormalText>No movie found in wishlist.</NormalText>}
        {wishlistData.length > 0 && wishlistData.map((movie, index) => {
          return (
            <Box style={moviePreview} key={`wishlist-${index}`} sx={{ m: 1 }}>
              { localStorage.getItem('username') === params.username && <FavoriteIcon 
                onClick={() => removeWishlist(''+movie[0])} 
                fontSize="medium"
                style={likeIcon}
              /> }
              <PreviewRating>{movie[7]}</PreviewRating>
              <Box>
                <img style={poster} src={movie[5]} alt={`poster of ${movie[0]}`}/>
              </Box>
              <PreviewText onClick={() => navigate(`/movie/${movie[0]}`)}>Movie: {movie[1]}</PreviewText>
              <PreviewText2>Director: {movie[3]}</PreviewText2>
            </Box>
          )})
        }
      </Box>
      { localStorage.getItem('username') === params.username && <Title3>Banlist</Title3> }
      { localStorage.getItem('username') === params.username && <Box style={banlistSection}>
        { banlistData.length === 0 && <NormalText>No banlist found.</NormalText> }
        { banlistData.length > 0 &&
          banlistData.map((banUser, index) => {
            return (
              <Box style={banlistPreview} key={`banlist-${index}`}>
                <CloseIcon style={closeBanlistBtn} onClick={() => deleteBanUser(banUser)}/>
                <p style={banlistContent} onClick={() => toProfile(banUser)}>{banUser}</p>
                <span style={banlistLayout}> </span>
              </Box>
          )})
        }
      </Box> }
    </Box>
  </>)
}

export default Profile;