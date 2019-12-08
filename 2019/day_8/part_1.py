if __name__ == '__main__':
    image = open('input').readline()
    layers = [(image[i:i + 150]) for i in range(0, len(image), 150)]
    fewest_zeros_layer = min(layers, key=lambda l: l.count('0'))
    print(fewest_zeros_layer.count('1') * fewest_zeros_layer.count('2'))
    a = 42
