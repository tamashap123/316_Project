-- NOTE: This is fake data, not based on real voting or sponsorship

INSERT INTO Congressman VALUES('B001135', 'Richard Burr', 'sen', 'NC', NULL, 'Republican', '202-224-3154', '217 Russell Senate Office Building Washington DC 20510', 'https://www.burr.senate.gov/contact/email');
INSERT INTO Congressman VALUES('B001251', 'G. K. Butterfield', 'rep', 'NC', 1, 'Democrat', '202-225-3101', '2080 Rayburn House Office Building; Washington DC 20515-3301', NULL);
INSERT INTO Congressman VALUES('H001075', 'Kamala D. Harris', 'sen', 'CA', NULL, 'Democrat', '202-224-3553', '112 Hart Senate Office Building Washington DC 20510', 'https://www.harris.senate.gov/contact');
INSERT INTO Bill VALUES('hr', 2217, 113, TRUE, 'Affordable Care Act...', 'Health', '2010-03-23');
INSERT INTO Bill VALUES('hr', 2218, 113, TRUE, 'Another act...', 'Health', '2010-03-25');
INSERT INTO Bill VALUES('s', 2218, 115, TRUE, 'A third act...', 'Economics', '2014-10-23');
INSERT INTO SponsoredBy VALUES('hr', 2217, 113, 'B001251');
INSERT INTO SponsoredBy VALUES('hr', 2218, 113, 'H001075');
INSERT INTO Vote VALUES('B001135', 'hr', 2217, 113, 'Nay');
INSERT INTO Vote VALUES('H001075', 'hr', 2217, 113, 'Yea');
INSERT INTO Vote VALUES('B001251', 'hr', 2217, 113, 'Yea');
INSERT INTO Vote VALUES('H001075', 'hr', 2218, 113, 'Yea');
INSERT INTO Vote VALUES('B001251', 'hr', 2218, 113, 'Nay');
INSERT INTO Vote VALUES('B001251', 's', 2218, 115, 'Yea');
INSERT INTO RegisteredUser VALUES('johndoe@gmail.com', 'John Doe', 'NC', 1);