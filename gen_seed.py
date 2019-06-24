import random

print("Generating Wallet Seed")
full_wallet_seed = hex(random.SystemRandom().getrandbits(256))
wallet_seed = full_wallet_seed[2:].upper()
print("Wallet Seed (make a copy of this in a safe place!): ", wallet_seed)
print(len(wallet_seed))
print("Done")
