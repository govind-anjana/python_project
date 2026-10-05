from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class AuthenticationTests(APITestCase):
	signup_url = "/api/signup/"
	login_url = "/api/login/"
	password = "Tr0ub4dor&3"
#this are to api to create to endpoint
	def signup(self, **overrides):
		payload = {
			"name": "Alex Morgan",
			"email": "alex@example.com",
			"password": self.password,
		}
		payload.update(overrides)
		return self.client.post(self.signup_url, payload, format="json")

	def test_signup_stores_a_hashed_password(self):
		response = self.signup()

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		user = User.objects.get(email="alex@example.com")
		self.assertNotEqual(user.password, self.password)
		self.assertTrue(check_password(self.password, user.password))

	def test_signup_rejects_duplicate_email(self):
		self.signup()

		response = self.signup(email="ALEX@example.com")

		self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
		self.assertEqual(response.data["msg"], "Email already exists")

	def test_signup_rejects_invalid_email_and_short_password(self):
		invalid_email = self.signup(email="not-an-email")
		short_password = self.signup(password="short")

		self.assertEqual(invalid_email.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(short_password.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(User.objects.count(), 0)

	def test_login_accepts_hashed_password_and_rejects_wrong_password(self):
		self.signup()

		valid_response = self.client.post(
			self.login_url,
			{"email": "alex@example.com", "password": self.password},
			format="json",
		)
		invalid_response = self.client.post(
			self.login_url,
			{"email": "alex@example.com", "password": "wrong-password"},
			format="json",
		)

		self.assertEqual(valid_response.status_code, status.HTTP_200_OK)
		self.assertEqual(valid_response.data["msg"], "Login Success")
		self.assertEqual(invalid_response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_login_hashes_existing_plaintext_password(self):
		User.objects.create(
			name="Alex Morgan",
			email="alex@example.com",
			password=self.password,
		)

		response = self.client.post(
			self.login_url,
			{"email": "alex@example.com", "password": self.password},
			format="json",
		)

		user = User.objects.get(email="alex@example.com")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertTrue(check_password(self.password, user.password))

	def test_user_list_and_details_require_staff_access(self):
		self.signup()
		list_url = "/api/users/"
		detail_url = f"/api/users/{User.objects.get().id}/"

		anonymous_response = self.client.get(list_url)
		self.assertIn(
			anonymous_response.status_code,
			(status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
		)

		staff_user = get_user_model().objects.create_user(
			username="staff",
			password="safe-password",
			is_staff=True,
		)
		self.client.force_authenticate(user=staff_user)

		self.assertEqual(self.client.get(list_url).status_code, status.HTTP_200_OK)
		self.assertEqual(self.client.get(detail_url).status_code, status.HTTP_200_OK)
		self.assertEqual(
			self.client.get("/api/users/999999/").status_code,
			status.HTTP_404_NOT_FOUND,
		)

	def test_cors_allows_only_local_frontend_origins(self):
		allowed_response = self.client.options(
			self.login_url,
			HTTP_ORIGIN="http://localhost:5173",
			HTTP_ACCESS_CONTROL_REQUEST_METHOD="POST",
		)
		blocked_response = self.client.options(
			self.login_url,
			HTTP_ORIGIN="https://untrusted.example",
			HTTP_ACCESS_CONTROL_REQUEST_METHOD="POST",
		)

		self.assertEqual(
			allowed_response["Access-Control-Allow-Origin"],
			"http://localhost:5173",
		)
		self.assertNotIn("Access-Control-Allow-Origin", blocked_response)
