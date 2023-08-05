def binaryToDecimal(val):
    return int(str(val), 2)

def decimalToBinary(n):
    return bin(n).replace("0b", "")

def binaryToString(binary):
    str_data =' '
    for i in range(0, len(binary), 7):
        temp_data = int(binary[i:i + 7])

        decimal_data = binaryToDecimal(temp_data)

        str_data = str_data + chr(decimal_data)

    return str_data

def stringToBinary(val):
    return ' '.join(format(x, 'b') for x in bytearray(val, 'utf-8'))