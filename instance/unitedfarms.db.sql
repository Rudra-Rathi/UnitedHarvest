BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER NOT NULL,
	"username"	VARCHAR(64) NOT NULL,
	"email"	VARCHAR(120) NOT NULL,
	"password_hash"	VARCHAR(256) NOT NULL,
	"full_name"	VARCHAR(100) NOT NULL,
	"phone"	VARCHAR(20) NOT NULL,
	"address"	VARCHAR(200) NOT NULL,
	"role"	VARCHAR(10) NOT NULL,
	"is_verified"	BOOLEAN,
	"created_at"	DATETIME,
	UNIQUE("email"),
	UNIQUE("username"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "farmer_verification" (
	"id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"license_number"	VARCHAR(50) NOT NULL,
	"license_image_path"	VARCHAR(200) NOT NULL,
	"status"	VARCHAR(20),
	"created_at"	DATETIME,
	"reviewed_at"	DATETIME,
	"reviewer_notes"	TEXT,
	FOREIGN KEY("user_id") REFERENCES "user"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "product" (
	"id"	INTEGER NOT NULL,
	"farmer_id"	INTEGER NOT NULL,
	"name"	VARCHAR(100) NOT NULL,
	"category"	VARCHAR(50) NOT NULL,
	"description"	TEXT,
	"price_per_kg"	FLOAT NOT NULL,
	"available_quantity"	FLOAT NOT NULL,
	"unit"	VARCHAR(10),
	"is_available"	BOOLEAN,
	"created_at"	DATETIME,
	"updated_at"	DATETIME,
	FOREIGN KEY("farmer_id") REFERENCES "user"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "order" (
	"id"	INTEGER NOT NULL,
	"order_number"	VARCHAR(20) NOT NULL,
	"vendor_id"	INTEGER NOT NULL,
	"farmer_id"	INTEGER NOT NULL,
	"total_amount"	FLOAT NOT NULL,
	"commission_amount"	FLOAT NOT NULL,
	"farmer_payout"	FLOAT NOT NULL,
	"status"	VARCHAR(20),
	"created_at"	DATETIME,
	"updated_at"	DATETIME,
	FOREIGN KEY("vendor_id") REFERENCES "user"("id"),
	FOREIGN KEY("farmer_id") REFERENCES "user"("id"),
	UNIQUE("order_number"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "product_price_history" (
	"id"	INTEGER NOT NULL,
	"product_id"	INTEGER NOT NULL,
	"price"	FLOAT NOT NULL,
	"date"	DATETIME,
	FOREIGN KEY("product_id") REFERENCES "product"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "order_item" (
	"id"	INTEGER NOT NULL,
	"order_id"	INTEGER NOT NULL,
	"product_id"	INTEGER NOT NULL,
	"quantity"	FLOAT NOT NULL,
	"unit_price"	FLOAT NOT NULL,
	"total_price"	FLOAT NOT NULL,
	FOREIGN KEY("order_id") REFERENCES "order"("id"),
	FOREIGN KEY("product_id") REFERENCES "product"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "negotiation" (
	"id"	INTEGER NOT NULL,
	"order_id"	INTEGER NOT NULL,
	"proposed_by"	VARCHAR(10) NOT NULL,
	"proposed_price"	FLOAT NOT NULL,
	"status"	VARCHAR(20),
	"message"	TEXT,
	"created_at"	DATETIME,
	"responded_at"	DATETIME,
	FOREIGN KEY("order_id") REFERENCES "order"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "rating" (
	"id"	INTEGER NOT NULL,
	"rater_id"	INTEGER NOT NULL,
	"ratee_id"	INTEGER NOT NULL,
	"order_id"	INTEGER NOT NULL,
	"rating"	INTEGER NOT NULL,
	"review"	TEXT,
	"created_at"	DATETIME,
	FOREIGN KEY("rater_id") REFERENCES "user"("id"),
	FOREIGN KEY("ratee_id") REFERENCES "user"("id"),
	FOREIGN KEY("order_id") REFERENCES "order"("id"),
	PRIMARY KEY("id")
);
INSERT INTO "user" VALUES (1,'farmer0','farmer0@example.com','scrypt:32768:8:1$YhylMioVOlTW1fiT$cc9ef642d591fae2c5bf83e2cef1d3a4cadcf4ac54ab4accb66addca885117456e9be9b02013a859406e59c0e5f4e9ef2bebc5b2ddf6d41f22007736dac2dc6d','Farmer 0','9000000000','Village 0, India','farmer',1,'2025-05-12 10:09:44.348770');
INSERT INTO "user" VALUES (2,'farmer1','farmer1@example.com','scrypt:32768:8:1$uzRnty80XjqcJ6ev$893f586248b3d0839384570448a91fabdec20f2251ad1b41329194811bc2fa780e2e0a0ef2a69b8ec06876df92a2dacf8a21567686eb6065819fdb6a2c4e143a','Farmer 1','9000000001','Village 1, India','farmer',1,'2025-05-12 10:09:44.348773');
INSERT INTO "user" VALUES (3,'farmer2','farmer2@example.com','scrypt:32768:8:1$SU6kze5FNox8stIm$2722492eac0f9c2184e963431d70ae76b22307d3399a69072858fd0866b8b3b8b30de22f530d588e6645d9c01de1a1620de5a8dddcc4142b04f64adf910b5886','Farmer 2','9000000002','Village 2, India','farmer',1,'2025-05-12 10:09:44.348774');
INSERT INTO "user" VALUES (4,'farmer3','farmer3@example.com','scrypt:32768:8:1$pVt95GIuLM20LXLB$58368b3b2a9f36337796fc9081bc3da9365e73ecfba29f6dbc337be6e8752b0158b98bd18b1dd6ae5fb954eee5e3216d3fbb45e4c8159043d85938f474a657c0','Farmer 3','9000000003','Village 3, India','farmer',1,'2025-05-12 10:09:44.348775');
INSERT INTO "user" VALUES (5,'farmer4','farmer4@example.com','scrypt:32768:8:1$ujdSJMqYbBiPG0uz$049c626fc6090cc5b3dd67fcd79e2a05c42bd430543dd81f3177b902717a570c1583aba74c9ed107fd93d2858c344b4dde09ac9773537c36ecdf3d64ae39e053','Farmer 4','9000000004','Village 4, India','farmer',1,'2025-05-12 10:09:44.348776');
INSERT INTO "user" VALUES (6,'vendor0','vendor0@example.com','scrypt:32768:8:1$aipBxmtR8SjqoBqJ$15792edaa171ad2a23c021f39e2c6e09871b9b40ad0c1b62f6f91c97b31ac01f6816147b2ae26f3306f976c62ef2a3535ca968f8569a0579cf573cd3cee6a0dd','Vendor 0','8000000000','City 0, India','vendor',1,'2025-05-12 10:09:44.348777');
INSERT INTO "user" VALUES (7,'vendor1','vendor1@example.com','scrypt:32768:8:1$lLMUN2Ly83MCHRRm$b3275c87f55913d5c2811eb4162e1bbd30cec8cc7c5f2c2f6d24e7af22b831c8efa5bf6e9f2bb91e29b01598f6375c419a6a1718fb8b8fb68aca148c164ad6a1','Vendor 1','8000000001','City 1, India','vendor',1,'2025-05-12 10:09:44.348778');
INSERT INTO "user" VALUES (8,'vendor2','vendor2@example.com','scrypt:32768:8:1$HL7bVHNBSpoDHQUF$e51079bb9bcb65af39437763eddd5c4bff28d0a15d221270eb3a43cb013ca2fae5969658cc34bc3228e165182c6d3fed8afef42bdf20f1d0835440b37760adfc','Vendor 2','8000000002','City 2, India','vendor',1,'2025-05-12 10:09:44.348778');
INSERT INTO "user" VALUES (9,'vendor3','vendor3@example.com','scrypt:32768:8:1$CDcEMeIdlUxx8M6Z$3b7acf20f11a156484330b4e29fce7a87b1208fc6164000228db26539f5be0ac431fa9ff53817227d8785cffa5419f52a7b9c193f9e5374e368b83168ea63a28','Vendor 3','8000000003','City 3, India','vendor',1,'2025-05-12 10:09:44.348779');
INSERT INTO "user" VALUES (10,'vendor4','vendor4@example.com','scrypt:32768:8:1$QrSF1w7RYWX3ypcT$c1aba023825f5876d8f342fbedcaa8ed690e1ee24cbb55ad18bca6795a12bc2ed129ed632427bd17ed29fabb97faa915657b792d19534e93670ef21326bfe1c6','Vendor 4','8000000004','City 4, India','vendor',1,'2025-05-12 10:09:44.348780');
INSERT INTO "farmer_verification" VALUES (1,1,'LIC-0001','dummy_license.jpg','approved','2025-04-12 10:09:44.356771','2025-04-27 10:09:44.356987','Verified successfully');
INSERT INTO "farmer_verification" VALUES (2,2,'LIC-0002','dummy_license.jpg','approved','2025-04-12 10:09:44.357039','2025-04-27 10:09:44.357042','Verified successfully');
INSERT INTO "farmer_verification" VALUES (3,3,'LIC-0003','dummy_license.jpg','approved','2025-04-12 10:09:44.357057','2025-04-27 10:09:44.357058','Verified successfully');
INSERT INTO "farmer_verification" VALUES (4,4,'LIC-0004','dummy_license.jpg','approved','2025-04-12 10:09:44.357069','2025-04-27 10:09:44.357070','Verified successfully');
INSERT INTO "farmer_verification" VALUES (5,5,'LIC-0005','dummy_license.jpg','approved','2025-04-12 10:09:44.357081','2025-04-27 10:09:44.357082','Verified successfully');
INSERT INTO "product" VALUES (1,3,'Product 0','fruit','Description for product 0',30.92,118.12,'kg',1,'2025-05-08 10:09:44.360834','2025-05-10 10:09:44.360921');
INSERT INTO "product" VALUES (2,1,'Product 1','vegetable','Description for product 1',64.07,757.64,'kg',1,'2025-04-15 10:09:44.361224','2025-05-12 12:33:42.572221');
INSERT INTO "product" VALUES (3,5,'Product 2','vegetable','Description for product 2',41.97,192.84,'kg',1,'2025-04-14 10:09:44.361541','2025-05-04 10:09:44.361545');
INSERT INTO "product" VALUES (4,2,'Product 3','fruit','Description for product 3',40.65,649.16,'kg',1,'2025-04-18 10:09:44.361954','2025-05-07 10:09:44.361958');
INSERT INTO "product" VALUES (5,4,'Product 4','fruit','Description for product 4',54.01,636.94,'kg',1,'2025-04-26 10:09:44.362221','2025-05-12 10:09:44.362224');
INSERT INTO "product" VALUES (6,5,'Product 5','fruit','Description for product 5',33.78,269.9,'kg',1,'2025-05-08 10:09:44.362247','2025-05-12 10:09:44.362249');
INSERT INTO "product" VALUES (7,3,'Product 6','fruit','Description for product 6',63.46,323.28,'kg',1,'2025-05-01 10:09:44.362263','2025-05-11 10:09:44.362264');
INSERT INTO "product" VALUES (8,5,'Product 7','vegetable','Description for product 7',76.57,527.7,'kg',1,'2025-05-06 10:09:44.362277','2025-05-12 10:09:44.362278');
INSERT INTO "product" VALUES (9,5,'Product 8','vegetable','Description for product 8',20.75,712.88,'kg',1,'2025-04-26 10:09:44.362289','2025-05-11 10:09:44.362291');
INSERT INTO "product" VALUES (10,3,'Product 9','vegetable','Description for product 9',62.16,692.57,'kg',1,'2025-05-06 10:09:44.362302','2025-05-02 10:09:44.362303');
INSERT INTO "order" VALUES (1,'ORD00000',8,1,18577.2017,928.860085,17648.341615,'completed','2025-04-21 10:09:44.379165','2025-05-12 10:09:44.381867');
INSERT INTO "order" VALUES (2,'ORD00001',6,1,17574.7471,878.737355,16696.009745,'completed','2025-04-19 10:09:44.382204','2025-05-12 10:09:44.384143');
INSERT INTO "order" VALUES (3,'ORD00002',7,4,17685.2527,884.262635,16800.990065,'completed','2025-05-06 10:09:44.384540','2025-05-12 10:09:44.385309');
INSERT INTO "order" VALUES (4,'ORD00003',7,2,15654.6754,782.73377,14871.94163,'completed','2025-04-25 10:09:44.385861','2025-05-12 10:09:44.386976');
INSERT INTO "order" VALUES (5,'ORD00004',8,2,19269.945,963.49725,18306.44775,'completed','2025-04-22 10:09:44.386804','2025-05-12 10:09:44.387379');
INSERT INTO "order" VALUES (6,'ORD00005',9,2,14468.3462,723.41731,13744.92889,'completed','2025-04-25 10:09:44.387606','2025-05-12 10:09:44.388304');
INSERT INTO "order" VALUES (7,'ORD00006',7,1,20328.4906,1016.42453,19312.06607,'completed','2025-04-29 10:09:44.388110','2025-05-12 10:09:44.389157');
INSERT INTO "order" VALUES (8,'ORD00007',6,3,17928.2175,896.410875,17031.806625,'completed','2025-04-25 10:09:44.389420','2025-05-12 10:09:44.389846');
INSERT INTO "order" VALUES (9,'ORD00008',6,4,3076.3446,153.81723,2922.52737,'completed','2025-04-18 10:09:44.389690','2025-05-12 10:09:44.390144');
INSERT INTO "order" VALUES (10,'ORD00009',8,4,13207.959,660.39795,12547.56105,'completed','2025-04-26 10:09:44.389989','2025-05-12 10:09:44.390631');
INSERT INTO "order" VALUES (11,'UF-20250512-45EE',6,5,19142.5,957.12,18185.38,'negotiating','2025-05-12 11:18:08.332879','2025-05-12 11:18:08.332885');
INSERT INTO "product_price_history" VALUES (1,1,29.74,'2025-05-02 10:09:44.366508');
INSERT INTO "product_price_history" VALUES (2,1,34.59,'2025-05-03 10:09:44.366576');
INSERT INTO "product_price_history" VALUES (3,1,33.97,'2025-05-04 10:09:44.366589');
INSERT INTO "product_price_history" VALUES (4,1,30.03,'2025-05-05 10:09:44.366601');
INSERT INTO "product_price_history" VALUES (5,1,30.5,'2025-05-06 10:09:44.366608');
INSERT INTO "product_price_history" VALUES (6,1,30.72,'2025-05-07 10:09:44.366614');
INSERT INTO "product_price_history" VALUES (7,1,27.21,'2025-05-08 10:09:44.366620');
INSERT INTO "product_price_history" VALUES (8,1,25.15,'2025-05-09 10:09:44.366627');
INSERT INTO "product_price_history" VALUES (9,1,29.14,'2025-05-10 10:09:44.366632');
INSERT INTO "product_price_history" VALUES (10,1,30.56,'2025-05-11 10:09:44.366638');
INSERT INTO "product_price_history" VALUES (11,2,74.26,'2025-05-02 10:09:44.367429');
INSERT INTO "product_price_history" VALUES (12,2,62.96,'2025-05-03 10:09:44.367446');
INSERT INTO "product_price_history" VALUES (13,2,62.39,'2025-05-04 10:09:44.367454');
INSERT INTO "product_price_history" VALUES (14,2,75.08,'2025-05-05 10:09:44.367459');
INSERT INTO "product_price_history" VALUES (15,2,66.99,'2025-05-06 10:09:44.367465');
INSERT INTO "product_price_history" VALUES (16,2,60.79,'2025-05-07 10:09:44.367471');
INSERT INTO "product_price_history" VALUES (17,2,67.37,'2025-05-08 10:09:44.367477');
INSERT INTO "product_price_history" VALUES (18,2,53.84,'2025-05-09 10:09:44.367482');
INSERT INTO "product_price_history" VALUES (19,2,73.84,'2025-05-10 10:09:44.367488');
INSERT INTO "product_price_history" VALUES (20,2,67.0,'2025-05-11 10:09:44.367494');
INSERT INTO "product_price_history" VALUES (21,3,47.63,'2025-05-02 10:09:44.367737');
INSERT INTO "product_price_history" VALUES (22,3,41.89,'2025-05-03 10:09:44.367749');
INSERT INTO "product_price_history" VALUES (23,3,41.87,'2025-05-04 10:09:44.367756');
INSERT INTO "product_price_history" VALUES (24,3,48.27,'2025-05-05 10:09:44.367762');
INSERT INTO "product_price_history" VALUES (25,3,36.23,'2025-05-06 10:09:44.367767');
INSERT INTO "product_price_history" VALUES (26,3,37.01,'2025-05-07 10:09:44.367773');
INSERT INTO "product_price_history" VALUES (27,3,46.69,'2025-05-08 10:09:44.367778');
INSERT INTO "product_price_history" VALUES (28,3,46.98,'2025-05-09 10:09:44.367784');
INSERT INTO "product_price_history" VALUES (29,3,48.47,'2025-05-10 10:09:44.368673');
INSERT INTO "product_price_history" VALUES (30,3,49.8,'2025-05-11 10:09:44.368691');
INSERT INTO "product_price_history" VALUES (31,4,45.43,'2025-05-02 10:09:44.369206');
INSERT INTO "product_price_history" VALUES (32,4,40.03,'2025-05-03 10:09:44.369229');
INSERT INTO "product_price_history" VALUES (33,4,44.54,'2025-05-04 10:09:44.369237');
INSERT INTO "product_price_history" VALUES (34,4,46.91,'2025-05-05 10:09:44.369245');
INSERT INTO "product_price_history" VALUES (35,4,37.23,'2025-05-06 10:09:44.369251');
INSERT INTO "product_price_history" VALUES (36,4,46.44,'2025-05-07 10:09:44.369256');
INSERT INTO "product_price_history" VALUES (37,4,44.31,'2025-05-08 10:09:44.369263');
INSERT INTO "product_price_history" VALUES (38,4,48.63,'2025-05-09 10:09:44.369269');
INSERT INTO "product_price_history" VALUES (39,4,44.7,'2025-05-10 10:09:44.369275');
INSERT INTO "product_price_history" VALUES (40,4,37.09,'2025-05-11 10:09:44.369281');
INSERT INTO "product_price_history" VALUES (41,5,43.84,'2025-05-02 10:09:44.369530');
INSERT INTO "product_price_history" VALUES (42,5,48.73,'2025-05-03 10:09:44.369544');
INSERT INTO "product_price_history" VALUES (43,5,58.76,'2025-05-04 10:09:44.369551');
INSERT INTO "product_price_history" VALUES (44,5,53.6,'2025-05-05 10:09:44.369557');
INSERT INTO "product_price_history" VALUES (45,5,45.87,'2025-05-06 10:09:44.369563');
INSERT INTO "product_price_history" VALUES (46,5,61.17,'2025-05-07 10:09:44.369569');
INSERT INTO "product_price_history" VALUES (47,5,57.47,'2025-05-08 10:09:44.369574');
INSERT INTO "product_price_history" VALUES (48,5,50.09,'2025-05-09 10:09:44.369579');
INSERT INTO "product_price_history" VALUES (49,5,49.61,'2025-05-10 10:09:44.369585');
INSERT INTO "product_price_history" VALUES (50,5,64.53,'2025-05-11 10:09:44.369590');
INSERT INTO "product_price_history" VALUES (51,6,30.87,'2025-05-02 10:09:44.369802');
INSERT INTO "product_price_history" VALUES (52,6,32.37,'2025-05-03 10:09:44.369814');
INSERT INTO "product_price_history" VALUES (53,6,35.28,'2025-05-04 10:09:44.369821');
INSERT INTO "product_price_history" VALUES (54,6,30.18,'2025-05-05 10:09:44.369827');
INSERT INTO "product_price_history" VALUES (55,6,32.81,'2025-05-06 10:09:44.369833');
INSERT INTO "product_price_history" VALUES (56,6,32.65,'2025-05-07 10:09:44.369838');
INSERT INTO "product_price_history" VALUES (57,6,33.85,'2025-05-08 10:09:44.369844');
INSERT INTO "product_price_history" VALUES (58,6,36.85,'2025-05-09 10:09:44.369849');
INSERT INTO "product_price_history" VALUES (59,6,35.05,'2025-05-10 10:09:44.369855');
INSERT INTO "product_price_history" VALUES (60,6,32.24,'2025-05-11 10:09:44.369860');
INSERT INTO "product_price_history" VALUES (61,7,59.13,'2025-05-02 10:09:44.370049');
INSERT INTO "product_price_history" VALUES (62,7,61.64,'2025-05-03 10:09:44.370060');
INSERT INTO "product_price_history" VALUES (63,7,68.48,'2025-05-04 10:09:44.370067');
INSERT INTO "product_price_history" VALUES (64,7,72.66,'2025-05-05 10:09:44.370073');
INSERT INTO "product_price_history" VALUES (65,7,68.7,'2025-05-06 10:09:44.370079');
INSERT INTO "product_price_history" VALUES (66,7,55.51,'2025-05-07 10:09:44.370085');
INSERT INTO "product_price_history" VALUES (67,7,74.44,'2025-05-08 10:09:44.370091');
INSERT INTO "product_price_history" VALUES (68,7,59.97,'2025-05-09 10:09:44.370096');
INSERT INTO "product_price_history" VALUES (69,7,65.92,'2025-05-10 10:09:44.370102');
INSERT INTO "product_price_history" VALUES (70,7,52.8,'2025-05-11 10:09:44.370107');
INSERT INTO "product_price_history" VALUES (71,8,87.1,'2025-05-02 10:09:44.370538');
INSERT INTO "product_price_history" VALUES (72,8,65.97,'2025-05-03 10:09:44.370556');
INSERT INTO "product_price_history" VALUES (73,8,65.71,'2025-05-04 10:09:44.371444');
INSERT INTO "product_price_history" VALUES (74,8,86.89,'2025-05-05 10:09:44.371457');
INSERT INTO "product_price_history" VALUES (75,8,84.06,'2025-05-06 10:09:44.371464');
INSERT INTO "product_price_history" VALUES (76,8,69.74,'2025-05-07 10:09:44.371470');
INSERT INTO "product_price_history" VALUES (77,8,73.04,'2025-05-08 10:09:44.371477');
INSERT INTO "product_price_history" VALUES (78,8,87.15,'2025-05-09 10:09:44.371487');
INSERT INTO "product_price_history" VALUES (79,8,81.35,'2025-05-10 10:09:44.371493');
INSERT INTO "product_price_history" VALUES (80,8,90.1,'2025-05-11 10:09:44.371500');
INSERT INTO "product_price_history" VALUES (81,9,18.54,'2025-05-02 10:09:44.371798');
INSERT INTO "product_price_history" VALUES (82,9,22.39,'2025-05-03 10:09:44.371815');
INSERT INTO "product_price_history" VALUES (83,9,20.28,'2025-05-04 10:09:44.371823');
INSERT INTO "product_price_history" VALUES (84,9,19.85,'2025-05-05 10:09:44.371828');
INSERT INTO "product_price_history" VALUES (85,9,24.0,'2025-05-06 10:09:44.371834');
INSERT INTO "product_price_history" VALUES (86,9,21.59,'2025-05-07 10:09:44.371840');
INSERT INTO "product_price_history" VALUES (87,9,22.42,'2025-05-08 10:09:44.371846');
INSERT INTO "product_price_history" VALUES (88,9,16.62,'2025-05-09 10:09:44.371851');
INSERT INTO "product_price_history" VALUES (89,9,18.06,'2025-05-10 10:09:44.371857');
INSERT INTO "product_price_history" VALUES (90,9,23.57,'2025-05-11 10:09:44.371863');
INSERT INTO "product_price_history" VALUES (91,10,63.44,'2025-05-02 10:09:44.372100');
INSERT INTO "product_price_history" VALUES (92,10,67.36,'2025-05-03 10:09:44.372113');
INSERT INTO "product_price_history" VALUES (93,10,55.55,'2025-05-04 10:09:44.372121');
INSERT INTO "product_price_history" VALUES (94,10,68.26,'2025-05-05 10:09:44.372128');
INSERT INTO "product_price_history" VALUES (95,10,70.12,'2025-05-06 10:09:44.372134');
INSERT INTO "product_price_history" VALUES (96,10,51.36,'2025-05-07 10:09:44.372139');
INSERT INTO "product_price_history" VALUES (97,10,61.38,'2025-05-08 10:09:44.372146');
INSERT INTO "product_price_history" VALUES (98,10,67.37,'2025-05-09 10:09:44.372152');
INSERT INTO "product_price_history" VALUES (99,10,58.73,'2025-05-10 10:09:44.372168');
INSERT INTO "product_price_history" VALUES (100,10,54.58,'2025-05-11 10:09:44.372174');
INSERT INTO "order_item" VALUES (1,1,10,143.68,62.16,8931.1488);
INSERT INTO "order_item" VALUES (2,1,5,125.21,54.01,6762.5921);
INSERT INTO "order_item" VALUES (3,1,6,85.36,33.78,2883.4608);
INSERT INTO "order_item" VALUES (4,2,1,151.89,30.92,4696.4388);
INSERT INTO "order_item" VALUES (5,2,8,168.19,76.57,12878.3083);
INSERT INTO "order_item" VALUES (6,3,2,157.45,64.07,10087.8215);
INSERT INTO "order_item" VALUES (7,3,7,119.72,63.46,7597.4312);
INSERT INTO "order_item" VALUES (8,4,2,104.3,64.07,6682.501);
INSERT INTO "order_item" VALUES (9,4,10,144.34,62.16,8972.1744);
INSERT INTO "order_item" VALUES (10,5,7,73.03,63.46,4634.4838);
INSERT INTO "order_item" VALUES (11,5,7,65.9,63.46,4182.014);
INSERT INTO "order_item" VALUES (12,5,10,168.17,62.16,10453.4472);
INSERT INTO "order_item" VALUES (13,6,2,75.6,64.07,4843.692);
INSERT INTO "order_item" VALUES (14,6,3,61.63,41.97,2586.6111);
INSERT INTO "order_item" VALUES (15,6,5,130.31,54.01,7038.0431);
INSERT INTO "order_item" VALUES (16,7,8,76.23,76.57,5836.9311);
INSERT INTO "order_item" VALUES (17,7,4,115.61,40.65,4699.5465);
INSERT INTO "order_item" VALUES (18,7,5,181.3,54.01,9792.013);
INSERT INTO "order_item" VALUES (19,8,5,101.62,54.01,5488.4962);
INSERT INTO "order_item" VALUES (20,8,5,75.17,54.01,4059.9317);
INSERT INTO "order_item" VALUES (21,8,10,134.81,62.16,8379.7896);
INSERT INTO "order_item" VALUES (22,9,6,91.07,33.78,3076.3446);
INSERT INTO "order_item" VALUES (23,10,3,123.45,41.97,5181.1965);
INSERT INTO "order_item" VALUES (24,10,3,191.25,41.97,8026.7625);
INSERT INTO "order_item" VALUES (25,11,8,250.0,76.57,19142.5);
INSERT INTO "negotiation" VALUES (1,1,'vendor',106.56,'pending','Negotiation message 0','2025-05-09 10:09:44.395075',NULL);
INSERT INTO "negotiation" VALUES (2,1,'farmer',97.93,'accepted','Negotiation message 1','2025-05-07 10:09:44.395149','2025-05-09 10:09:44.395235');
INSERT INTO "negotiation" VALUES (3,2,'vendor',101.67,'pending','Negotiation message 0','2025-05-06 10:09:44.395670',NULL);
INSERT INTO "negotiation" VALUES (4,2,'farmer',98.09,'accepted','Negotiation message 1','2025-05-06 10:09:44.395697','2025-05-12 10:09:44.395700');
INSERT INTO "negotiation" VALUES (5,3,'vendor',175.4,'pending','Negotiation message 0','2025-05-09 10:09:44.395960',NULL);
INSERT INTO "negotiation" VALUES (6,3,'farmer',195.45,'accepted','Negotiation message 1','2025-05-06 10:09:44.395982','2025-05-09 10:09:44.395984');
INSERT INTO "negotiation" VALUES (7,4,'vendor',90.43,'pending','Negotiation message 0','2025-05-03 10:09:44.396209',NULL);
INSERT INTO "negotiation" VALUES (8,4,'farmer',125.8,'accepted','Negotiation message 1','2025-05-07 10:09:44.396228','2025-05-10 10:09:44.396230');
INSERT INTO "negotiation" VALUES (9,5,'vendor',117.79,'pending','Negotiation message 0','2025-05-11 10:09:44.396430',NULL);
INSERT INTO "negotiation" VALUES (10,5,'farmer',111.5,'accepted','Negotiation message 1','2025-05-04 10:09:44.396448','2025-05-09 10:09:44.396450');
INSERT INTO "negotiation" VALUES (11,6,'vendor',157.23,'pending','Negotiation message 0','2025-05-03 10:09:44.396646',NULL);
INSERT INTO "negotiation" VALUES (12,6,'farmer',107.29,'accepted','Negotiation message 1','2025-05-02 10:09:44.396663','2025-05-11 10:09:44.396666');
INSERT INTO "negotiation" VALUES (13,7,'vendor',113.98,'pending','Negotiation message 0','2025-05-10 10:09:44.396848',NULL);
INSERT INTO "negotiation" VALUES (14,7,'farmer',121.7,'accepted','Negotiation message 1','2025-05-08 10:09:44.396864','2025-05-09 10:09:44.396866');
INSERT INTO "negotiation" VALUES (15,8,'vendor',112.43,'pending','Negotiation message 0','2025-05-02 10:09:44.397070',NULL);
INSERT INTO "negotiation" VALUES (16,8,'farmer',118.77,'accepted','Negotiation message 1','2025-05-08 10:09:44.397088','2025-05-08 10:09:44.397090');
INSERT INTO "negotiation" VALUES (17,9,'vendor',16.22,'pending','Negotiation message 0','2025-05-03 10:09:44.397276',NULL);
INSERT INTO "negotiation" VALUES (18,9,'farmer',52.12,'accepted','Negotiation message 1','2025-05-04 10:09:44.397293','2025-05-07 10:09:44.397295');
INSERT INTO "negotiation" VALUES (19,10,'vendor',96.07,'pending','Negotiation message 0','2025-05-07 10:09:44.397492',NULL);
INSERT INTO "negotiation" VALUES (20,10,'farmer',114.62,'accepted','Negotiation message 1','2025-05-10 10:09:44.397509','2025-05-08 10:09:44.397512');
INSERT INTO "negotiation" VALUES (21,11,'vendor',76.57,'pending','','2025-05-12 11:18:08.335348',NULL);
INSERT INTO "rating" VALUES (1,9,1,1,4,'Good transaction','2025-05-03 10:09:44.401324');
INSERT INTO "rating" VALUES (2,9,1,2,5,'Good transaction','2025-05-08 10:09:44.401695');
INSERT INTO "rating" VALUES (3,3,4,3,4,'Good transaction','2025-05-07 10:09:44.402154');
INSERT INTO "rating" VALUES (4,4,2,4,4,'Good transaction','2025-05-03 10:09:44.402554');
INSERT INTO "rating" VALUES (5,4,2,5,3,'Good transaction','2025-05-10 10:09:44.402751');
INSERT INTO "rating" VALUES (6,10,2,6,4,'Good transaction','2025-05-09 10:09:44.403097');
INSERT INTO "rating" VALUES (7,9,1,7,4,'Good transaction','2025-05-11 10:09:44.403298');
INSERT INTO "rating" VALUES (8,3,6,8,3,'Good transaction','2025-05-04 10:09:44.403493');
INSERT INTO "rating" VALUES (9,3,4,9,3,'Good transaction','2025-05-06 10:09:44.403693');
INSERT INTO "rating" VALUES (10,1,4,10,3,'Good transaction','2025-05-09 10:09:44.404043');
COMMIT;
