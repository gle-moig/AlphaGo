use std::ops::Not;

enum Player {
    None,
    White,
    Black
}

impl Not for Player {
    type Output = Self;

    fn not(self) -> self::Output{
        match self {
            Player::Black => Player::White,
            Player::White => Player::Black,
            Player::None => Player::None
        }
    }
}

struct State {
    size: u8,
    board: [u8; ..],
    captures: [u8; 2],
    history: Vec<u64>
}

impl State {
    fn new(size: u8) -> Self {
        const SIZE: u8 = size;
        State {
            size,
            board: [0; SIZE**2],
            captures: [0, 0],
            history: vec![]
        }
    }

    fn get_legal_moves(self) -> Vec<Option<u8>> {
    }
}