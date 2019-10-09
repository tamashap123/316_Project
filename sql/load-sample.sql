-- NOTE: This is fake data, not based on real voting or sponsorship

INSERT INTO Congressman VALUES(1, 'Richard Burr', 'S', 'NC', NULL, 'R');
INSERT INTO Congressman VALUES(2, 'George Butterfield Jr.', 'H', 'NC', 1, 'D');
INSERT INTO Bill VALUES('H', 2217, 113, TRUE, 'Affordable Care Act...', 'Health', '2010-03-23');
INSERT INTO SponsoredBy VALUES('H', 2217, 2);
INSERT INTO Vote VALUES(1, 'H', 2217, 'Nay');
INSERT INTO Vote VALUES(2, 'H', 2217, 'Aye');
INSERT INTO RegisteredUser VALUES('johndoe@gmail.com', 'John Doe', 'NC', 1);