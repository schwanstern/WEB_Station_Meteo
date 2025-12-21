from django.test import TestCase
from core import forms
from django.contrib.auth.models import User

class FormTests(TestCase):
    def test_login_form_valid(self):
        form = forms.LoginForm(data={'identifiant': 'testuser', 'mdp': 'password'})
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        form = forms.LoginForm(data={'identifiant': ''})
        self.assertFalse(form.is_valid())

    def test_register_form_valid(self):
        # Ensure user does not exist
        form = forms.RegisterForm(data={
            'identifiant': 'newuser',
            'email': 'new@example.com',
            'mdp': 'password'
        })
        self.assertTrue(form.is_valid())

    def test_register_form_duplicate_user(self):
        User.objects.create_user(username='dupuser', email='dup@example.com', password='password')
        form = forms.RegisterForm(data={
            'identifiant': 'dupuser',
            'email': 'other@example.com',
            'mdp': 'password'
        })
        self.assertFalse(form.is_valid())
        self.assertIn("Ce nom d'utilisateur est déjà pris.", form.errors['identifiant'])

    def test_register_form_contact_duplicate_email(self):
         User.objects.create_user(username='user1', email='dup@example.com', password='password')
         form = forms.RegisterForm(data={
            'identifiant': 'user2',
            'email': 'dup@example.com',
            'mdp': 'password'
        })
         self.assertFalse(form.is_valid())
         self.assertIn("Cet email est déjà utilisé.", form.errors['email'])
