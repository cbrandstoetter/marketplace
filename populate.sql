INSERT INTO USER (id, name, password_hash) VALUES 
-- (1, 'demo_user', 'scrypt:32768:8:1$6xqrAkPQoaMLpwkT$8e40e2734a5668dd587a49d90b88350f9b0f8bf1d1856d2bcc4353bb47fc0afa88bdbdcd4fb5195f2f9452ec4e27740a6634b45b2b86c8c072dbf315ba18b70d'),
-- (3, 'Lisa', 'scrypt:32768:8:1$Bc9kwY31YEnObeJ0$869bf4d3c51cc7896edf2cdd38a82b8562ef01d517391c7de66663b9c7bb2626d3ef409e731a4802a88c0dbfb78ef487030b0f7ed774379775fea57a86f79e8c'),
(1, 'Christoph', 'scrypt:32768:8:1$WhgITJTzdjGHKW22$cf2ce3b6178ea76cd65789dc7fe3a48077130b2a71239113ef985ef7197bf7e70e982364611670973e362bd2de489c5434b0ed67db3c5499fbd84dbdaa02ff8f');



INSERT INTO Listings (category, name, image, description, price, user_id) VALUES
('', 'Welcome', 'happy.jpeg', 'This listing was created or the welcome message. It is not for sale ;)', 0, 1),
('Sports', 'Basketball', 'demo-items/basketball.png', 'Official size basketball for indoor and outdoor use.', 14.99, 1),
('Sports', 'Football', 'demo-items/football.png', 'Sturdy leather football, great for weekend matches.', 17.50, 1),
('Toys', 'Rocking Horse', 'demo-items/rocking-horse.png', 'Wooden rocking horse, safe and fun for toddlers.', 29.99, 1),
('Clothing', 'T-Shirt', 'demo-items/tshirt.png', 'Cotton T-shirt, size M, with a cool print.', 9.99, 1),
('Toys', 'Teddy Bear', 'demo-items/bear.jpg', 'Soft plush teddy bear, 30cm tall.', 8.50, 1),
('Music', 'Guitar', 'demo-items/guitar.png', 'Acoustic guitar for beginners.', 59.99, 1),
('Music', 'Saxophone', 'demo-items/saxophone.png', 'Used saxophone, in good condition.', 120.00, 1),
('Accessories', 'Watch', 'demo-items/watch.png', 'Elegant wristwatch with leather strap.', 45.00, 1),
('Clothing', 'Boots', 'demo-items/boots.jpeg', 'Waterproof hiking boots, size 42.', 35.00, 1),
('Electronics', 'Laptop', 'demo-items/laptop.png', 'Used laptop, 8GB RAM, 256GB SSD.', 299.99, 1),
('Tools', 'Screwdriver', 'demo-items/screwdriver.png', 'Multi-bit screwdriver for home repairs.', 6.50, 1),
('Garden', 'Wheelbarrow', 'demo-items/wheelbarrow.png', 'Heavy-duty wheelbarrow for gardening.', 49.99, 1),
('Vehicles', 'Car Toy', 'demo-items/car.png', 'Remote-controlled car with rechargeable battery.', 24.99, 1),
('Vehicles', 'Motorcycle Toy', 'demo-items/motorcycle.png', 'Miniature model motorcycle, great for collectors.', 19.99, 1),
('Electronics', 'Smartphone', 'demo-items/smartphone.png', 'Android smartphone, slightly used.', 99.99, 1),
('Furniture', 'Chair', 'demo-items/chair.png', 'Simple wooden chair, light and sturdy.', 12.00, 1),
('Music', 'Piano', 'demo-items/piano.jpeg', 'Electric piano with stand and bench.', 199.00, 1),
('Accessories', 'Sunglasses', 'demo-items/sunglasses.png', 'UV-protective stylish sunglasses.', 15.00, 1),
('Clothing', 'Doc Martens', 'demo-items/doc-marten.png', 'Classic Doc Martens boots, size 43.', 70.00, 1),
('Electronics', 'Printer', 'demo-items/printer.png', 'Wireless inkjet printer.', 39.00, 1),
('Vehicles', 'Toy Truck', 'demo-items/truck.png', 'Plastic dump truck toy for kids.', 10.99, 1),

('Toys', 'Puzzle Set', 'default_listings_image.png', '500-piece jigsaw puzzle for family fun.', 12.99, 1),
('Tools', 'Hammer', 'default_listings_image.png', 'Durable steel hammer with rubber grip.', 8.75, 1),
('Electronics', 'Tablet', 'default_listings_image.png', '10-inch Android tablet with charger.', 85.00, 1),
('Books', 'Cookbook', 'default_listings_image.png', 'Vegetarian recipes from around the world.', 6.00, 1),
('Decor', 'Wall Clock', 'default_listings_image.png', 'Minimalist wall clock, runs silently.', 13.50, 1);



