class MovesRegistry:
    _registry = {}

    @classmethod
    def register(cls, piece_type, move_class):
        cls._registry[piece_type] = move_class

    @classmethod
    def get_move(cls, piece_type):
        return cls._registry.get(piece_type)
