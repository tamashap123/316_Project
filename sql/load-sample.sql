-- NOTE: This is fake data, not based on real voting or sponsorship

INSERT INTO Congressman VALUES(1, 'Richard Burr', 'S', 'NC', NULL, 'R');
INSERT INTO Congressman VALUES(2, 'George Butterfield Jr.', 'H', 'NC', 1, 'D');
INSERT INTO Congressman VALUES(3, 'Kamala Harris', 'S', 'CA', 27, 'D');
INSERT INTO Bill VALUES('H', 2217, 113, TRUE, 'Affordable Care Act...', 'Health', '2010-03-23');
INSERT INTO Bill VALUES('H', 2218, 113, TRUE, 'Another act...', 'Health', '2010-03-25');
INSERT INTO Bill VALUES('S', 2218, 115, TRUE, 'A third act...', 'Economics', '2014-10-23');
INSERT INTO SponsoredBy VALUES('H', 2217, 2);
INSERT INTO SponsoredBy VALUES('H', 2218, 3);
INSERT INTO Vote VALUES(1, 'H', 2217, 'Nay');
INSERT INTO Vote VALUES(2, 'H', 2217, 'Aye');
INSERT INTO RegisteredUser VALUES('johndoe@gmail.com', 'John Doe', 'NC', 1);