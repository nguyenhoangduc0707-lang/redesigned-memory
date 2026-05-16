import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db_connection  # giả sử bạn có hàm này

class TestDatabase(unittest.TestCase):
    def test_connection(self):
        conn = get_db_connection()
        self.assertIsNotNone(conn)
        conn.close()

if __name__ == '__main__':
    unittest.main()
