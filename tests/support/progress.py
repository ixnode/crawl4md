from collections.abc import Callable, Sequence
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
            print(f"\n[{index}/{total}] [{name}] ❌ ({duration_ms:.0f} ms)", flush=True)
            raise

        duration_ms = (time.perf_counter() - started_at) * 1000
        print(f"\n[{index}/{total}] [{name}] ✅ ({duration_ms:.0f} ms)", end="", flush=True)

    print(flush=True)
