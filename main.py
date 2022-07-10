from time import sleep

from vk import Vk

if __name__ == "__main__":
    vk = Vk()
    author_id = int(input("Author ID input: "))
    while True:
        streams = vk.get_new_streams(author_id)
        for stream in streams:
            print(f"Началась трансляция {stream['title']}. Ссылка: {stream['player']}")
        sleep(60)
