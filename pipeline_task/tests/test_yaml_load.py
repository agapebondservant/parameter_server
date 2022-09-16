import unittest
import yaml


class TestYamlLoad(unittest.TestCase):

    def test_load(self):
        with open('pipeline_task/tests/data/data_task1.yaml', 'r') as file:
            docs = yaml.safe_load_all(file)
            for doc in docs:
                print(doc.get('task'))
                self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
