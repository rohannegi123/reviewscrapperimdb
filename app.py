import ssl
from flask import Flask, render_template, jsonify , request
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import pyttsx3
import pymongo



app = Flask(__name__)

@app.route('/', methods = ['GET'])
@cross_origin()
def homepage():
    engine = pyttsx3.init()
    engine.say(' You can find top highest voted reviews of any shows or movies from imdb here  ')
    engine.runAndWait()
    return render_template('index.html')


def checkexistance(data , db):  #to check if collection already axist
    a = db.list_collection_names()
    for i in a:
        if i == data:
            return True


@app.route('/showlist', methods=['GET','POST'])
@cross_origin()
def showlist():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            imdb_url = 'https://www.imdb.com/find?q=' + searchString
            uclient = uReq(imdb_url)   #opening thr url
            imdb_page = uclient.read()
            uclient.close()
            imdb_html = bs(imdb_page, 'html.parser')
            show_list = imdb_html.find_all('tr', {"class": ['findResult odd', 'findResult even']})
            show_link = show_list[0].td.a['href']
            showpage = 'https://www.imdb.com' + str(show_link)
            reviewpage = 'https://www.imdb.com' + str(show_link) + 'reviews?sort=totalVotes&dir=desc&ratingFilter=0'
            reviewRes = requests.get(reviewpage)
            reviewRes.encoding = 'utf-8'
            showreview_html = bs(reviewRes.text, "html.parser")
            print(showreview_html)
            reviewboxes = showreview_html.find_all('div', {'class': 'review-container'})


            # decorating the reuslts page with show images,etc
            poster = showreview_html.find('div', {'class': 'subpage_title_block'}).a.img['src']  # image of the show
            variable = showreview_html.find('h3', {'itemprop': 'name'}).a.text  # returns the name of the show
            rawreleasedate = showreview_html.find('h3', {'itemprop': 'name'}).span.text  # returns release date of the show with some more characters
            releasedate = rawreleasedate.replace('\n ', '')  # removing unwanted characters from str
            variable2 = releasedate.replace('  ', '')  # date of release
            showRes = requests.get(showpage)
            showRes.encoding = 'utf-8'
            show_html = bs(showRes.text, "html.parser")
            show_info = show_html.find_all('div', {'class': 'ipc-html-content ipc-html-content--base'})[0].text


            reviews = []
            for review in reviewboxes:
                try:
                    name = review.div.find('span', {'class': 'display-name-link'}).text
                except:
                    name = 'no username'
                try:
                    date = review.div.find('span', {'class': 'review-date'}).text
                except:
                    date = 'review date not available'
                try:
                    rating = review.div.div.span.span.text
                except:
                    rating = 'no rating'
                try:
                   commentHead = review.div.a.text
                except:
                    commentHead = 'no comment heading'
                try:
                    custComment = review.div.find('div', {'class': 'content'}).div.text
                except:
                    custComment = 'no review comment'

                   #adding items in dict
                mydict = {"Date": date, "Name": name, "Rating": rating, "CommentHead": commentHead,"Comment": custComment,'addings' : (poster , variable,variable2 , show_info) }
                reviews.append(mydict)
            db = pymongo.MongoClient(
                "mongodb+srv://rohan1:rohannegi@cluster0.ezeqz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
                ssl_cert_reqs=ssl.CERT_NONE)
            db = db['imdbscrapper']
            col_name = db[searchString]
            if checkexistance(col_name , db) == True :
                col_name.drop()
                col_name.insert_many(reviews)
            else:
                col_name.insert_many(reviews)

            return render_template('results.html', reviews=reviews, variable = variable ,variable2 = variable2,rating = rating, poster = poster , show_info = show_info)
        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong or No movie,show with suchname'

# return render_template('results.html')

    else:
        return render_template('index.html')





if __name__ == '__main__':
    app.run(debug= True)


