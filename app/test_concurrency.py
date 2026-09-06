import asyncio
import time

async def task(name:str):
    print(f"{name} started")

    await asyncio.sleep(2)

    print(f"{name} finished")


async def sequential():

    start = time.perf_counter()

    await task("Task 1")
    await task("Task 2")
    await task("Task 3")

    end = time.perf_counter()

    print(f"Finished Sequential tasks in {round(end - start, 2)} second(s)")


async def concurrent():

    start = time.perf_counter()

    await asyncio.gather(
        task("Task 1"),
        task("Task 2"),
        task("Task 3")
    )

    end = time.perf_counter()

    print(f"Finished Concurrent tasks in {round(end - start, 2)} second(s)")

async def main():

    print("Sequential")
    await sequential()

    print("Concurrent")
    await concurrent()

asyncio.run(main())
    