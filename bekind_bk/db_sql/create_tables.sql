/* POSTS TABLE */
CREATE TABLE post(
   id SERIAL PRIMARY KEY,
   uuid UUID DEFAULT uuid_generate_v4(),
   title VARCHAR(50) NOT NULL,
   content TEXT NOT NULL,
   published BOOLEAN NOT NULL DEFAULT 'f',
   created_at TIMESTAMPTZ NOT NULL DEFAULT Now()
);