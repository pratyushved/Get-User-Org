import unittest
from unittest.mock import MagicMock, create_autospec
from sqlalchemy.orm import Session
from repository.crud import get_user, create_user
from models.models import User
from models.schemas import ItemBase


class TestCrud(unittest.TestCase):

  def setUp(self) -> None:
    self.mock_db_session = create_autospec(Session, instance=True)

  def test_get_user(self) -> None:
    self.mock_db_session.query.return_value.all.return_value = [User(id=1, name='Collance')]
    result = get_user(self.mock_db_session)
    self.assertEqual(len(result), 1)
    self.assertEqual(result[0].id, 1)
    self.assertEqual(result[0].name, 'Collance')

  def test_create_user(self) -> None:
    new_org = ItemBase(name='CCMG')
    self.mock_db_session.add = MagicMock()
    self.mock_db_session.commit = MagicMock()
    self.mock_db_session.refresh = MagicMock()
    created_org = create_user(self.mock_db_session, new_org)
    self.mock_db_session.add.assert_called_with(new_org)
    self.mock_db_session.commit.assert_called_once()
    self.mock_db_session.refresh.assert_called_with(new_org)
    self.assertEqual(created_org, new_org)


if __name__ == '__main__':
  unittest.main(verbosity=1)
