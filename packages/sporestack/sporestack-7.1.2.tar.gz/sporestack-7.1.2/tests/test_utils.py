from sporestack import utils


def test_random_machine_id() -> None:
    assert utils.random_machine_id() != utils.random_machine_id()
    assert len(utils.random_machine_id()) == 32
    assert utils.random_machine_id().startswith("ss_m_")


def test_hash() -> None:
    assert utils.checksum("ss_m_1deadbeefcafedeadbeef1") == "0892"
