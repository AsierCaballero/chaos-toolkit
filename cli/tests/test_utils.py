"""Tests for chaos_toolkit.utils module."""

from chaos_toolkit.utils import validate_k8s_name, merge_dicts


class TestValidateK8sName:
    def test_valid_names(self):
        assert validate_k8s_name("my-deployment")
        assert validate_k8s_name("app-1")
        assert validate_k8s_name("a")

    def test_invalid_names(self):
        assert not validate_k8s_name("MyDeployment")
        assert not validate_k8s_name("-leading")
        assert not validate_k8s_name("trailing-")
        assert not validate_k8s_name("name with spaces")
        assert not validate_k8s_name("UPPERCASE")


class TestMergeDicts:
    def test_merge_simple(self):
        base = {"a": 1, "b": 2}
        override = {"b": 3, "c": 4}
        result = merge_dicts(base, override)
        assert result == {"a": 1, "b": 3, "c": 4}

    def test_merge_nested(self):
        base = {"app": {"name": "test", "port": 8080}}
        override = {"app": {"port": 9090, "debug": True}}
        result = merge_dicts(base, override)
        assert result["app"]["name"] == "test"
        assert result["app"]["port"] == 9090
        assert result["app"]["debug"] is True

    def test_merge_does_not_mutate_base(self):
        base = {"a": [1, 2]}
        override = {"a": [3, 4]}
        result = merge_dicts(base, override)
        assert result["a"] == [3, 4]
        assert base["a"] == [1, 2]
