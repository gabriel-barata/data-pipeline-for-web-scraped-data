CREATE TABLE IF NOT EXISTS tbHairProd (

    id SERIAL PRIMARY KEY,
    product TEXT,
    brand TEXT,
    description TEXT,
    price FLOAT(2),
    vol VARCHAR(50)
    
)