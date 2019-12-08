def apply_layer(image, layer):
    return ''.join(l if p == '2' else p for p, l in zip(image, layer))


if __name__ == '__main__':
    image = open('input').readline()
    layers = [(image[i:i + 150]) for i in range(0, len(image), 150)]
    result = layers[0]

    for layer in layers:
        result = apply_layer(result, layer)

    for r in [(result[i:i + 25]) for i in range(0, len(result), 25)]:
        print(r.replace('0', ' ').replace('1', 'o'))
