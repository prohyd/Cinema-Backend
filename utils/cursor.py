import base64
import json
from datetime import datetime
from uuid import UUID


def encode_cursor(created_at: datetime, id_movie: UUID):
    payload = {
        "created_at": created_at.isoformat(),
        "id_movie": id_movie
    }
    raw = json.dumps(payload).encode()
    return base64.urlsafe_b64encode(raw).decode()


def decode_cursor(cursor: str) -> tuple[datetime, int]:
    raw = base64.urlsafe_b64decode(cursor.encode())
    data = json.loads(raw)
    return datetime.fromisoformat(data["created_at"]), data["id_movie"]