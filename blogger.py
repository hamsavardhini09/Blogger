#!/usr/bin/env python
# encoding: utf-8

from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import urllib

DEFAULT_BLOG_ROOM_NAME = "Blogger"

DEFAULT_LOGOUT_BLOG_HEADER = """
    <div class="top-row">
    <a class="home-link" href="/">home</a>
        |
    <a class="New-post-link" href="/new">New Post</a>
        |
    <a class ="logout-link" href="/logout">logout</a>
    </div>"""

DEFAULT_LOGIN_BLOG_HEADER = """
    <div class="top-row">
    <a class="home-link" href="/">home</a>
        |
    <a class="New-post-link" href="/new">New Post</a>
        |
    <a class ="login-link" href="/login">login</a>
    </div>"""


class BlogUser(ndb.Model):

    user_name = ndb.StringProperty()
    user_email = ndb.StringProperty()
    user_id = ndb.StringProperty()


class Blog(ndb.Model):

    blog_title = ndb.StringProperty()
    published_date = ndb.DateTimeProperty(auto_now_add=True)
    updated_date = ndb.DateTimeProperty(auto_now_add=True)
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    blog_user = ndb.StructuredProperty(BlogUser)
    body = ndb.TextProperty()


def blog_key(blog_room=DEFAULT_BLOG_ROOM_NAME):
    return ndb.Key('blogger', blog_room)


class HomePage(webapp2.RequestHandler):

    def get(self):

        blog_user = users.get_current_user()

        if blog_user is None:
            self.response.write(DEFAULT_LOGIN_BLOG_HEADER)
            blog_user = users.User("Guest")
        else:
            self.response.write(DEFAULT_LOGOUT_BLOG_HEADER)

        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        self.response.write('Hello, ' + blog_user.nickname())
        self.response.out.write(
            """
            <html>
            <head>
            <link type="text/css" rel="stylesheet" href="/static/blog_style.css" />
            <title>Welcome to MyBlog</title></head>
            <body>"""
        )

        blog_room = self.request.get('blog_name', DEFAULT_BLOG_ROOM_NAME)
        blogs_query = Blog.query(ancestor=blog_key(blog_room)).order(-Blog.published_date)
        blogs = blogs_query.fetch(5)
        for each_blog in blogs:
            self.response.out.write("""
            <div>
            """
                                    )
            self.response.out.write("<h3>%s</h3>" %each_blog.blog_title)
            self.response.out.write("<p>%s</p>" %each_blog.published_date.strftime("%d/%m/%y %H:%M:%S"))
            self.response.out.write("<p>%s</p>" %each_blog.body)

            self.response.out.write("""
            </div>
            """
                                    )
            self.response.out.write("""<br>""")

        self.response.out.write(""" </body></html>""")


class NewPost(webapp2.RequestHandler):

    def get(self):
        blog_user = users.get_current_user()

        if blog_user is None:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            self.response.write(DEFAULT_LOGOUT_BLOG_HEADER)

            self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
            self.response.write('Hello, ' + blog_user.nickname())
            self.response.out.write(
                """
                <html>
                <head>
                <link type="text/css" rel="stylesheet" href="/static/blog_style.css" />
                <title>Welcome to MyBlog</title></head>
                <body>"""
            )
            self.response.out.write("""
            <form action="" method="post">
            <div>
            <div>Blog Title<br>
            <textarea name="blog_title" rows="3" cols="90"></textarea>
            </div>
            <div>Blog Content<br>
            <textarea name="blog_content" rows="30" cols="90"></textarea>
            <input type="submit" value="Submit" height="20"></input>
            </div>
            </div>
            </form>
            </body></html>""")

    def post(self):
        user_email = users.get_current_user().email()
        user_id = users.get_current_user().user_id()
        user_name = users.get_current_user().nickname()

        blog_name = self.request.get('blog_name', DEFAULT_BLOG_ROOM_NAME)

        blog = Blog(parent=blog_key(blog_name))
        blog.body = self.request.get('blog_content')
        blog.blog_title = self.request.get('blog_title')
        if users.get_current_user():
            blog.blog_user = BlogUser(user_name=user_name, user_email=user_email, user_id=user_id)
        blog.put()

        query_params = {'blog_name': blog_name}
        self.redirect('/?' + urllib.urlencode(query_params))


class Login(webapp2.RequestHandler):

    def get(self):
        blog_user = users.get_current_user()
        if blog_user is None:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            self.redirect('/')


class Logout(webapp2.RequestHandler):

    def get(self):

        blog_user = users.get_current_user()
        if blog_user is not None:
            self.redirect(users.create_logout_url('/'))


app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/new', NewPost),
    ('/login', Login),
    ('/logout', Logout)
], debug=True)