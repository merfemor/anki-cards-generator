import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


async def retry_async(
    operation: Callable[[], Awaitable[T]],
    *,
    should_retry: Callable[[BaseException], bool],
    max_attempts: int = 3,
    wait_multiplier: float = 1,
    max_wait: float = 2,
) -> T:
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    if wait_multiplier < 0 or max_wait < 0:
        raise ValueError("wait_multiplier and max_wait must be non-negative")

    attempt = 1
    while True:
        try:
            return await operation()
        except Exception as error:
            if attempt >= max_attempts or not should_retry(error):
                raise

            delay = min(wait_multiplier * 2 ** (attempt - 1), max_wait)
            logging.warning(
                "Retryable request failed; retrying attempt %s/%s in %s seconds",
                attempt + 1,
                max_attempts,
                delay,
            )
            await asyncio.sleep(delay)
            attempt += 1
