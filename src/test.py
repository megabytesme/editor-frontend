import unittest
from flask_testing import TestCase
from app import app

class TestSaveAndRecallText(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_save_text(self):
        response = self.client.post('/save', json={'text': 'It was the best of cloud, it was the worst of cloud...'})
        self.assertEqual(response.status_code, 201)
        data = response.json
        self.assertIn('identifier', data)

    def test_recall_text(self):
        response_save = self.client.post('/save', json={'text': 'It was the best of cloud, it was the worst of cloud...'})
        self.assertEqual(response_save.status_code, 201)
        identifier = response_save.json['identifier']
        response_recall = self.client.get(f'/recall/{identifier}')
        self.assertEqual(response_recall.status_code, 200)
        data = response_recall.json
        self.assertEqual(data['text'], 'It was the best of cloud, it was the worst of cloud...')

    def test_recall_nonexistent_text(self):
        response = self.client.get('/recall/nonexistent-identifier')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Text not found')

if __name__ == '__main__':
    unittest.main()
