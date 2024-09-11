from encoder import encoder

# Specify the path to your image file
file_path = "./test/krabs.png"

# Call the encoder function
encoded_pgn = encoder(file_path)

# Optionally, print the encoded PGN
print(encoded_pgn)