"""
Single hash table trie
"""

from typing import Any, Tuple, Dict, cast
import rocksdb
import orjson


TabKey = bytes
TabVal = Tuple[int, bool, Any]
Trie = Dict[TabKey, TabVal]
Member = Any
MemberWithPayload = Tuple[Member, Any]
ROW_KEY = 0
TERMINAL_KEY = 1
PAYLOAD_KEY = 2


def _first(i: MemberWithPayload) -> Member:
    return i[0]


def create_key(row_no: int, offset: int, member: Any) -> TabKey:
    """Create a key"""
    return f'{row_no}:{offset}:{member}'.encode("UTF-8")


def list_to_trie_db(
        members_with_payload: list[MemberWithPayload],
        db: Any) -> None:
    """Construct a trie from sorted members with payload."""
    if members_with_payload is None or len(members_with_payload) == 0:
        return None
    sorted_members_with_payload = sorted(members_with_payload, key=_first)
    for i, (members, payload) in enumerate(sorted_members_with_payload):
        row_no = 0
        for j, member in enumerate(members):
            is_terminal = len(members) == j + 1
            member = members[j]
            key: TabKey = create_key(row_no, j, member)
            val = db.get(key)
            if val is not None:
                parsed_val = orjson.loads(val)
                row_no = parsed_val[0]
            else:
                val = (i,
                       is_terminal,
                       payload if is_terminal else None)
                val_bytes = orjson.dumps(val)
                db.put(key, val_bytes, sync=True)
                row_no = i
    return None


def lookup(rock_db: Any,
           i: int,
           offset: int,
           member_part: Any) -> None | TabVal:
    """Lookup is done by searching an element of members in the tree."""
    key = create_key(i, offset, member_part)
    val = rock_db.get(key)
    if val is None:
        return None
    return cast(TabVal, orjson.loads(val))
