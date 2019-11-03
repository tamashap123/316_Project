-- NOTE: This is fake data, not based on real voting or sponsorship

INSERT INTO Congressman VALUES(400054, 'Richard Burr', 'sen', 'NC', NULL, 'Republican', '202-224-3154', '217 Russell Senate Office Building Washington DC 20510', 'https://www.burr.senate.gov/contact/email');
INSERT INTO Congressman VALUES(400616, 'G. K. Butterfield', 'rep', 'NC', 1, 'Democrat', '202-225-3101', '2080 Rayburn House Office Building; Washington DC 20515-3301', NULL);
INSERT INTO Congressman VALUES(412678, 'Kamala D. Harris', 'sen', 'CA', NULL, 'Democrat', '202-224-3553', '112 Hart Senate Office Building Washington DC 20510', 'https://www.harris.senate.gov/contact');
INSERT INTO Bill VALUES('H', 2217, 113, TRUE, 'Affordable Care Act...', 'Health', '2010-03-23');
INSERT INTO Bill VALUES('H', 2218, 113, TRUE, 'Another act...', 'Health', '2010-03-25');
INSERT INTO Bill VALUES('S', 2218, 115, TRUE, 'A third act...', 'Economics', '2014-10-23');
INSERT INTO SponsoredBy VALUES('H', 2217, 400616);
INSERT INTO SponsoredBy VALUES('H', 2218, 412678);
INSERT INTO Vote VALUES(400054, 'H', 2217, 'Nay');
INSERT INTO Vote VALUES(412678, 'H', 2217, 'Aye');
INSERT INTO Vote VALUES(400616, 'H', 2217, 'Aye');
INSERT INTO Vote VALUES(412678, 'H', 2218, 'Aye');
INSERT INTO Vote VALUES(400616, 'H', 2218, 'Nay');
INSERT INTO Vote VALUES(400616, 'S', 2218, 'Aye');
INSERT INTO RegisteredUser VALUES('johndoe@gmail.com', 'John Doe', 'NC', 1);