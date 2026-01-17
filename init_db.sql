CREATE TABLE IF NOT EXISTS rooms_room (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bookings_booking (
    id BIGSERIAL PRIMARY KEY,
    room_id BIGINT NOT NULL,
    date_start DATE NOT NULL,
    date_end DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_room
        FOREIGN KEY(room_id)
        REFERENCES rooms_room(id)
        ON DELETE CASCADE,
    CONSTRAINT check_dates
        CHECK (date_end > date_start),
    CONSTRAINT check_not_past_dates
        CHECK (date_start >= CURRENT_DATE)
);

CREATE INDEX IF NOT EXISTS idx_rooms_price ON rooms_room(price);
CREATE INDEX IF NOT EXISTS idx_rooms_created_at ON rooms_room(created_at);
CREATE INDEX IF NOT EXISTS idx_rooms_name ON rooms_room(name);

CREATE INDEX IF NOT EXISTS idx_bookings_room_dates 
    ON bookings_booking(room_id, date_start, date_end);

CREATE INDEX IF NOT EXISTS idx_bookings_date_start 
    ON bookings_booking(date_start);

COMMENT ON TABLE rooms_room IS 'Таблица номеров отеля';
COMMENT ON TABLE bookings_booking IS 'Таблица бронирований номеров';

COMMENT ON COLUMN rooms_room.name IS 'Название номера';
COMMENT ON COLUMN rooms_room.description IS 'Текстовое описание номера';
COMMENT ON COLUMN rooms_room.price IS 'Цена за ночь';
COMMENT ON COLUMN rooms_room.created_at IS 'Дата добавления номера';

COMMENT ON COLUMN bookings_booking.room_id IS 'ID номера отеля';
COMMENT ON COLUMN bookings_booking.date_start IS 'Дата начала брони';
COMMENT ON COLUMN bookings_booking.date_end IS 'Дата окончания брони';
