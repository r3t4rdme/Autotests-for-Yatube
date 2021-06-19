from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Post

User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.leo = User.objects.create(username='leo')
        Post.objects.create(
            text='Тестовый текст',
            author=cls.leo
        )
        cls.post_author_client = Client()
        cls.post_author_client.force_login(cls.leo)

    def setUp(self):
        self.leo_test = User.objects.create_user(username='leo_test')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.leo_test)

    def test_new_post_created(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст из формы',
            'author': self.leo_test
        }
        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_post_edited(self):
        form_data = {
            'text': 'Измененный текст',
            'author': self.leo_test
        }
        editing = self.post_author_client.post(
            '/leo/1/edit/',
            data=form_data,
            follow=True
        )
        after_edit_response = self.post_author_client.get('/leo/1/')
        work_post = after_edit_response.context.get('post')
        work_post_text = work_post.text
        self.assertRedirects(
            editing, '/leo/1/')
        self.assertEqual(
            work_post_text, 'Измененный текст', 'Текст не изменился')
