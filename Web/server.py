from flask import Flask, request, redirect

app = Flask(__name__)

nextId = 9
topics = [
    {'id': 1, 'title': 'Thailand (Bangkok)', 'body': 'THB'},
    {'id': 2, 'title': 'Taiwan (Taipei)', 'body': 'TWD'},
    {'id': 3, 'title': 'Hongkong/Macau', 'body': 'HKD/MOP'},
    {'id': 4, 'title': 'Japan (Osaka)', 'body': 'Yen'},
    {'id': 5, 'title': 'Australia (Sydney, Brisbane)', 'body': 'AUD'},
    {'id': 6, 'title': 'Vietnam (Hanoi)', 'body': 'VND'},
    {'id': 7, 'title': 'Malaysia (Kuala Lumpur)', 'body': 'MYR'},
    {'id': 8, 'title': 'Vietnam (Danang)', 'body': 'VND'},
]


def template(lists, contents, id=None):
    contextUI = ''
    if id != None:
        contextUI = f'''
            <li><a href = "/update/{id}/">update</a></li>
            <li><form action="/delete/{id}" method="POST"><input type="submit" value="delete"></form></li>
        '''
    return f'''
    <!DOCTYPE html>
    <html>
        <head>
            <title>Bon voyage!</title>
        </head>
        <body>
            <h1><a href="/"> * countries or cities I've been to * </a></h1>
            <ol>
                {lists}
            </ol>
            <h2> Trip makes you happy :) </h2>
            {contents}
            <ul>
                <li><a href="/create/">create</a></li>
                {contextUI}
            </ul>
        </body>
    </html>
    '''


def getContents():
    liTags = ''
    for topic in topics:
        liTags = liTags + f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
    return liTags


@app.route('/')
def inedx():
    return template(getContents(), '<h2>Welcom3 :) </h2>')


@app.route('/create/', methods=['GET', 'POST'])
def create():
    # print('request.method: ', request.method)
    if request.method == 'GET':
        content = '''
            <form action="/create/" method="POST">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="write your story"></textarea></p>
                <p><input type="submit" value="create"></p>
            </form>
        '''
        return template(getContents(),content)
    elif request.method == 'POST':
        global nextId
        title = request.form['title']
        body = request.form['body']
        newTopic = {'id': nextId, 'title': title, 'body': body}
        topics.append(newTopic)
        url = '/read/' + str(nextId) + '/'
        nextId += 1
        return redirect(url)


@app.route('/read/<id>/')
def read(id):
    title = ''
    body = ''
    id = int(id)
    for topic in topics:
        if id == topic["id"]:
            title = topic["title"]
            body = topic["body"]
            break
    # print(title, body)
    return template(getContents(), f'<h2>{title}</h2>{body}', id)


@app.route('/update/<id>/', methods=['GET', 'POST'])
def update(id):
    # print('request.method: ', request.method)
    id = int(id)
    if request.method == 'GET':
        title = ''
        body = ''
        for topic in topics:
            if id == topic["id"]:
                title = topic["title"]
                body = topic["body"]
                break
        content = f'''
            <form action="/update/{id}/" method="POST">
                <p><input type="text" name="title" placeholder="title" value="{title}"></p>
                <p><textarea name="body" placeholder="body">{body}</textarea></p>
                <p><input type="submit" value="update"></p>
            </form>
        '''
        return template(getContents(),content)
    elif request.method == 'POST':
        global nextId
        title = request.form['title']
        body = request.form['body']
        for topic in topics:
            if id == topic['id']:
                topic['title'] = title
                topic['body'] = body
                break
        url = '/read/' + str(id) + '/'
        return redirect(url)
    

@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    id = int(id)
    for topic in topics:
        if id == topic['id']:
            topics.remove(topic)
            break
    return redirect('/')


app.run(port=5000, debug=True)