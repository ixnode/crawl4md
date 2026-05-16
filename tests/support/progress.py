# This file is part of the https://github.com/ixnode/crawl4md project.
#
# (c) 2026 Björn Hempel <bjoern@hempel.li>
#
# For the full copyright and license information, please view the LICENSE.md
# file that was distributed with this source code.
#
# @author: Björn Hempel <bjoern@hempel.li>
# @version: 1.0.0 (2026-05-16)
# @since 1.0.0 (2026-05-16) First version

import asyncio
import sys
import time

from collections.abc import Awaitable, Callable, Sequence


def _print_progress(
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


def run_progress_cases(
    names: Sequence[str],
    run_case: Callable[[int], None],
) -> None:
    async def _run_case(index: int) -> None:
        run_case(index)

    asyncio.run(run_progress_cases_async(names, _run_case))


async def run_progress_cases_async(
    names: Sequence[str],
    run_case: Callable[[int], Awaitable[None]],
) -> None:
    total = len(names)
    index_width = len(str(total))
    name_width = max((len(name) for name in names), default=0)

    for index, name in enumerate(names, start=1):
        started_at = time.perf_counter()
        try:
            await run_case(index - 1)
        except Exception:
            _print_progress(
                index,
                total,
                name,
                False,
                started_at,
                index_width=index_width,
                name_width=name_width,
            )
            raise

        _print_progress(
            index,
            total,
            name,
            True,
            started_at,
            index_width=index_width,
            name_width=name_width,
        )
