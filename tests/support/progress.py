from collections.abc import Awaitable, Callable, Sequence
import sys
import time


def run_progress_cases(
    names: Sequence[str],
    run_case: Callable[[int], None],
) -> None:
    total = len(names)

    for index, name in enumerate(names, start=1):
        started_at = time.perf_counter()
        try:
            run_case(index - 1)
        except Exception:
            duration_ms = (time.perf_counter() - started_at) * 1000
            print(f"[{index}/{total}] [{name}] ❌ ({duration_ms:.0f} ms)", file=sys.stderr, flush=True)
            raise

        duration_ms = (time.perf_counter() - started_at) * 1000
        print(f"[{index}/{total}] [{name}] ✅ ({duration_ms:.0f} ms)", file=sys.stderr, flush=True)


async def run_progress_cases_async(
    names: Sequence[str],
    run_case: Callable[[int], Awaitable[None]],
) -> None:
    total = len(names)

    for index, name in enumerate(names, start=1):
        started_at = time.perf_counter()
        try:
            await run_case(index - 1)
        except Exception:
            duration_ms = (time.perf_counter() - started_at) * 1000
            print(f"[{index}/{total}] [{name}] ❌ ({duration_ms:.0f} ms)", file=sys.stderr, flush=True)
            raise

        duration_ms = (time.perf_counter() - started_at) * 1000
        print(f"[{index}/{total}] [{name}] ✅ ({duration_ms:.0f} ms)", file=sys.stderr, flush=True)
