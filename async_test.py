import asyncio
from time import sleep


async  def main():
    print('main')
    await asyncio.sleep(1)
    print('main2')

async  def main1():
    print('main1')

if __name__ == '__main__':
    event_loop = asyncio.new_event_loop()
    tasks = [event_loop.create_task(main()), event_loop.create_task(main1())]
    wait_task = asyncio.wait(tasks)
    event_loop.run_until_complete(wait_task)
    event_loop.close()
