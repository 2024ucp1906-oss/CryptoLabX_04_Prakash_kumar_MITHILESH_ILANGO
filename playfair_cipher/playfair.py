from collections import Counter


# Generate the 5x5 Playfair key matrix
def generate_key_matrix(key):
    key = key.upper().replace("J", "I")

    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    letters = ""

    # Add letters from the keyword
    for ch in key:
        if ch in alphabet and ch not in letters:
            letters += ch

    # Add remaining alphabet letters
    for ch in alphabet:
        if ch not in letters:
            letters += ch

    # Create 5x5 matrix
    matrix = []

    for i in range(0, 25, 5):
        matrix.append(list(letters[i:i + 5]))

    return matrix


# Prepare plaintext into digraphs
def prepare_plaintext(text):
    text = text.upper().replace("J", "I")

    # Keep only alphabets
    text = "".join(ch for ch in text if ch.isalpha())

    pairs = []
    i = 0

    while i < len(text):

        # Last single character
        if i == len(text) - 1:
            pairs.append(text[i] + "X")
            i += 1

        # Repeated letters
        elif text[i] == text[i + 1]:
            pairs.append(text[i] + "X")
            i += 1

        # Normal pair
        else:
            pairs.append(text[i] + text[i + 1])
            i += 2

    return pairs


# Find row and column of a letter
def find_position(matrix, letter):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == letter:
                return row, col


# Encrypt one digraph
def encrypt_digraph(pair, matrix):

    r1, c1 = find_position(matrix, pair[0])
    r2, c2 = find_position(matrix, pair[1])

    # Same row
    if r1 == r2:
        first = matrix[r1][(c1 + 1) % 5]
        second = matrix[r2][(c2 + 1) % 5]

        return first + second

    # Same column
    elif c1 == c2:
        first = matrix[(r1 + 1) % 5][c1]
        second = matrix[(r2 + 1) % 5][c2]

        return first + second

    # Rectangle rule
    else:
        first = matrix[r1][c2]
        second = matrix[r2][c1]

        return first + second


# Decrypt one digraph
def decrypt_digraph(pair, matrix):

    r1, c1 = find_position(matrix, pair[0])
    r2, c2 = find_position(matrix, pair[1])

    # Same row
    if r1 == r2:
        first = matrix[r1][(c1 - 1) % 5]
        second = matrix[r2][(c2 - 1) % 5]

        return first + second

    # Same column
    elif c1 == c2:
        first = matrix[(r1 - 1) % 5][c1]
        second = matrix[(r2 - 1) % 5][c2]

        return first + second

    # Rectangle rule
    else:
        first = matrix[r1][c2]
        second = matrix[r2][c1]

        return first + second


# Encrypt complete plaintext
def playfair_encrypt(plaintext, matrix):

    pairs = prepare_plaintext(plaintext)

    ciphertext = ""

    for pair in pairs:
        ciphertext += encrypt_digraph(pair, matrix)

    return ciphertext


# Decrypt complete ciphertext
def playfair_decrypt(ciphertext, matrix):

    plaintext = ""

    for i in range(0, len(ciphertext), 2):

        pair = ciphertext[i:i + 2]

        plaintext += decrypt_digraph(pair, matrix)

    return plaintext


# Perform bigram frequency analysis
def digraph_frequency(ciphertext):

    pairs = []

    for i in range(0, len(ciphertext), 2):
        pairs.append(ciphertext[i:i + 2])

    return Counter(pairs)


# Verify encryption
def verify(plaintext, ciphertext, matrix):

    new_ciphertext = playfair_encrypt(plaintext, matrix)

    if new_ciphertext == ciphertext:
        return "SUCCESS"

    return "FAILED"


# Main program
def main():

    # Assignment keyword
    keyword = "COMPUTER"

    # Read plaintext from file
    with open("plaintext.txt", "r") as file:
        plaintext = file.read().strip()

    # Generate key matrix
    matrix = generate_key_matrix(keyword)

    print("Keyword:", keyword)

    # Display key matrix
    print("\nKey Matrix:")

    for row in matrix:
        print(" ".join(row))

    # Prepare plaintext
    pairs = prepare_plaintext(plaintext)

    print("\nPrepared Digraphs:")
    print(" ".join(pairs))

    # Encryption
    ciphertext = playfair_encrypt(plaintext, matrix)

    print("\nCiphertext:")
    print(ciphertext)

    # Decryption
    decrypted_text = playfair_decrypt(ciphertext, matrix)

    print("\nDecrypted Text:")
    print(decrypted_text)

    # Bigram frequency analysis
    print("\nBigram Frequency:")

    frequency = digraph_frequency(ciphertext)

    for pair, count in frequency.items():
        print(pair, ":", count)

    # Verification
    print("\nVerification:")
    print(verify(plaintext, ciphertext, matrix))


# Run program
if __name__ == "__main__":
    main()
