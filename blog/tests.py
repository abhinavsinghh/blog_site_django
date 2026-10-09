from django.test import TestCase
from django.urls import reverse

from .models import Post


class BlogViewTests(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title="Hello", excerpt="Short", slug="hello", content="Some long content here."
        )

    def test_pages_render_without_image_or_author(self):
        for name in ("starting-page", "posts-page", "read-later"):
            self.assertEqual(self.client.get(reverse(name)).status_code, 200)
        self.assertEqual(self.client.get(reverse("post-detail-page", args=["hello"])).status_code, 200)

    def test_missing_post_is_404(self):
        self.assertEqual(self.client.get(reverse("post-detail-page", args=["nope"])).status_code, 404)

    def test_comment_saved_and_invalid_rerendered(self):
        url = reverse("post-detail-page", args=["hello"])
        resp = self.client.post(url, {"user_name": "A", "user_email": "a@b.co", "text": "Nice"})
        self.assertRedirects(resp, url)
        self.assertEqual(self.post.comments.count(), 1)
        self.assertEqual(self.client.post(url, {"user_name": ""}).status_code, 200)

    def test_read_later_toggle(self):
        self.client.post(reverse("read-later"), {"post_id": self.post.id})
        self.assertEqual(self.client.session["stored_posts"], [self.post.id])
        self.client.post(reverse("read-later"), {"post_id": self.post.id})
        self.assertEqual(self.client.session["stored_posts"], [])
        self.assertEqual(self.client.post(reverse("read-later"), {"post_id": "x"}).status_code, 302)
