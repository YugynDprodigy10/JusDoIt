
class TestGenAIAdvice(unittest.TestCase):

    @patch("data_fetcher.vertexai.init")
    @patch("data_fetcher.get_user_profile")
    @patch("data_fetcher.GenerativeModel")
    def test_genai_advice_format(self, mock_model_class, mock_get_user_profile, mock_vertexai_init):
        # Mock user profile
        mock_get_user_profile.return_value = {
            "userID": "user1",
            "Name": "Remi",
            "Username": "remi_the_rems",
            "DateOfBirth": "1990-01-01",
            "ImageUrl": "https://someurl.com/pic.jpg",
            "Friends": []
        }

        # Set up mock for Gemini model
        mock_model_instance = MagicMock()
        
        # Ensure generate_content().text.strip() returns the expected string
        mock_generate_result = MagicMock()
        mock_generate_result.text.strip.return_value = "Keep pushing forward!"
        mock_model_instance.generate_content.return_value = mock_generate_result

        mock_model_class.return_value = mock_model_instance

        # Call the function
        result = get_genai_advice("user1")

        # DEBUG print (optional)
        print("DEBUG Final Result:", result)

        # Assert structure
        self.assertIn("advice_id", result)
        self.assertIn("timestamp", result)
        self.assertIn("content", result)
        self.assertIn("image", result)
        self.assertEqual(result["content"], "Keep pushing forward!")


