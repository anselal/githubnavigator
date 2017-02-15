import sys
import json

from app import app
from flask import render_template, flash, request, redirect, url_for
from forms import SearchForm

# import any special Python 2.7 packages
if sys.version_info.major == 2:
    from urllib import urlopen

# import any special Python 3 packages
elif sys.version_info.major == 3:
    from urllib.request import urlopen


# -------------------------------------------------------------------------------
# Custom error page

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# -------------------------------------------------------------------------------
# Main Views

# This function will be mounted on "/" and display a entry link
@app.route('/')
@app.route('/index')
def index():
    form = SearchForm()
    return render_template('index.html', title='Home', form=form)


@app.route('/navigator/', methods=['POST'])
def navigator():
    '''
        This part of the Application will fetch the JSON data from the GitHub API
        based on the search keyword provided. Then extract the required field
        from the JSON data and send the data to Jinja2 Template for rendering.
    '''

    form = SearchForm()
    if not form.validate():
        flash('No keyword supplied to search.')
        return redirect(url_for('index'))

    urlData = 'https://api.github.com/search/repositories?q=' + request.form['search_term']

    webUrl = urlopen(urlData)
    theData = []

    if webUrl.getcode() == 200:
        data = webUrl.read()
        theJSON = json.loads(data.decode('utf-8'))

        total = theJSON['total_count']
        latest = 5 if total > 5 else total

        if total > 0:
            for i in range(0, latest):
                description = theJSON['items'][i]['description']
                repoName = theJSON['items'][i]['name']
                createdAt = theJSON['items'][i]['created_at']
                ownerUrl = theJSON['items'][i]['owner']['html_url']
                avatarUrl = theJSON['items'][i]['owner']['avatar_url']
                ownerLogin = theJSON['items'][i]['owner']['login']

                repoUrl = theJSON['items'][i]['html_url']

                commitsUrl = theJSON['items'][i]['commits_url']
                commitsUrl = commitsUrl[0:-6]

                try:
                    commitJSON = urlopen(commitsUrl)

                    if (commitJSON.getcode() == 200):
                        commitData = commitJSON.read()
                        commitJSONData = json.loads(commitData.decode('utf-8'))
                        commitSha = commitJSONData[0]['sha']
                        commitMessage = commitJSONData[0]['commit']['message']
                        committerName = commitJSONData[0]['commit']['committer']['name']
                    else:
                        commitSha = 'Data Cannot Be Loaded'
                        commitMessage = 'Data Cannot Be Loaded'
                        committerName = 'Data Cannot Be Loaded'
                except:
                    commitSha = 'Data Cannot Be Loaded'
                    commitMessage = 'Data Cannot Be Loaded'
                    committerName = 'Data Cannot Be Loaded'

                theData.append({'search_term': 'arrow', 'respository_name': repoName, \
                                'created_at': createdAt, 'owner_url': ownerUrl, \
                                'avatar_url': avatarUrl, 'owner_login': ownerLogin, \
                                'sha': commitSha, 'commit_message': commitMessage, \
                                'commit_author_name': committerName, \
                                'repository_description': description, \
                                'repository_url': repoUrl})

            # sorts the data based on created_at in decending order
            theData = sorted(theData, key=lambda k: k['created_at'], reverse=True)

            # return the response with the template
            return render_template('search_result.html', theKey=request.form['search_term'], theDatas=theData,
                                   total=total, \
                                   latest=latest)
        else:
            flash('Nothing Found Based On Search Term.')
            return redirect(url_for('index'))
