from unittest.mock import patch
from project import new_member, delete_member, edit_member

def test_new_member():
    with patch("builtins.input", side_effect=["asad", "25", "monthly", "basic"]):
        assert new_member() == "Member Created Successfully!"

def test_delete_member():
    with patch("builtins.input", side_effect=["808"]):
        assert delete_member() == "Member deleted successfully!"

def test_edit_member():
    with patch("builtins.input", side_effect=["1", "611", "yousaf", "25"]):
        assert edit_member() == "Changes Made Successfully!"