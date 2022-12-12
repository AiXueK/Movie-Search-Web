import sys

# setting path
sys.path.append('../')
sys.path.append('../functions')

import database
from functions import webfunctions

app = database.app

app.add_url_rule('/api/register/otc', methods=['POST'], view_func=webfunctions.genotc)

app.add_url_rule('/api/register', methods=['POST'], view_func=webfunctions.register)

app.add_url_rule('/api/auth', methods=['POST'], view_func=webfunctions.auth)

app.add_url_rule('/api/forgetpassword', methods=['POST'], view_func=webfunctions.forgetpassword)

app.add_url_rule('/alive', methods=['GET'], view_func=webfunctions.alive)

app.add_url_rule('/home', methods=['POST'], view_func=webfunctions.dashboard)

app.add_url_rule('/search', methods=['POST'], view_func=webfunctions.search)

app.add_url_rule('/api/logout', methods=['POST'], view_func=webfunctions.logout)

app.add_url_rule('/api/updateprofile', methods=['POST'], view_func=webfunctions.updateprofile)

app.add_url_rule('/api/updateprofile', methods=['POST'], view_func=webfunctions.updateprofile)


app.add_url_rule('/wishlist', methods=['POST'], view_func=webfunctions.getwishlist)

app.add_url_rule('/movie/addwishlist', methods=['POST'], view_func=webfunctions.addwishlist)

app.add_url_rule('/wishlist/removewishlist', methods=['DELETE'], view_func=webfunctions.removewishlist)

app.add_url_rule('/movieinfo', methods=['POST'], view_func=webfunctions.movieinfo)

app.add_url_rule('/wishlistinfo', methods=['POST'], view_func=webfunctions.wishlistinfo)

app.add_url_rule('/movie/checkwishlist', methods=['POST'], view_func=webfunctions.checkwishlist)

app.add_url_rule('/getrating', methods=["POST"], view_func=webfunctions.getrating)

app.add_url_rule('/addrating', methods=["POST"], view_func=webfunctions.addrating)

app.add_url_rule('/addreview', methods=["POST"], view_func=webfunctions.addreview)

app.add_url_rule('/deletereview', methods=["DELETE"], view_func=webfunctions.deletereview)

app.add_url_rule('/getmoviereview', methods=["POST"], view_func=webfunctions.getmoviereview)

app.add_url_rule('/getusereview', methods=["POST"], view_func=webfunctions.getuserreview)

app.add_url_rule('/banlist/info', methods=["POST"], view_func=webfunctions.getbanlist)

app.add_url_rule('/banlist/add', methods=["POST"], view_func=webfunctions.addbanlist)

app.add_url_rule('/banlist/remove', methods=["DELETE"], view_func=webfunctions.removebanlist)

app.add_url_rule('/getuserrating', methods=["POST"], view_func=webfunctions.getuserrating)

app.add_url_rule('/suggestion', methods=['POST'], view_func=webfunctions.suggestions)

app.add_url_rule('/banlist/check', methods=['POST'], view_func=webfunctions.checkbanlist)
