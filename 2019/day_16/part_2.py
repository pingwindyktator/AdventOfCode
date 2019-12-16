if __name__ == '__main__':
    input_signal = list(map(int, open('input').readline())) * 10000
    msg_offset = int(''.join(map(str, input_signal[:7])))
    input_signal = input_signal[msg_offset:]
    for _ in range(100):
        for i in range(len(input_signal) - 2, -1, -1):
            input_signal[i] = (input_signal[i] + input_signal[i + 1]) % 10

    print(''.join(map(str, input_signal))[:8])
