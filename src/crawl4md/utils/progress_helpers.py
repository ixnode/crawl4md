import sys
import time


def print_progress(
    index: int,
    total: int,
    name: str,
    success: bool,
    started_at: float,
    *,
    index_width: int,
    name_width: int,
) -> None:
    duration_ms = (time.perf_counter() - started_at) * 1000
    status = "✅" if success else "❌"
    index_text = f"[{index:>{index_width}}/{total}]"
    name_text = f"[{name}]"
    duration_text = f"({duration_ms:>5.0f} ms)"
    print(
        f"{index_text} {name_text:<{name_width + 2}}  {status} {duration_text}",
        file=sys.stderr,
        flush=True,
    )
