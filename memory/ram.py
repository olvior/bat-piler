from typing import Optional


class RAM:
    available_addresses = list(range(239, -1, -1))  # addresses 239, 238 .. 0

    @staticmethod
    def free(address: int) -> None:
        RAM.available_addresses.append(address)
        RAM.available_addresses = sorted(RAM.available_addresses)

    @staticmethod
    def allocate(length: Optional[int] = None) -> int:
        if length is not None:
            if length == 0:
                raise ValueError("Length cannot be zero")
            memory_address = RAM.find_contiguous_memory(length)
            for i in range(length):
                RAM.available_addresses.remove(memory_address + i)
        else:
            memory_address = RAM.available_addresses.pop()

        return memory_address

    @staticmethod
    def find_contiguous_memory(amount: int) -> int:
        addresses = sorted(RAM.available_addresses)
        possible_memory_address: int = addresses[0]

        last_address: int = possible_memory_address - 1
        consecutive: int = 0

        for address in addresses:
            if last_address + 1 == address:
                consecutive += 1
                if consecutive == amount:
                    return possible_memory_address
            else:
                possible_memory_address = address
                consecutive = 1

            last_address = address

        raise ValueError(f"Failed to allocate {amount} consecutive addresses")
