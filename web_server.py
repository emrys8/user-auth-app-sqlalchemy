from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi, re

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, or_

from database_setup import User, Base

# Bind the engine to the metadata of the Base class
# Create a db session
engine = create_engine('sqlite:///user_app.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

def css_styles():
    return '\
    html { font-family: Helvetica, Arial, sans-serif; }\
    body { width: 80%; }\
    a { color: #1187b2; } a:link, a:visited { color: #1187b2; }\
    form input { padding: 0.5rem; margin-right: 10px; font-size: 1em; }\
    input { width: 300px; }\
    label { display: inline-block; width: 100px; }\
    form div { margin-top: 10px; }\
    button { margin-left: 170px; padding: 0.5rem; font-size: 0.8rem;\
        display: inline-block; width: 170px; }\
    '
def encrypt(password):
    password = password.lower()
    my_hash = {}
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    num = 0
    for char in alphabets:
        my_hash[char] = str(num)
        num += 1

    nums = '0123456789'
    for n in nums:
        my_hash[n] = n

    # print my_hash
    hashed_pwd = ''
    for s in password:
        hashed_pwd += my_hash[s]

    print hashed_pwd
    return hashed_pwd

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/users"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                styles = css_styles()
                output += "<html><head><style>%s</style></head><body>" % styles

                output += "<h1>User Auth Application</h1>"
                output += '''<form method='POST' action='/users' enctype='multipart/form-data'>
                <div>
                  <label for='user-name'>Username</label>
                  <input type='text' name='username' id='user-name' placeholder='Enter your username'>
                </div>

                <div>
                   <label for='mail'>Email</label>
                   <input type='email' name='useremail' id='mail' placeholder='Enter your Email'>
                </div>

                <div>
                  <label for='pwd'>Password</label>
                  <input type='password' name='user-pwd' id='pwd' placeholder='Choose a password'>
                </div>

                <div>
                  <button type='submit'>Sign Up</button>
                </div>
                '''

                output += "<p>Already a user <a href='/users/login'>login</a></p>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                styles = css_styles()
                output = ""
                output += "<html><head><style>%s</style></html><body>" % styles
                output += "<h1>Welcome to my page dear user!</h1>"
                output += "<p><a href='/users'>Create a new Account</a></p>"
                output += "<p><a href='/users/login'>Sign In</a></p>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/all_users"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                users = session.query(User).all()

                styles = css_styles()
                output = ""
                output += "<html><head><style>%s</style><body>" % styles
                output += "<h1>List of all users</h1>"
                for user in users:
                    output += "<li>%s | %s | %s</li>" % (user.user_name, user.email, user.password)

                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/login"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><head><style>%s</style><body>" % css_styles()
                output += "<h1>User Auth Application</h1><h2>Login</h2>"
                output += '''<form method='POST' action='/users/login' enctype='multipart/form-data'>
                <div>
                   <label for='mail'>Email</label>
                   <input type='email' name='useremail' id='mail' placeholder='Enter your Email'>
                </div>

                <div>
                  <label for='pwd'>Password</label>
                  <input type='password' name='user-pwd' id='pwd' placeholder='Choose a password'>
                </div>

                <div>
                  <button type='submit'>Login</button>
                </div>

                </form>
                <div>
                  <p>Forgot password? <a href="/users/reset-password">Reset it</a></p>
                </div>
                '''
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/reset-password"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = "<html lang='en'><head><title>Reset Password</title><style>%s</style></head><body>" % css_styles()
                output += "<h1>Reset Password</h1>"
                output += '''<form method='POST' action='/users/reset-password' enctype='multipart/form-data'>
                <div>
                    <label for='mail'>Email</label>
                    <input type='text' name = 'useremail' id = 'mail' placeholder='Enter your Email'>
                </div>
                <div>
                    <label for='pwd'>Password</label>
                    <input type='password' id = 'pwd' name = 'user-pwd' placeholder='Enter a new Password'>
                </div>
                <div>
                    <label for='pwd2'>Password</label>
                    <input type='password' id = 'pwd2' placeholder='Enter the password again'>
                </div>
                <div>
                 <button type='submit'>Submit</button>
                </div>
                '''

                output += "</form></body></html>"
                self.wfile.write(output)
                return


        except:
            pass

    def do_POST(self):

        try:
            if self.path.endswith("/users"):
                print ('path ends with /users')
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                # print (ctype)
                # print (pdict)
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)

                    username = fields.get('username')
                    email = fields.get('useremail')
                    password = fields.get('user-pwd')

                    # find a user with that username, email or password

                    # print (or_)
                    # a_user = session.query(User).filter_by(or_(user_name = username[0],
                    #                                       email = email[0], password = password[0]))

                    # first select the user with the user_name
                    # then, use the username obtained to get the user email

                    by_username = session.query(User).filter_by(user_name = username[0]).all()
                    by_email = session.query(User).filter_by(email = email[0]).all()

                    # print (a_user)
                    # new_output = ""

                    if ((by_username != []) or (by_email != [])):
                        # user exists, send a error message

                        data = ''
                        message = ''

                        if (by_username == []):
                            message = 'email'
                            data = by_email[0].email
                        else:
                            message = 'username'
                            data = by_username[0].user_name

                        # print ('user exists...')
                        new_output = ""
                        new_output += "<html><head><style>%s</style></head><body>" % css_styles()
                        new_output += "<h1>Error!</h1><p>A user with the %s: %s already exists</p>" % (message, data)
                        new_output += "<a href='/users'>Go Back</a>"
                        new_output += "</body></html>"
                        # print new_output
                        self.send_response(400)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(new_output)
                        # print output
                        return

                    user = User(user_name=username[0], email = email[0], password = encrypt(password[0]))

                    # print user
                    # persist to database
                    session.add(user)
                    session.commit()

                    # send headers
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/')
                    self.end_headers()
                    self.wfile.write(output)
                    # print output
                    return

            if self.path.endswith("/login"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == "multipart/form-data":
                    fields = cgi.parse_multipart(self.rfile, pdict)

                    email = fields.get('useremail')
                    password = fields.get('user-pwd')

                    user = session.query(User).filter_by(email=email[0], password=encrypt(password[0])).all()

                    if (user == []):

                        # user does not exist
                        # redirect user to the login page

                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/login')
                        self.end_headers()
                        self.wfile.write(output)
                        return

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/')
                    self.end_headers()
                    self.wfile.write(output)
                    return

            if self.path.endswith("/users/reset-password"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == "multipart/form-data":
                    fields = cgi.parse_multipart(self.rfile, pdict)

                    email = fields.get('useremail')

                    user = session.query(User).filter_by(email = email[0]).one()

                    if (user == []):
                        # user does not exist
                        # create an account
                        output = "<html lang='en'><head><style>%s</style><body>" % css_styles()
                        output += "<h1>Error</h1><h2>This email is not yet registered.\
                        <a href='/users'>Create an account</a></h2></body></html>"

                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(output)
                        return

                    # user exist
                    # get the password and reset it
                    user_password = fields.get('user-pwd')
                    user.password = encrypt(user_password[0])

                    session.add(user)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/')
                    self.end_headers()
                    self.wfile.write(output)
                    return

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print 'Web server running on port %s' % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()
