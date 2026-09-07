import time

from fastapi import Request


async def timing_middleware(
    request: Request,
    call_next
):

    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = (
        time.perf_counter() - start_time
    )

    response.headers[
        "X-Process-Time"
    ] = f"{process_time:.4f}"

    return response