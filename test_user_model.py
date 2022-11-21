import os
# temp db for test
os.environ['DATABASE_URI'] = 'sqlite://'
import unittest
from microblog import app, db, User, Post


class TestUserModel(unittest.TestCase):
    def setUp(self):
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_check_password(self):
        u = User(username='john', email='john@example.com')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))
    
    def test_follow(self):
        u1 = User(username='john', email='john@example.com')
        u1.set_password('cat')
        u2 = User(username='susan', email='susan@example.com')
        u2.set_password('cat')
        db.session.add_all([u1, u2])
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])
        
        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_in_followed(u2))
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u1.followed.all(), [u2])
        self.assertEqual(u2.followers.all(), [u1])
        
        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_in_followed(u2))
        self.assertEqual(u1.followed.count(), 0)
    
    def test_followed_users_posts(self):
        username = ['john', 'susan', 'mary', 'david']
        U = []
        P = []
        for name in username:
            #create user
            user = User(
                username=name, 
                email=f'{name}@example.com'
            )
            user.set_password(f'{name}123')
            #post for the user
            post = Post(body=f'post from {name}', author=user)
            U.append(user)
            P.append(post)
            
        db.session.add_all(U)
        db.session.add_all(P)
        db.session.commit()
        
        U[0].follow(U[1])
        U[0].follow(U[2])
        U[0].follow(U[3])
        db.session.commit()
        
        self.assertEqual(
            U[0].followed_users_posts().all(),
            P[::-1]
        )


if __name__ == '__main__':
    unittest.main()
