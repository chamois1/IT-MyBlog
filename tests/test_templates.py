import pytest

from app import app
from models import Accounts_Users, Posts, listRequestEdit
from db import db

"""
Testing that the pages have loaded their templates, we will check this with the <title> tag. 
Let's create prepared data in models, example - for routes profiles, account and session.
Using 'parametrize' will not constantly create a function, thereby shortening the code.
"""


# checking url and templates(tag <title>) 
@pytest.mark.parametrize('path, expected_text', [

    # main routes
    ('/', 'Index'),
    ('/sign-up', 'Зарегеструватися'),
    ('/sign-in', 'Увійти'),
    ('/search/test', 'Результат по запиту "test"'),
    ('/contact', 'Контакти'),
    ('/statistics', 'Статистика сайту'),

    # profiles
    ('/my-profile', 'Мій профіль'),
    ('/my-profile/settings', 'Налаштування профіля'),
    ('/my-profile/history-comments', 'Історія моїх коментарів'),
    ('/my-profile/save-posts', 'Збережені пости'),
    ('/my-profile/like-posts', 'Вподобані пости'),
    ('/my-profile/request-post-edits', 'Мої запити на правку постів'),
    
    # admin panel
    ('/admin/add-post', 'Добавити пост'),
    ('/admin/list-posts', 'Список постів'),
    ('/admin/list-posts', '<td>news</td>'), # display post
    ('/admin/list-posts/editor-post/testTitle/1', 'Редагувати пост'),
    ('/admin/list-users', 'Список користувачів'),
    ('/admin/list-users', '<td>testUser</td>'), # display user
    ('/admin/list-request-edit', 'Список запитів на редагування поста'),
    ('/admin/list-request-edit', '<td>testText</td>'), # display request

    # posts
    ('/news', 'news'),
    ('/news', 'testTitle'), # display post
    ('/post/testTitle/1', 'Post testTitle'),
])


def test_page_content(path, expected_text):
    with app.app_context():
        with app.test_client() as client:
            with client.session_transaction() as session:

                # create tests data
                test_userAdmin = Accounts_Users(login='testUserAdmin', email='testUserAdmin@gmail.com', password='test123Admin', is_admin=True)
                test_user = Accounts_Users(login='testUser', email='test@gmail.com', password='test123')
                test_post = Posts(title='testTitle', description='testDescription', tag='#testTag #testTag', type='news')
                test_request = listRequestEdit(text='testText', id_post=1, title_post='testTitle', id_author=1)

                db.session.add(test_userAdmin)
                db.session.add(test_user)
                db.session.add(test_post)
                db.session.add(test_request)

                db.session.commit()

                session['id'] = test_userAdmin.id
                session['is_admin'] = test_userAdmin.is_admin


        response = client.get(path)
        assert expected_text in response.data.decode('utf-8')