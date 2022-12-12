# Frontend Guide
1. install [Google Chrome](https://www.google.com/intl/en_au/chrome/) latest version
2. install Node and NPM [here](https://nodejs.org/en/download/)
    - or via command line: `sudo apt update` and `sudo apt install nodejs` (for Linux)
3. install Yarn on Linux `sudo npm i -g yarn`
4. on terminal, navigate to project repository with `cd project`
5. on terminal, run `yarn install` to install packages (this step might take some time)
6. on terminal, run `yarn start` to run the frontend
    - Note: if this step failed, run `yarn upgrade` before `yarn start`
7. open Google Chrome and search `http://localhost:3000`

## first time running frontend
1. `cd project`
2. `npm install` or `yarn install`
3. `npm start` or `yarn start`

## running frontend
1. `cd project`
2. `npm install` or `yarn install`
3. `npm start` or `yarn start`
4. `control + C` to quit

## first time running backend
1. `cd project`
2. `chmod +x setup.sh`
3. `./setup.sh`
4. `cd backend`
5. `python3 app.py`

## running backend
1. `cd project/backend`
2. `python3 app.py`

## API Sprint 2
~~~python
###------ get wishlist ------###
url = '/wishlistinfo'
methods = 'POST'
# frontend -> backend
{
  email: string,
}
# backend -> frontend success
['movieId1', 'movieId2']
# backend -> frontend failed
{
  message: string
}

###------ add to wishlist ------###
url = '/movie/addwishlist'
methods = 'POST'
# frontend -> backend
{
  movieId: string,
  email: string,
}
# backend -> frontend success
{
  message: string
}
# backend -> frontend failed
{
  message: string
}

###------ delete from wishlist ------###
url = '/wishlist/removewishlist'
methods = 'DELETE'
# frontend -> backend
{
  email: string,
  movieId: string,
}
# backend -> frontend success
{
  message: string
}
# backend -> frontend failed
{
  message: string
}

###------ movie information ------###
url = '/movieinfo'
methods = 'POST'
# frontend -> backend
{
  movieId: string,
}
# backend -> frontend success
[['ID', 'Name', 'Genre', 'Director', 'Cast', 'Poster', 'Description', 'Rating', 'Year']]
# backend -> frontend failed
{
  message: string
}

###------ check movie wishlist ------###
url = 'movie/checkwishlist'
methods = 'POST'
# frontend -> backend
{
  email: string,
  movieId: string,
}
# backend -> frontend success
boolean
# backend -> frontend failed
{
  message: string
}

###------ edit profile ------###
url = '/api/updateprofile'
methods = 'POST'
# frontend -> backend
# if no edit, the respective value will be undefined
{
  token: string,
  username: string,
  oldPassword: string,
  newPassword: string,
  confirmedPassword: string,
}
# backend -> frontend success
{
  message: string
}
# backend -> frontend failed
{
  message: string
}
~~~

## API Sprint3

~~~python
###------ get banlist ------###
url = '/banlist/info'
methods = 'POST'
# frontend -> backend
{
  username: string,
}
# backend -> frontend success
['username1', 'username2']
# backend -> frontend failed
{
  message: string
}

###------ add to banlist ------###
url = '/banlist/add'
methods = 'POST'
# frontend -> backend
{
  username: string, # username of user wants to add someone into their banlist
  ban_name: string, # username of user being added to banlist
}
# backend -> frontend success
{
  message: string
}
# backend -> frontend failed
{
  message: string
}

###------ delete from banlist ------###
url = '/banlist/remove'
methods = 'DELETE'
# frontend -> backend
{
  username: string, # email of user wants to remove someone from their banlist
  ban_name: string, # username of user being deleted from banlist
}
# backend -> frontend success
{
  message: string
}
# backend -> frontend failed
{
  message: string
}

###------ fetch rating ------###
url = '/getrating'
methods = 'POST'
# frontend -> backend
{
  username: string,
  movieId: string,
}
# backend -> frontend success
float/double
# backend -> frontend failed
{
  message: string
}

###------ fetch user rating ------###
url = '/getuserrating'
methods = 'POST'
# frontend -> backend
{
  username: string,
  movieId: string,
}
# backend -> frontend success
int
# backend -> frontend failed
{
  message: string
}


###------ add rating ------###
url = '/addrating'
methods = 'POST'
# frontend -> backend
{
  username: string,
  movieId: string,
  rating: int,
}
# backend -> frontend success
{
  message: string
}
# backend -> frontend failed
{
  message: string
}

###------ add review ------###
url = '/addreview'
methods = 'POST'
# frontend -> backend
{
  username: string,
  movieId: string,
  content: string,
}
# backend -> frontend success
{
  message: string
}
# backend -> frontend failed
{
  message: string
}

###------ delete review ------###
url = '/deletereview'
methods = 'DELETE'
# frontend -> backend
{
  username: string,
  movieId: string,
  reviewId: string,
}
# backend -> frontend success
{
  message: string
}
# backend -> frontend failed
{
  message: string
}

###------ fetch review movie page ------###
url = '/getmoviereview'
methods = 'POST'
# frontend -> backend
{
  movieId: string,
  username: string,
}
# backend -> frontend success
# sort by time, latest to oldest
[{
  rating: int,
  content: string,
  username: string,
  sentimentAnalysis: int, # 1 = positive, 0 = neutral, -1 = negative
  spam: boolean, # false = real comment, true = fake comment (if true frontend display likely spam)
  similarityScore: int/float, # type not matters to frontend
}]
# backend -> frontend failed
{
  message: string
}

###------ fetch review profile page ------###
url = '/getusereview'
methods = 'POST'
# frontend -> backend
{
  username: string,
}
# backend -> frontend success
# sort by time, latest to oldest
[{
  reviewId: int,
  movieId: int,
  movieName: string,
  content: string,
}]
# backend -> frontend failed
{
  message: string
}

###------ fetch suggestions ------###
url = '/suggestion'
methods = 'POST'
# frontend -> backend
{
  movieId: string,
  username: string,
}
# backend -> frontend success
[['ID', 'Name', 'Genre', 'Director', 'Cast', 'Poster', 'Description', 'Rating', 'Year']]
# backend -> frontend failed
{
  message: string
}

###------ fetch banlist status ------###
url = '/banlist/check'
methods = 'POST'
# frontend -> backend
{
  username: string, # email of user wants to remove someone from their banlist
  ban_name: string, # username of user being deleted from banlist
}
# backend -> frontend success
boolean
# backend -> frontend failed
{
  message: string
}
~~~

---
