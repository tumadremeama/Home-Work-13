import asyncio


async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования.')

    for ball_number in range(1, 6):
        await asyncio.sleep(1 / power)
        print(f'Силач {name} поднял {ball_number} шар.')

    print(f'Силач {name} законкил соревнованя.')


async def start_tournament():
    tasks = [
        start_strongman('Паша', 3),
        start_strongman('Денис', 4),
        start_strongman('Аполлон', 5)
    ]

    await asyncio.gather(*tasks)

asyncio.run(start_tournament())