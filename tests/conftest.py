from pathlib import Path


BASE_DIR = Path(__file__).parent.parent

TEST_DB = BASE_DIR / 'test_db'
print(TEST_DB)
