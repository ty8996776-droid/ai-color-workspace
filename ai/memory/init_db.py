from ai.memory.store import MemoryStore


def main() -> None:
    store = MemoryStore()
    store.init_db()
    print("AI Color Workspace V2 memory database initialized.")


if __name__ == "__main__":
    main()
