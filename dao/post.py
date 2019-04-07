from dao.data import Data
import psycopg2
from config.dbconfig import pg_config


class PostDAO:

    def __init__(self):
        #DATABASE_URL = 'postgres://postgres:databaseclass@localhost:5432/jjkchat'
        DATABASE_URL = "dbname=%s user=%s password=%s host=%s" % (pg_config['dbname'], pg_config['user'], pg_config['passwd'], pg_config['host'])
        self.conn = psycopg2._connect(DATABASE_URL)

    posts = Data().posts

    def getAllPosts(self):
        cursor = self.conn.cursor()
        query = "select * from post"
        try:
            cursor.execute(query)
        except psycopg2.Error as e:
            return
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getPostsByGroupID(self, gID):
        cursor = self.conn.cursor()
        #query = "select * from post where chat_group_id = %s"

        query = """WITH plikes AS (SELECT post_id, count(*) AS likes
	                    FROM reactions
	                    WHERE reaction = 'like'
	                    GROUP BY post_id),
                    pdislikes AS (SELECT post_id, count(*) AS dislikes
	                    FROM reactions
	                    WHERE reaction = 'dislike'
	                    GROUP BY post_id)
                SELECT post.post_id, post.media, post.message, post.post_date, post.chat_group_id, post.user_id,likes, dislikes, users.username, users.first_name, users.last_name 
                FROM post natural inner join users LEFT JOIN plikes on post.post_id = plikes.post_id LEFT JOIN pdislikes on post.post_id = pdislikes.post_id
                WHERE post.chat_group_id =%s;"""
        try:
            cursor.execute(query,(gID,))
        except psycopg2.Error as e:
            return
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getNumberOfReactionsForGivenPost(self, pID, reaction):
        cursor = self.conn.cursor()
        query = "SELECT post_id, count(*) as likes FROM reactions  where post_id = %s and reaction =%s GROUP BY post_id"
        try:
            cursor.execute(query, (pID, reaction,))
        except psycopg2.Error as e:
            return
        result = cursor.fetchone()
        return result

    def getListOfUsersWhoReactedPost(self, pID, reaction):
        cursor = self.conn.cursor()
        query = "SELECT  user_id, first_name, last_name, username, reaction_date FROM reactions NATURAL INNER JOIN users WHERE post_id = %s AND reaction = %s"
        try:
            cursor.execute(query, (pID, reaction, ))
        except psycopg2.Error as e:
            return
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getNumberOfPostsPerDay(self):
        cursor = self.conn.cursor()
        query = "SELECT post_date AS day, count(*) AS total FROM post GROUP BY post_date"
        try:
            cursor.execute(query)
        except psycopg2.Error as e:
            return
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getNumberOfRepliesPerDay(self):
        cursor = self.conn.cursor()
        query = "SELECT reply_date AS day, count(*) AS total FROM reply GROUP BY reply_date"
        try:
            cursor.execute(query)
        except psycopg2.Error as e:
            return
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getNumberOfLikesPerDay(self):
        cursor = self.conn.cursor()
        query = "SELECT reaction_date AS day, count(*) AS total FROM reactions WHERE reaction = 'like' GROUP BY reaction_date"
        try:
            cursor.execute(query)
        except psycopg2.Error as e:
            return
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getNumberOfDislikesPerDay(self):
        cursor = self.conn.cursor()
        query = "SELECT reaction_date AS day, count(*) AS total FROM reactions WHERE reaction = 'dislike' GROUP BY reaction_date"
        try:
            cursor.execute(query)
        except psycopg2.Error as e:
            return
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getNumberOfRepliesForGivenPost(self, pID):
        cursor = self.conn.cursor()
        query = "SELECT post_id, count(*) AS total_replies FROM reply WHERE post_id = %s GROUP BY post_id"
        try:
            cursor.execute(query, (pID,))
        except psycopg2.Error as e:
            return
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getNumberOfPostsPerDayByUser(self, uID):
        cursor = self.conn.cursor()
        query = "SELECT post_date AS day, count(*) AS total FROM post WHERE user_id = %s GROUP BY post_date"
        try:
            cursor.execute(query, (uID, ))
        except psycopg2.Error as e:
            return
        result = cursor.fetchone()
        return result

    def getNumberOfPostPerDay(self):
        cursor = self.conn.cursor()
        query = "SELECT post_date AS day, count(*) AS total FROM post GROUP BY post_date"
        try:
            cursor.execute(query)
        except psycopg2.Error as e:
            return
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getRepliesByPostID(self, pID):
        cursor = self.conn.cursor()
        query = "SELECT reply_id, reply_date, reply_message, post_id, username, first_name, last_name FROM reply natural inner join users WHERE post_id =%s"
        try:
            cursor.execute(query,(pID, ))
        except psycopg2.Error as e:
            return
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getPostByID(self, pID):
        post = list(filter(lambda u: u['post_id'] == pID, self.posts))
        return post

    def getMessageByPostID(self,pID):
        message = list(filter(lambda u: u['post_id'] == pID, self.posts))
        return message

    def getMediaByPostID(self, pID):
        media = list(filter(lambda u: u['post_id'] == pID, self.posts))
        return media

    def getAuthorByPostID(self, pID):
        user = list(filter(lambda u: u['post_id'] == pID, self.posts))
        return user

    def getPostsByUserID(self, uID):
        posts = list(filter(lambda u: u['post_author_id'] == uID, self.posts))
        return posts

    def addPost(self, gID, aID, message,media):
        return "Message posted id 5"