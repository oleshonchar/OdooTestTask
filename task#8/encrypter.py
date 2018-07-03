import threading
from queue import Queue


def get_content(input_file):
    with open(input_file, 'r') as f:
        content = f.read()
    return content


class Encrypter(threading.Thread):

    def __init__(self, queue, input_file, output_file):
        threading.Thread.__init__(self)
        self.queue = queue
        self.input_file = input_file
        self.output_file = output_file

    def run(self):
        while True:
            text = self.queue.get()
            self.execute_and_write(text, self.output_file)
            self.queue.task_done()

    def encryption_and_decryption(self, string, key=8):
        finished_string = ''
        for letter in string:
            finished_string += chr(ord(letter) ^ key)
        return finished_string

    def execute_and_write(self, string, output_file):
        with open(output_file, 'a') as o:
            encrypted = self.encryption_and_decryption(string)
            o.write(encrypted)


def main(input_file, output_file):
    queue = Queue()
    for i in range(4):
        t = Encrypter(queue, input_file, output_file)
        t.setDaemon(True)
        t.start()
    with open(input_file, 'r') as f:
        for i in range(4):
            text = f.read((len(get_content(input_file)) // 4) + 1)
            queue.put(text)
    queue.join()
    print('Done!')


if __name__ == "__main__":
    print('*' * 45)
    print('|\tЯ умею кодировать и декодировать файлы\t|')
    print('*' * 45)
    print('Вставьте файл с расширением *.txt в папку со скриптом')
    print()
    input_file = input('Введите название файла для кодирования/декодирования: ')
    output_file = input('Введите название файла для выходной информции: ')
    main(input_file, output_file)


