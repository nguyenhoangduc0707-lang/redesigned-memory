import unittest

from src.database import get_db_connection


class TestDatabase(unittest.TestCase):
    def test_connection(self):
        conn = get_db_connection()
        self.assertIsNotNone(conn)
        conn.close()


if __name__ == "__main__":
    unittest.main()
