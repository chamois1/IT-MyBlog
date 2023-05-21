import pytest
from models import Accounts_Users, Posts, Comments, ReplyComment

""" 
Testing whether data is added to the model  
We will use 'parametrize' in order not to constantly write separate functions and the same code
After set up models, example: Accounts_Users, first argument - input data, second - assert, that is do the data match which we recorded
"""


@pytest.mark.parametrize('model, data, expected_values', [
                        
    (Accounts_Users(), {'login': 'testLogin', 'email': 'test@gmail.com', 'password': 'testpassword123'}, 
                        {'login': 'testLogin', 'email': 'test@gmail.com', 'password': 'testpassword123'}
    ),

    (Posts(), {'title': 'testTitle', 'description': 'testDescription', 'tag': 'testTag testTag testTag', 'type': 'testType'}, 
              {'title': 'testTitle', 'description': 'testDescription', 'tag': 'testTag testTag testTag', 'type': 'testType'}
    ),

    (Comments(), {'text': 'testText', 'id_post': 1, 'title_post': 'testTitlePost', 'id_author': 1},
                 {'text': 'testText', 'id_post': 1, 'title_post': 'testTitlePost', 'id_author': 1}
    ),

    (ReplyComment(), {'text': 'testText', 'id_main_comment': 1, 'id_author_reply': 1, 'login_author_reply': 'testLogin'},
                     {'text': 'testText', 'id_main_comment': 1, 'id_author_reply': 1, 'login_author_reply': 'testLogin'}
    )
])


def test_add_data_to_model(model, data, expected_values):
    # Act
    for key, value in data.items():
        setattr(model, key, value)

    # Assert 
    for key, value in expected_values.items():
        assert getattr(model, key) == value