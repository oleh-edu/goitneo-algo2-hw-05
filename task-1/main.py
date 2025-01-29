#!/usr/bin/env python

import mmh3
import bitarray

class BloomFilter:
    def __init__(self, size: int, num_hashes: int):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = bitarray.bitarray(size)
        self.bit_array.setall(0)

    def _hashes(self, item: str):
        """Generates num_hashes of hashes for the item string."""
        return [mmh3.hash(item, seed) % self.size for seed in range(self.num_hashes)]

    def add(self, item: str):
        """Adds an element to the Bloom filter."""
        for index in self._hashes(item):
            self.bit_array[index] = 1

    def check(self, item: str) -> bool:
        """Checks if an element can be in a Bloom filter."""
        return all(self.bit_array[index] for index in self._hashes(item))

def check_password_uniqueness(bloom_filter: BloomFilter, passwords: list) -> dict:
    """Checks a list of passwords for uniqueness using a Bloom filter."""
    results = {}
    for password in passwords:
        if not isinstance(password, str) or not password.strip():
            results[password] = "Incorrect password"
            continue
        
        if bloom_filter.check(password):
            results[password] = "Possibly used"
        else:
            results[password] = "Unique"
            bloom_filter.add(password)  # Add a new password to the filter
    
    return results

if __name__ == "__main__":
    # Initializing the Bloom filter
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Adding existing passwords
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Checking new passwords
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest", "", None, 12345]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Displaying the results
    for password, status in results.items():
        print(f"Password '{password}' - {status}.")
